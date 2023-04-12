from django.urls import path

from main.views import TestList, TestDetail, AnswerList, AnswerDetail, \
    QuestionList, QuestionDetail, TestingSystemList, TestingSystemDetail, ExampleAuthentication

from main.views1.user_view import UserList, UserDetail


rest_api_patterns = ((
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
    path('auth', ExampleAuthentication.as_view())
), 'djangoRest')