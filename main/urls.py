from django.urls import path

from main.views import UserList, UserDetail, ScoreList, ScoreDetail, TestList, TestDetail, AnswerList, AnswerDetail, \
    QuestionList, QuestionDetail, TestingSystemList, TestingSystemDetail

rest_api_patterns = ((
    path('user', UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view()),
    path('score', ScoreList.as_view()),
    path('score/<int:pk>', ScoreDetail.as_view()),
    path('test', TestList.as_view()),
    path('test/<int:pk>', TestDetail.as_view()),
    path('answer', AnswerList.as_view()),
    path('answer/<int:pk>', AnswerDetail.as_view()),
    path('question', QuestionList.as_view()),
    path('question/<int:pk>', QuestionDetail.as_view()),
    path('testing_system', TestingSystemList.as_view()),
    path('testing_system/<int:pk>', TestingSystemDetail.as_view()),
), 'djangoRest')