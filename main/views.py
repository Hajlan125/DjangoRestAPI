import hashlib
import os

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import exceptions
import bcrypt


from main.models import User, Question, Answer, Score, Test, TestingSystem
from main.serializers import UserSerializer, QuestionSerializer, AnswerSerializer, ScoreSerializer, TestSerializer, \
    TestingSystemSerializer, UserExpandSerializer, TestExpandSerializer, QuestionExpandSerializer, QuestionPassingSerializer


class UserList(APIView):
    def get(self, request):
        type = request.GET.get("user_type")
        expand = request.GET.get("expand")
        users = User.objects.all()
        if type is not None:
            users = users.filter(user_type=type)
        if expand is not None:
            user_serializer = UserExpandSerializer(instance=users, many=True)
        else :
            user_serializer = UserSerializer(instance=users, many=True)

        return Response(user_serializer.data)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            print(user_serializer.data)
        return Response(user_serializer.data)
class UserDetail(APIView):
    def get(self, request, pk):
        expand = request.GET.get("expand")
        try:
            user = User.objects.get(user_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if expand is not None:
            user_serializer = UserExpandSerializer(instance=user)
        else :
            user_serializer = UserSerializer(instance=user)

        return Response(user_serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(user_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        return Response(user_serializer.data)

    def delete(self, request, pk):
        try:
            user = User.objects.get(user_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(instance=user)
        user.delete()
        return Response(user_serializer.data)

class QuestionList(APIView):
    def get(self,request):
        test = request.GET.get("q_test_id")
        expand = request.GET.get("expand")
        passing_expand = request.GET.get("passing_expand")
        questions = Question.objects.all()
        if test is not None:
            questions = questions.filter(q_test_id=test)
        elif expand is not None:
            questions = questions.filter(q_parent_id=0)
            question_serializer = QuestionExpandSerializer(instance=questions, many=True)
        elif passing_expand is not None:
            question_serializer = QuestionPassingSerializer(instance=questions, many=True)
        else:
            question_serializer = QuestionSerializer(instance=questions, many=True)
        return Response(question_serializer.data)
    def post(self,request):
        question_serializer = QuestionSerializer(data=request.data)
        if question_serializer.is_valid():
            question_serializer.save()
        return Response(question_serializer.data)
class QuestionDetail(APIView):
    def get(self, request, pk):
        expand = request.GET.get("expand")
        try:
            question = Question.objects.get(q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if expand is not None:
            question_serializer = QuestionExpandSerializer(instance=question)
        else :
            question_serializer = QuestionSerializer(instance=question)
        return Response(question_serializer.data)

    def put(self, request, pk):
        try:
            question = Question.objects.get(q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        question_serializer = QuestionSerializer(instance=question, data=request.data, partial=True)
        if question_serializer.is_valid():
            question_serializer.save()
        return Response(question_serializer.data)

    def delete(self, request, pk):
        try:
            question = Question.objects.get(q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        question_serializer = QuestionSerializer(instance=question)
        question.delete()
        return Response(question_serializer.data)

class AnswerList(APIView):
    def get(self,request):
        question = request.GET.get("answ_question_id")
        answers = Answer.objects.all()
        if question is not None:
            answers = answers.filter(answ_question_id=question)
        answer_serializer = AnswerSerializer(instance=answers, many=True)
        return Response(answer_serializer.data)
    def post(self,request):
        answer_serializer = AnswerSerializer(data=request.data)
        if answer_serializer.is_valid():
            answer_serializer.save()
        return Response(answer_serializer.data)
class AnswerDetail(APIView):
    def get(self, request, pk):
        try:
            answer = Answer.objects.get(answ_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        answer_serializer = AnswerSerializer(instance=answer)
        return Response(answer_serializer.data)

    def put(self, request, pk):
        try:
            answer = Answer.objects.get(answ_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        answer_serializer = AnswerSerializer(instance=answer, data=request.data, partial=True)
        if answer_serializer.is_valid():
            answer_serializer.save()
        return Response(answer_serializer.data)

    def delete(self, request, pk):
        try:
            answer = Answer.objects.get(answ_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        answer_serializer = AnswerSerializer(instance=answer)
        answer.delete()
        return Response(answer_serializer.data)

class ScoreList(APIView):
    def get(self,request):
        scores = Score.objects.all()
        score_serializer = ScoreSerializer(instance=scores, many=True)
        return Response(score_serializer.data)
    def post(self,request):
        score_serializer = ScoreSerializer(data=request.data)
        if score_serializer.is_valid():
            score_serializer.save()
        return Response(score_serializer.data)
class ScoreDetail(APIView):
    def get(self, request, pk):
        try:
            score = Score.objects.get(score_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        score_serializer = ScoreSerializer(instance=score)
        return Response(score_serializer.data)

    def put(self, request, pk):
        try:
            score = Score.objects.get(score_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        score_serializer = ScoreSerializer(instance=score, data=request.data, partial=True)
        if score_serializer.is_valid():
            score_serializer.save()
        return Response(score_serializer.data)

    def delete(self, request, pk):
        try:
            score = Score.objects.get(score_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        score_serializer = ScoreSerializer(instance=score)
        score.delete()
        return Response(score_serializer.data)

class TestList(APIView):
    def get(self,request):
        creator = request.GET.get("test_creator")
        subject = request.GET.get("test_subject")
        expand = request.GET.get("expand")
        tests = Test.objects.all().order_by("test_id")
        if creator is not None:
            tests = tests.filter(test_creator=creator)
        if subject is not None:
            tests = tests.filter(test_subject=subject)
        if expand is not None:
            test_serializer = TestExpandSerializer(instance=tests, many=True)
        else :
            test_serializer = TestSerializer(instance=tests, many=True)
        return Response(test_serializer.data)
    def post(self,request):
        test_serializer = TestSerializer(data=request.data)
        if test_serializer.is_valid():
            test_serializer.save()
        else:
            print(test_serializer.data)
        return Response(test_serializer.data)
class TestDetail(APIView):
    def get(self, request, pk):
        expand = request.GET.get("expand")
        try:
            test = Test.objects.get(test_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if expand is not None:
            test_serializer = TestExpandSerializer(instance=test)
        else:
            test_serializer = TestSerializer(instance=test)
        return Response(test_serializer.data)

    def put(self, request, pk):
        try:
            test = Test.objects.get(test_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_serializer = TestSerializer(instance=test, data=request.data, partial=True)
        if test_serializer.is_valid():
            test_serializer.save()
        return Response(test_serializer.data)

    def delete(self, request, pk):
        try:
            test = Test.objects.get(test_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_serializer = TestSerializer(instance=test)
        test.delete()
        return Response(test_serializer.data)

class TestingSystemList(APIView):
    def get(self,request):
        user = request.GET.get("ts_user_id")
        test = request.GET.get("ts_test_id")
        testing_systems = TestingSystem.objects.all()
        if user is not None:
            testing_systems = testing_systems.filter(ts_user_id=user)
        if test is not None:
            testing_systems = testing_systems.filter(ts_test_id=test)
        testing_system_serializer = TestingSystemSerializer(instance=testing_systems, many=True)
        return Response(testing_system_serializer.data)
    def post(self,request):
        testing_system_serializer = TestingSystemSerializer(data=request.data)
        if testing_system_serializer.is_valid():
            testing_system_serializer.save()
        return Response(testing_system_serializer.data)
class TestingSystemDetail(APIView):
    def get(self, request, pk):
        try:
            testing_system = TestingSystem.objects.get(ts_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_serializer = TestingSystemSerializer(instance=testing_system)
        return Response(test_serializer.data)

    def put(self, request, pk):
        try:
            test = TestingSystem.objects.get(ts_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_serializer = TestingSystemSerializer(instance=test, data=request.data, partial=True)
        if test_serializer.is_valid():
            test_serializer.save()
        return Response(test_serializer.data)

    def delete(self, request, pk):
        try:
            test = TestingSystem.objects.get(ts_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_serializer = TestingSystemSerializer(instance=test)
        test.delete()
        return Response(test_serializer.data)

class ExampleAuthentication(APIView):
    def get(self, request):
        username = request.GET.get('login')
        password = request.GET.get('password')
        try:
            user = User.objects.get(login=username)
            if username == 'admin':
                user_serializer = UserSerializer(instance=user)
                return Response(user_serializer.data)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                user_serializer = UserSerializer(instance=user)
                return Response(user_serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

