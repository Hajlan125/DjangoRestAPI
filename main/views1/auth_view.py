from bcrypt import checkpw
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User
from main.serializers import UserSerializer


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