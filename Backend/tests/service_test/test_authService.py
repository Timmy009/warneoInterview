import unittest

from app import create_app
from app.exception.CustomExceptions import CustomExceptions
from app.services.AuthService import AuthService
from app.utils.ErrorMessages import ErrorMessages
from app.utils.database import db


class UserServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and configure it
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the database
        db.create_all()

    def tearDown(self):
        # Remove the database and the app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        auth_service = AuthService()

        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
        response = auth_service.register_user(data)

        self.assertEqual(response[0]['message'], 'User registered successfully')
        self.assertEqual(response[1], 201)  # Check for status code 201 Created

        # Attempt to register the same user again (should raise CustomExceptions.USER_ALREADY_EXISTS)
        with self.assertRaises(CustomExceptions) as context:
            auth_service.register_user(data)

        self.assertEqual(context.exception.message, ErrorMessages.USER_ALREADY_EXISTS)

    def test_login_user(self):
        auth_service = AuthService()

        # Create a test user
        user_data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
        auth_service.register_user(user_data)

        # Attempt to login with correct credentials
        login_data = {'email': 'test@example.com', 'password': 'password123'}
        response = auth_service.login_user(login_data)

        self.assertIn('access_token', response[0])
        self.assertEqual(response[1], 200)  # Check for status code 200 OK

        # Attempt to login with incorrect password (should raise CustomExceptions.INVALID_CREDENTIALS)
        login_data['password'] = 'wrong_password'
        with self.assertRaises(CustomExceptions) as context:
            auth_service.login_user(login_data)

        self.assertEqual(context.exception.message, ErrorMessages.INVALID_CREDENTIALS)
        self.assertEqual(context.exception.status_code, 401)


if __name__ == '__main__':
    unittest.main()
