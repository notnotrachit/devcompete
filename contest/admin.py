from django.contrib import admin
from .models import Contest, Problem, TestCase, Submission, SubmissionTestCase
# Register your models here.

admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
admin.site.register(SubmissionTestCase)
