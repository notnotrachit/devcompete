from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import Contest, Problem, TestCase, Submission
from django.utils import timezone
import os
import requests
import json
# Create your views here.


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
        # print(json.loads(request.body))
        code = json.loads(request.body.decode('utf-8'))['source_code']
        stdinput = json.loads(request.body.decode('utf-8'))['stdinput']
        language = json.loads(request.body.decode('utf-8'))['language'].lower()
        print(language)
        all_languages={
            "python": 71,
            "c++": 53,
            "java": 62,
            "javascript": 63,
            "rust": 73,
        }

        endpoint = os.getenv('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        data = {
            'source_code': code,
            'language_id': all_languages[language],
            'stdin': stdinput,
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
        c_problem = Problem.objects.filter(contest=contest)[0]
        code = json.loads(request.body.decode('utf-8'))['source_code']
        submission = Submission.objects.create(problem=c_problem, user=request.user, code=code, status="In Queue", score=0, language="Python")

        test_cases = TestCase.objects.filter(problem=c_problem)

        final_data = {"submissions": [], "total_test_cases": len(test_cases), "passed_test_case": 0}
        # print(final_data)
        endpoint = os.getenv('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        score=0
        for _ in range(len(test_cases)):
            data = {
                'source_code': code,
                'language_id': 71,
                'stdin': test_cases[_].user_input,
            }
            response = requests.post(endpoint, json=data)
            # print(response.json())
            user_output = response.json()['stdout']
            if user_output.endswith('\n'):
                user_output = user_output[:-1]
            final_data["submissions"].append({
                "expected_output": test_cases[_].output,
                "user_output": user_output,
            })
            if user_output == test_cases[_].output:
                final_data["passed_test_case"] += 1
            score += test_cases[_].points
        
        print(f"Final Score: {final_data['passed_test_case']}/{final_data['total_test_cases']}")




        # resp = {
        #     'output': response.json()['stdout'],
        # }
        return JsonResponse({'output': f"Final Score: {final_data['passed_test_case']}/{final_data['total_test_cases']}"})
