from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import UserType
from main.serializers import UserTypeSerializer


class UserTypeList(APIView):
    @staticmethod
    def get(request):
        user_types = UserType.objects.all()
        user_type_serializer = UserTypeSerializer(instance=user_types, many=True)
        return Response(user_type_serializer.data)

    @staticmethod
    def post(request):
        user_type_serializer = UserTypeSerializer(data=request.data)
        if user_type_serializer.is_valid():
            user_type_serializer.save()
            print(user_type_serializer.data)
        return Response(user_type_serializer.data)


class UserTypeDetail(APIView):

    @staticmethod
    def get(request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_type_serializer = UserTypeSerializer(instance=user_type)

        return Response(user_type_serializer.data)

    @staticmethod
    def put(request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_type_serializer = UserTypeSerializer(instance=user_type, data=request.data, partial=True)
        if user_type_serializer.is_valid():
            user_type_serializer.save()
        return Response(user_type_serializer.data)

    @staticmethod
    def delete(request, pk):
        try:
            user_type = UserType.objects.get(type_u_id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_type_serializer = UserTypeSerializer(instance=user_type)
        user_type.delete()
        return Response(user_type_serializer.data)
