from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Question, TestCase, Submission
import json
import os
import requests
from devcompete.utils import optimisation_ai_help, ai_chat

all_languages={
    "python": 71,
    "c++": 53,
    "java": 62,
    "javascript": 63,
    "rust": 73,
    "go": 60,
    "golang": 60,
    "c": 50,
    "c#": 51,
    "ruby": 72,
    "php": 68,
    "swift": 74,
    "kotlin": 78,
    "scala": 81,
    "haskell": 82,
    "perl": 84,
    "elixir": 88,
}


# Create your views here.
def practice_home(request):
    all_questions = Question.objects.all()
    context = {'all_questions': all_questions}
    return render(request,  'practice/practice.html', context)


def create_question(request):
    if request.method == 'POST':
        question_name = request.POST['question_name']
        question_text = request.POST['question_text']
        pub_date = request.POST['pub_date']
        score = request.POST['score']
        test_cases = request.POST['test_cases']
        question = Question(question_name=question_name, question_text=question_text, pub_date=pub_date, score=score, test_cases=test_cases)
        question.save()
        return render(request, 'practice/practice.html')
    else:
        return render(request, 'practice/create_question.html')
    

def question_page(request, question_id):
    question = Question.objects.get(pk=question_id)
    test_cases = TestCase.objects.filter(question=question).filter(hidden=False)
    context = {'question': question, 'test_cases': test_cases}
    return render(request, 'practice/question.html', context)

def run_code(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        submission_code = request.body.decode('utf-8')
        submission_code = json.loads(submission_code)
        endpoint = os.environ.get('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        question_testcases = TestCase.objects.filter(question=question).filter(hidden=False)
        total_testcase = len(question_testcases)
        correct_testcase = 0
        language=submission_code['lang']
        testcase_stats = []
        for testcase in question_testcases:
            data = {
                'source_code': submission_code['code'],
                'stdin': testcase.test_input,
                'language_id': all_languages[language.lower()],
                'redirect_stderr_to_stdout': True,
            }
            response = requests.post(endpoint, json=data)
            # print(response.json())
            stats={
                'memory': response.json()['memory'],
                'time': response.json()['time'],
                'result': "Failed",
            }
            testcase_stats.append(stats)
            output = response.json()['stdout'].strip()
            print(output)
            print(testcase.test_output)
            if output == testcase.test_output:
                correct_testcase += 1
                stats['result'] = "Passed"
        resp = {
                'total_testcase': total_testcase,
                'correct_testcase': correct_testcase,
                'testcase_stats': testcase_stats,
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return redirect('practice:question_page', question_id=question_id)
    

def ai_optimize(request):
    if request.method == 'POST':
        req_data = request.body.decode('utf-8')
        req_data = json.loads(req_data)
        code = req_data['code']
        question_id = req_data['question_id']
        question = Question.objects.get(pk=question_id)
        question = question.question_text
        language = req_data['lang']
        response = optimisation_ai_help(code, question, language)
        output={
            'data': response
        }
        return JsonResponse(output)
    else:
        return render(request, 'practice/practice.html')


def submit_code(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        submission_code = request.body.decode('utf-8')
        submission_code = json.loads(submission_code)
        endpoint = os.environ.get('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        question_testcases = TestCase.objects.filter(question=question).order_by('hidden')
        total_testcase = len(question_testcases)
        correct_testcase = 0
        language=submission_code['lang']
        testcase_stats = []
        for testcase in question_testcases:
            data = {
                'source_code': submission_code['code'],
                'stdin': testcase.test_input,
                'language_id': all_languages[language.lower()],
                'redirect_stderr_to_stdout': True,
            }
            response = requests.post(endpoint, json=data)
            stats={
                'memory': response.json()['memory'],
                'time': response.json()['time'],
                'result': "Failed",
                'hidden': testcase.hidden,
            }
            testcase_stats.append(stats)
            output = response.json()['stdout'].strip()

            if output == testcase.test_output:
                correct_testcase += 1
                stats['result'] = "Passed"
        resp = {
                'total_testcase': total_testcase,
                'correct_testcase': correct_testcase,
                'testcase_stats': testcase_stats,
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return redirect('practice:question_page', question_id=question_id)
    

def AI_Chat(request):
    if request.method=="GET":
        return render(request, 'AI_Chat.html')
    else:
        req_post = request.body.decode('utf-8')
        req_post = json.loads(req_post)
        try:
            chat_history = req_post['chat_history']
        except:
            chat_history = []
        query = req_post['query']
        msg_history, response = ai_chat(chat_history, query)
        return JsonResponse({'response': response, 'msg_history': msg_history})
