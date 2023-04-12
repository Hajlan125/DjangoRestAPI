from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Answer
from main.serializers import AnswerSerializer


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