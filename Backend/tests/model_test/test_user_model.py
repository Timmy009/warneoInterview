import unittest
from app import create_app
from app.utils.database import db
from app.security.password import bcrypt
from app.models.user_model import User

class UserModelTestCase(unittest.TestCase):

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

    def test_password_hashing(self):
        # Test if the password is hashed and verified correctly
        user = User(name='test_user', email='test@example.com')
        user.set_password('password123')

        self.assertTrue(bcrypt.check_password_hash(user.password, 'password123'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'wrong_password'))

    def test_repr_method(self):
        # Test if the __repr__ method returns the expected string
        user = User(name='test_user', email='test@example.com')
        repr_string = repr(user)
        print(repr_string)
        self.assertIn('User', repr_string)
        self.assertIn('test_user', repr_string)
        self.assertIn('test@example.com', repr_string)

    def test_check_password_method(self):
        # Test if the check_password method works as expected
        user = User(name='test_user', email='test@example.com')
        user.set_password('password123')

        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrong_password'))

    def test_create_user(self):
        # Test creating a new user
        user_data = {'name': 'new_user', 'email': 'new_user@example.com', 'password': 'new_password'}
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()

        # Verify that the user is in the database
        retrieved_user = User.query.filter_by(email='new_user@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, 'new_user')

    def test_update_user(self):
        # Test updating user information
        user = User(name='test_user', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Modify user information
        user.name = 'updated_user'
        db.session.commit()

        # Verify that the user information is updated
        updated_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.name, 'updated_user')

    def test_delete_user(self):
        # Test deleting a user
        user = User(name='test_user', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Verify that the user is deleted
        deleted_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()
