from django.contrib import admin
from .models import Question, TestCase, Submission

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'score')

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('test_input', 'test_output', 'test_score', 'hidden')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_text', 'submission_score', 'pub_date', 'question', 'user')

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(Submission, SubmissionAdmin)