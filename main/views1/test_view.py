from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Test
from main.serializers import TestExpandSerializer, TestSerializer


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