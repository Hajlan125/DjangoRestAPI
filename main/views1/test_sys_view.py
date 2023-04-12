from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import TestingSystem
from main.serializers import TestingSystemSerializer


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