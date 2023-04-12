from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import QuestionType
from main.serializers import UserTypeSerializer, QuestionTypeSerializer


class QuestionTypeList(APIView):
    def get(self, request):
        question_types = QuestionType.objects.all()
        question_type_serializer = UserTypeSerializer(instance=question_types, many=True)
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
