import json
import unittest
from flask import Flask
from app import db
from app.models.user_model import User
from app import create_app
from app.services.AuthService import AuthService


class UserServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and configure it
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Set up the database
        db.create_all()

    def tearDown(self):
        # Remove the database and the app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_resource(self):
        user_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post('/auth/register', json=user_data)
        self.assertEqual(response.status_code, 201)

    def test_login_resource(self):
        user_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response_register = self.client.post('/auth/register', json=user_data)
        self.assertEqual(response_register.status_code, 201)

        login_data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response_login = self.client.post('/auth/login', json=login_data)
        self.assertEqual(response_login.status_code, 200)

