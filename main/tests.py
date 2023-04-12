import itertools
import json

import requests
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APITestCase
from main.models import User
from main.views import UserList, APIView


class FullTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'user_name': 'test', 'user_type': 'test', 'login': 'test', 'password': 'test',
                         'create_test_permission': False}

    def UserTestPost(self):
        user_response = requests.post("http://localhost:8000/user", self.user_data)
        self.assertEqual(user_response.status_code, 200)

        user_json_response = json.loads(user_response.text)
        self.user_id = user_json_response['user_id']
        user_get_response = requests.get(f"http://localhost:8000/user/{self.user_id}")
        user_get_json_response = json.loads(user_get_response.text)
        self.user_data['user_id'] = self.user_id
        self.assertEqual(user_get_response.status_code, 200)
        self.assertEqual(user_get_json_response, self.user_data)

    def UserTestPut(self):
        user_put_response = requests.put(f"http://localhost:8000/user/{self.user_id}",
                                         {'user_name': 'test_put'})
        self.assertEqual(user_put_response.status_code, 200)
        self.user_data['user_name'] = 'test_put'
        self.assertEqual(json.loads(user_put_response.text), self.user_data)

    def UserTestDelete(self):
        response = requests.delete(f'http://localhost:8000/user/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['user_id'], None)

    def test_user(self):
        self.UserTestPost()
        self.UserTestPut()

    def tearDown(self) -> None:
        self.UserTestDelete()
