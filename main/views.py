import copy
import hashlib
import os

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import exceptions
from bcrypt import checkpw


from main.models import User, Question, Answer, Test, TestingSystem, UserType, QuestionType, TestType, ParallelBlock
from main.serializers import UserSerializer, QuestionSerializer, AnswerSerializer, TestSerializer, \
    TestingSystemSerializer, UserExpandSerializer, TestExpandSerializer, QuestionExpandSerializer, \
    QuestionPassingSerializer, UserTypeSerializer, QuestionTypeSerializer, TestTypeSerializer, ParallelBlockSerializer


class UserTypeList(APIView):
    def get(self, request):
        user_types = UserType.objects.all()
        user_type_serializer = UserTypeSerializer(instance=user_types, many=True)
        return Response(user_type_serializer.data)
    def post(self, request):
        user_type_serializer = UserTypeSerializer(data=request.data)
        if user_type_serializer.is_valid():
            user_type_serializer.save()
            print(user_type_serializer.data)
        return Response(user_type_serializer.data)
class UserTypeDetail(APIView):
    def get(self, request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_type_serializer = UserTypeSerializer(instance=user_type)

        return Response(user_type_serializer.data)

    def put(self, request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_type_serializer = UserTypeSerializer(instance=user_type, data=request.data, partial=True)
        if user_type_serializer.is_valid():
            user_type_serializer.save()
        return Response(user_type_serializer.data)

    def delete(self, request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_type_serializer = UserTypeSerializer(instance=user_type)
        user_type.delete()
        return Response(user_type_serializer.data)


class QuestionTypeList(APIView):
    def get(self, request):
        question_types = QuestionType.objects.all()
        question_type_serializer = QuestionTypeSerializer(instance=question_types, many=True)
        return Response(question_type_serializer.data)
    def post(self, request):
        question_type_serializer = QuestionTypeSerializer(data=request.data)
        if question_type_serializer.is_valid():
            question_type_serializer.save()
            print(question_type_serializer.data)
        return Response(question_type_serializer.data)
class QuestionTypeDetail(APIView):
    def get(self, request, pk):
        try:
            question_type = QuestionType.objects.get(type_q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        question_type_serializer = QuestionTypeSerializer(instance=question_type)

        return Response(question_type_serializer.data)

    def put(self, request, pk):
        try:
            question_type = QuestionType.objects.get(type_q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        question_type_serializer = QuestionTypeSerializer(instance=question_type, data=request.data, partial=True)
        if question_type_serializer.is_valid():
            question_type_serializer.save()
        return Response(question_type_serializer.data)

    def delete(self, request, pk):
        try:
            question_type = QuestionType.objects.get(type_q_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        question_type_serializer = QuestionTypeSerializer(instance=question_type)
        question_type.delete()
        return Response(question_type_serializer.data)


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
        connected = request.GET.get("connected")
        questions = Question.objects.all()
        if test is not None:
            questions = questions.filter(q_test_id=test)
        elif expand is not None:
            questions = questions.filter(q_parent_id=0)
            question_serializer = QuestionExpandSerializer(instance=questions, many=True)
        elif passing_expand is not None:
            question_serializer = QuestionPassingSerializer(instance=questions, many=True)
        elif connected is not None:
            questions = questions.filter(q_conection = connected)
            questions_serializer = QuestionSerializer(instance=questions, many=True)
        else:
            question_serializer = QuestionSerializer(instance=questions, many=True)
        return Response(question_serializer.data)
    def post(self,request):
        question_serializer = QuestionSerializer(data=request.data)
        if question_serializer.is_valid():
            question_serializer.save()
        else:
            print(question_serializer.errors)
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
            print(test_serializer.errors)
            # print(test_serializer.data)
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
            if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                user_serializer = UserSerializer(instance=user)
                return Response(user_serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PermissionChecker(APIView):
    def get(self, request):
        required = request.GET.get('req')
        u_id = request.GET.get('u_id')
        try:
            user_access_level = User.objects.get(user_id=u_id)
            if user_access_level > required:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_100_CONTINUE)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TestTypeList(APIView):
    def get(self, request):
        test_types = TestType.objects.all()
        test_type_serializer = TestTypeSerializer(instance=test_types, many=True)
        return Response(test_type_serializer.data)
    def post(self, request):
        test_type_serializer = TestTypeSerializer(data=request.data)
        if test_type_serializer.is_valid():
            test_type_serializer.save()
            print(test_type_serializer.data)
        return Response(test_type_serializer.data)
class TestTypeDetail(APIView):
    def get(self, request, pk):
        try:
            test_type = TestType.objects.get(type_t_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        test_type_serializer = TestTypeSerializer(instance=test_type)

        return Response(test_type_serializer.data)

    def put(self, request, pk):
        try:
            test_type = TestType.objects.get(type_t_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_type_serializer = TestTypeSerializer(instance=test_type, data=request.data, partial=True)
        if test_type_serializer.is_valid():
            test_type_serializer.save()
        return Response(test_type_serializer.data)

    def delete(self, request, pk):
        try:
            test_type = TestType.objects.get(type_t_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_type_serializer = TestTypeSerializer(instance=test_type)
        test_type.delete()
        return Response(test_type_serializer.data)


class ParallelBlockList(APIView):
    def get(self, request):
        p_blocks = ParallelBlock.objects.all()
        p_b_serializer = ParallelBlockSerializer(instance=p_blocks, many=True)
        return Response(p_b_serializer.data)
    def post(self, request):
        p_b_serializer = ParallelBlockSerializer(data=request.data)
        if p_b_serializer.is_valid():
            p_b_serializer.save()
            print(p_b_serializer.data)
        return Response(p_b_serializer.data)