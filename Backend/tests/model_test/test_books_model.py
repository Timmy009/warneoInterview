import unittest
from app.app import create_app
from app.utils.database import db
from app.models.books_model import Book


class BookModelTestCase(unittest.TestCase):

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

    def test_create_book(self):
        # Test creating a new book
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()
        print(book)
        self.assertIsNotNone(book.id)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')

    def test_read_book(self):
        # Test reading an existing book
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        retrieved_book = Book.query.get(book.id)

        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book.title, 'Test Book')
        self.assertEqual(retrieved_book.author, 'Test Author')

    def test_update_book(self):
        # Test updating an existing book
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        book.title = 'Updated Book Title'
        book.author = 'Updated Author'
        db.session.commit()

        updated_book = Book.query.get(book.id)

        self.assertEqual(updated_book.title, 'Updated Book Title')
        self.assertEqual(updated_book.author, 'Updated Author')

    def test_delete_book(self):
        # Test deleting an existing book
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        db.session.delete(book)
        db.session.commit()

        deleted_book = Book.query.get(book.id)

        self.assertIsNone(deleted_book)

    def test_repr_method(self):
        # Test if the __repr__ method returns the expected string
        book = Book(title='Test Book', author='Test Author')
        repr_string = repr(book)

        self.assertIn('Book', repr_string)
        self.assertIn('Test Book', repr_string)
        self.assertIn('Test Author', repr_string)

if __name__ == '__main__':
    unittest.main()
