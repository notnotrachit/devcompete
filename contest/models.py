from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    rules = models.TextField()
    prizes = models.TextField()
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2', null=True, blank=True)
    player1_submitted = models.BooleanField(default=False)
    player2_submitted = models.BooleanField(default=False)
    ai_result_analysis = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    
class Problem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    constraints = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return self.name

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_input = models.TextField()
    output = models.TextField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.problem.name + " - " + str(self.pk)

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=100)
    score = models.IntegerField()
    language = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem.name + " - " + str(self.pk)
    
class SubmissionTestCase(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    time = models.IntegerField()
    memory = models.IntegerField()

    def __str__(self):
        return self.submission.problem.name + " - " + str(self.pk)
    
class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.contest.name + " - " + self.problem.name
    
class ContestSubmission(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    def __str__(self):
        return self.contest.name + " - " + self.submission.problem.name + " - " + str(self.pk)


class Results(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_result')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_result')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner')
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contest.name + " - " + str(self.pk)