from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import Contest, Problem
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
        return render(request, self.template_name, {
            'contest': contest,
            'problem': c_problem,
            'player_number': 1 if request.user == contest.player1 else 2,
        })
    
    def post(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=kwargs['id'])
        c_problem = Problem.objects.filter(contest=contest)[0]
        # print(json.loads(request.body))
        code = json.loads(request.body.decode('utf-8'))['source_code']


        endpoint = os.getenv('JUDGE_ENDPOINT')
        endpoint += "/submissions/?base64_encoded=false&wait=true"
        data = {
            'source_code': code,
            'language_id': 71,
        }

        response = requests.post(endpoint, json=data)
        print(response.json())
        resp = {
            'output': response.json()['stdout'],
        }
        return JsonResponse(resp)