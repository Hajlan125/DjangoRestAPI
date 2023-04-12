from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Question
from main.serializers import QuestionExpandSerializer, QuestionPassingSerializer, QuestionSerializer


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