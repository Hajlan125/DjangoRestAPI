from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User
from main.serializers import UserExpandSerializer, UserSerializer


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
