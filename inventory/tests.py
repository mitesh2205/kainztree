from django.test import TestCase
from rest_framework.test import APIClient  # test client for making requests to the API
from rest_framework import status # to check the status of the response
from django.contrib.auth.models import User # to create a user using user model for testing
# Create your tests here.

class DjangoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'test',
            'password': 'test'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post('/api/login/', self.user_data)
        return response.data.get('token', '')

    def test_user_signup(self):
        new_user_data = {
            'username': 'test2',
            'password': 'test2'
        }
        response = self.client.post('/api/signup/', new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post('/api/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_item_list_unauthenticated(self):
    #     response = self.client.get('/api/items/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)