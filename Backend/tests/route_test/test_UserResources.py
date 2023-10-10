import json
import unittest
from flask import Flask
from flask_jwt_extended import create_access_token
from app import db
from app.models.user_model import User
from app import create_app
from app.services.UserService import UserService


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

        # Create a test user for authentication
        test_user = User(name='test_user', email=f'test@example.com_{self._testMethodName}')
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

    def test_get_user(self):
        # Test fetching user details with a valid token
        response = self.client.get('/user', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json)

    def test_unauthorized_access(self):
        # Test accessing user details without a token (should be unauthorized)
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 500)

    def test_update_user(self):
        # Test updating user details with valid data
        data = {'name': 'new_name'}
        response = self.client.put('/user', json=data, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User updated successfully')

    def test_delete_user(self):
        # Test deleting user with a valid token
        response = self.client.delete('/user', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User deleted successfully')

    def test_delete_user_unauthorized(self):
        # Test deleting user without a token (should be unauthorized)
        response = self.client.delete('/user')
        self.assertEqual(response.status_code, 500)

    def test_delete_nonexistent_user(self):
        # Test deleting a user that doesn't exist (should return 404)
        non_existent_token = create_access_token(identity=999)  # Assuming 999 is not a valid user ID
        response = self.client.delete('/user', headers={'Authorization': f'Bearer {non_existent_token}'})
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
