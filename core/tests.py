"""Testing cases for the core app"""
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from core.crud.standard import Crud
from core.crud.exeptions import NonCallableParam
# Create your tests here.

class LoginTest(APITestCase):
    """Tests for login"""
    @staticmethod
    def create_user():
        """Creates an user in the db"""
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()

    def test_login(self):
        """Test a correct login"""
        LoginTest.create_user()
        url = reverse('login')
        data = {
            'username':'john',
            'password':'johnpassword'
        }
        response = self.client.post(url, data, format='json')
        answer = json.loads(response.content)
        self.assertEqual(answer["detail"], "Success")

    def test_failed_login(self):
        """Test an incorrect login"""
        url = reverse('login')
        data = {
            'username':'john',
            'password':'johnpassword'
        }
        response = self.client.post(url, data, format='json')
        answer = json.loads(response.content)
        self.assertEqual(answer["detail"], "Invalid credentials")

class CrudTest(TestCase):
    """Test for the Crud class """
    def validate_function_test(self):
        """Test for the validate function"""
        def callablefunc():
            pass

        self.assertEqual(Crud.validate_function(callablefunc), False)
        self.assertEqual(Crud.validate_function(None), False)

    def validate_function_test_raise_exeption(self):
        with self.assertRaises(NonCallableParam):
            Crud.validate_function(3)
