"""
URL configuration for devcompete project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import MyView
from contest.views import Contests, ContestView, ContestSubmission, ResultView, CreateContest, EndContest
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from pratice.views import practice_home, create_question, question_page, run_code


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', MyView.as_view(), name='home'),
    path('contests/', login_required(Contests.as_view()), name='contests'),
    path('contest/<int:id>/', login_required(ContestView.as_view()), name='contest'),
    path('contest/<int:id>/submit/', login_required(ContestSubmission.as_view()), name='contest-submit'),
    path('contest/<int:id>/result/', login_required(ResultView.as_view()), name='contest-result'),
    path('create-contest/', login_required(CreateContest.as_view()), name='create-contest'),
    path('end-contest/<int:id>/', login_required(EndContest.as_view()), name='end-contest'),
    path('accounts/profile/', RedirectView.as_view(url='/')),
    path('practice', practice_home, name="pratice"),
    path('practice/create_question', create_question, name="create_question"),
    path('practice/<int:question_id>/', question_page, name="question_page"),
    path('practice/<int:question_id>/run', run_code, name="run_code"),
    
]
