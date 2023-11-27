from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from .models import Contest, Problem, TestCase, Submission
from django.utils import timezone
import os
import requests
import json
import google.generativeai as palm
from django.contrib.auth.models import User

palm.configure(api_key=os.environ['PALM_API_KEY'])
# Create your views here.

all_languages={
    "python": 71,
    "c++": 53,
    "java": 62,
    "javascript": 63,
    "rust": 73,
}

class Contests(View):
    template_name = "contests.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        current_contests = Contest.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).filter(player1=user) | Contest.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).filter(player2=user)
        return render(request, self.template_name, {
            'current_contests': current_contests,
        })

class ContestView(View):
    template_name = "contest.html"

    def get(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        if request.user != contest.player1 and request.user != contest.player2:
            return redirect('home')
        c_problem = Problem.objects.filter(contest=contest)[0]
        end_time = contest.end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        print("end time" , end_time)
        return render(request, self.template_name, {
            'contest': contest,
            'problem': c_problem,
            'player_number': 1 if request.user == contest.player1 else 2,
            'end_time': end_time,
        })
    
    def post(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        c_problem = Problem.objects.filter(contest=contest)[0]
        if request.user != contest.player1 and request.user != contest.player2:
            return redirect('home')
        # print(json.loads(request.body))
        code = json.loads(request.body.decode('utf-8'))['source_code']
        stdinput = json.loads(request.body.decode('utf-8'))['stdinput']
        language = json.loads(request.body.decode('utf-8'))['language'].lower()
        print(language)


        endpoint = os.getenv('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        data = {
            'source_code': code,
            'language_id': all_languages[language],
            'stdin': stdinput,
            'redirect_stderr_to_stdout': True,
        }

        response = requests.post(endpoint, json=data)
        print(response.json())
        resp = {
            'output': response.json()['stdout'],
        }
        return JsonResponse(resp)
    
class ContestSubmission(View):
    def post(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        user = request.user
        if user != contest.player1 and user != contest.player2:
            return redirect('home')
        if request.user == contest.player1:
            if contest.player1_submitted == True:
                return redirect('contest-result', id=contest.pk)
        elif request.user == contest.player2:
            if contest.player2_submitted == True:
                return redirect('contest-result', id=contest.pk)
        c_problem = Problem.objects.filter(contest=contest)[0]
        code = json.loads(request.body.decode('utf-8'))['source_code']
        language = json.loads(request.body.decode('utf-8'))['language']
        submission = Submission.objects.create(problem=c_problem, user=request.user, code=code, status="In Queue", score=0, language=language)
        test_cases = TestCase.objects.filter(problem=c_problem)
        final_data = {"submissions": [], "total_test_cases": len(test_cases), "passed_test_case": 0}
        endpoint = os.getenv('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        score=0
        for _ in range(len(test_cases)):
            data = {
                'source_code': code,
                'language_id': 71,
                'stdin': test_cases[_].user_input,
                'language_id': all_languages[language.lower()],
                'redirect_stderr_to_stdout': True,
            }
            response = requests.post(endpoint, json=data)
            user_output = response.json()['stdout']
            if user_output.endswith('\n'):
                user_output = user_output[:-1]
            final_data["submissions"].append({
                "expected_output": test_cases[_].output,
                "user_output": user_output,
            })
            if user_output == test_cases[_].output.replace('\r', ''):
                final_data["passed_test_case"] += 1
            score += test_cases[_].points
        
        print(f"Final Score: {final_data['passed_test_case']}/{final_data['total_test_cases']}")
        submission.score = score
        submission.status = "Accepted" if final_data['passed_test_case'] == final_data['total_test_cases'] else "Wrong Answer"
        submission.save()
        return JsonResponse({'output': f"Final Score: {final_data['passed_test_case']}/{final_data['total_test_cases']}"})
    

class ResultView(View):
    template_name = "result.html"

    def get(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        if request.user != contest.player1 and request.user != contest.player2:
            return redirect('home')
        if contest.player1_submitted == False or contest.player2_submitted == False:
            return render(request, "result_wait.html")
        c_problem = Problem.objects.filter(contest=contest)[0]
        submission_player1 = Submission.objects.filter(problem=c_problem).filter(user=contest.player1).order_by('-score')
        submission_player2 = Submission.objects.filter(problem=c_problem).filter(user=contest.player2).order_by('-score')
        winner = None
        if len(submission_player1) == 0 and len(submission_player2) == 0:
            winner = None
        elif len(submission_player1) == 0:
            winner = contest.player2
        elif len(submission_player2) == 0:
            winner = contest.player1
        elif submission_player1[0].score > submission_player2[0].score:
            winner = contest.player1
        elif submission_player1[0].score < submission_player2[0].score:
            winner = contest.player2
        elif submission_player1[0].score == submission_player2[0].score:
            winner = contest.player1 if submission_player1[0].time < submission_player2[0].time else contest.player2
        
        if contest.ai_result_analysis is None or contest.ai_result_analysis == "":
            prompt = f"There is a coding contest between 2 players. The question was '{c_problem.description}'. Player 1 is {contest.player1.username} and Player 2 is {contest.player2.username}. The result of the contest is '{winner.username}'. {contest.player1.username}'s code is {submission_player1[0].code} and {contest.player2.username}'s code is {submission_player2[0].code}. Now analyze the code and give me proper analyses on which code is better and why?."
            ai_analysis = palm.generate_text(prompt=prompt).result
            print(ai_analysis)
            contest.ai_result_analysis = ai_analysis
            contest.save()

        return render(request, self.template_name, {
            'contest': contest,
            'problem': c_problem,
            'submissions_player1': submission_player1,
            'submissions_player2': submission_player2,
            'winner': winner,
        })
    

class CreateContest(View):
    template_name = "create-contest.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, self.template_name, {
                
            })
        else:
            return redirect('home')
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        player1_username = request.POST['player1']
        player2_username = request.POST['player2']
        player1 = None
        player2 = None
        try:
            player1 = User.objects.get(username=player1_username)
        except:
            return JsonResponse({'status': 'failure', 'message': 'Player 1 does not exist'})
        try:
            player2 = User.objects.get(username=player2_username)
        except:
            return JsonResponse({'status': 'failure', 'message': 'Player 2 does not exist'})
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        problem = request.POST['problem']
        description = request.POST['description']
        points = request.POST['points']
        user_input = request.POST['user_input']
        output = request.POST['output']
        contest = Contest.objects.create(player1=player1, player2=player2, start_date=start_date, end_date=end_date)
        problem = Problem.objects.create(contest=contest, description=description, points=points)
        TestCase.objects.create(problem=problem, user_input=user_input, output=output)
        return JsonResponse({'status': 'success'})
    

class EndContest(View):
    def post(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        user = request.user
        if user != contest.player1 and user != contest.player2:
            return redirect('home')
        if request.user == contest.player1:
            contest.player1_submitted = True
        elif request.user == contest.player2:
            contest.player2_submitted = True
        contest.save()
        return redirect('contest-result', id=contest.pk)
