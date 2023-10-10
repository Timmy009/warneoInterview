import unittest
from app import create_app
from app.utils.database import db
from app.models.user_model import User
from app.services.UserService import UserService
from app.exception.CustomExceptions import CustomExceptions
from app.utils.ErrorMessages import ErrorMessages
from flask_jwt_extended import create_access_token


class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test Flask app and configure it
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the database
        db.create_all()

        # Create a test user for authentication
        test_user = User(name='test_user', email='test@example.com')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()

        # Get an access token for the test user
        self.access_token = create_access_token(identity=test_user.id)

    def tearDown(self):
        # Remove the database and the app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_with_valid_token(self):
        user_service = UserService()

        # Attempt to get the user with a valid access token
        with self.app.test_request_context(headers={'Authorization': f'Bearer {self.access_token}'}):
            response, status_code = user_service.get_user()

        self.assertEqual(status_code, 200)
        self.assertIn('user', response)

    def test_update_user_with_valid_token(self):
        user_service = UserService()

        # Attempt to update the user with a valid access token
        with self.app.test_request_context(headers={'Authorization': f'Bearer {self.access_token}'}):
            response, status_code = user_service.update_user(user_data={'name': 'new_name'})

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], ErrorMessages.USER_UPDATED_SUCCESSFULLY)

    def test_delete_user_with_valid_token(self):
        user_service = UserService()

        # Attempt to delete the user with a valid access token
        with self.app.test_request_context(headers={'Authorization': f'Bearer {self.access_token}'}):
            response, status_code = user_service.delete_user()

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], ErrorMessages.USER_DELETED_SUCCESSFULLY)


if __name__ == '__main__':
    unittest.main()
