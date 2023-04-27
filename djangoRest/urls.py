"""djangoRest URL Configuration

The `urlpatterns` list routes URLs to views1. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views1
    1. Add an import:  from my_app import views1
    2. Add a URL to urlpatterns:  path('', views1.home, name='home')
Class-based views1
    1. Add an import:  from other_app.views1 import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main.views import UserList, UserDetail, TestList, TestDetail, AnswerList, AnswerDetail, \
    QuestionList, QuestionDetail, TestingSystemList, TestingSystemDetail, ExampleAuthentication, \
    UserTypeList, UserTypeDetail, QuestionTypeList, QuestionTypeDetail, PermissionChecker, \
    TestTypeList, TestTypeDetail, ParallelBlockList, ParallelBlockDetail, UserAnswersValidation

from main.urls import rest_api_patterns

urlpatterns = [
    path('user', UserList.as_view(), name="user-list"),
    path('user/<int:pk>', UserDetail.as_view()),
    path('test', TestList.as_view()),
    path('test/<int:pk>', TestDetail.as_view()),
    path('answer', AnswerList.as_view()),
    path('answer/<int:pk>', AnswerDetail.as_view()),
    path('question', QuestionList.as_view()),
    path('question/<int:pk>', QuestionDetail.as_view()),
    path('testing_system', TestingSystemList.as_view()),
    path('testing_system/<int:pk>', TestingSystemDetail.as_view()),
    path('auth', ExampleAuthentication.as_view()),
    path('user_type', UserTypeList.as_view()),
    path('user_type/<int:pk>', UserTypeDetail.as_view()),
    path('q_type', QuestionTypeList.as_view()),
    path('q_type/<int:pk>', QuestionTypeDetail.as_view()),
    path('perm_checker', PermissionChecker.as_view()),
    path('test_type', TestTypeList.as_view()),
    path('test_type/<int:pk>', TestTypeDetail.as_view()),
    path('p_block', ParallelBlockList.as_view()),
    path('p_block/<int:pk>', ParallelBlockDetail.as_view()),
    path('validation', UserAnswersValidation.as_view())

]
