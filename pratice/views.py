from django.shortcuts import render
from .models import Question, TestCase, Submission
import json
import os
import requests

all_languages={
    "python": 71,
    "c++": 53,
    "java": 62,
    "javascript": 63,
    "rust": 73,
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
        print(submission_code)
        endpoint = os.environ.get('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"

        testcases = question.test_cases
        question_testcases = TestCase.objects.filter(question=question).filter(hidden=False)
        total_testcase = len(question_testcases)
        correct_testcase = 0
        language="python"
        for testcase in question_testcases:
            print(testcase.test_input)
            data = {
                'source_code': submission_code['code'],
                'stdin': testcase.test_input,
                'language_id': all_languages[language.lower()],
                'redirect_stderr_to_stdout': True,
            }
            response = requests.post(endpoint, json=data)
            output = response.json()['stdout'].strip()
            resp = {
                'output': output,
            }
            if output == testcase.test_output:
                correct_testcase += 1
            print(response.json())
        print(correct_testcase)

        return render(request, 'practice/question.html', {'question': question})
    else:
        return render(request, 'practice/question.html', {'question': question})