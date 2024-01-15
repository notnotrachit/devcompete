from django.shortcuts import render
from .models import Question, TestCase, Submission
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
    context = {'question': question}
    return render(request, 'practice/question.html', context)