import unittest
from app import create_app
from app.utils.database import db
from app.models.books_model import Book
from app.services.BookService import BookService
from app.exception.CustomExceptions import CustomExceptions
from app.utils.ErrorMessages import ErrorMessages


class BookServiceTestCase(unittest.TestCase):

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

    def test_add_book(self):
        book_service = BookService()

        data = {'title': 'Test Book', 'author': 'Test Author'}
        response = book_service.add_book(data)

        self.assertEqual(response['message'], 'Book added successfully')

    def test_get_book(self):
        book_service = BookService()

        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = book_service.get_book(book.id)

        expected_result = {'book': {'title': 'Test Book', 'author': 'Test Author'}}
        self.assertEqual(response, (expected_result, 200))

        with self.assertRaises(CustomExceptions) as context:
            book_service.get_book(999)  # Non-existent book

        self.assertEqual(context.exception.message, ErrorMessages.BOOK_NOT_FOUND)

    def test_update_book(self):
        book_service = BookService()

        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        data = {'title': 'Updated Book Title', 'author': 'Updated Author'}
        response = book_service.update_book(book.id, data)

        self.assertEqual(response[0]['message'], ErrorMessages.BOOK_UPDATED_SUCCESSFULLY)

    def test_delete_book(self):
        book_service = BookService()

        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = book_service.delete_book(book.id)

        self.assertEqual(response[0]['message'], ErrorMessages.BOOK_DELETED_SUCCESSFULLY)

    def test_list_books(self):
        book_service = BookService()

        books = [
            {'title': 'Book 1', 'author': 'Author 1'},
            {'title': 'Book 2', 'author': 'Author 2'},
            # Add more books as needed
        ]

        for book_data in books:
            new_book = Book(title=book_data['title'], author=book_data['author'])
            db.session.add(new_book)
            db.session.commit()

        response = book_service.list_books()

        # Check that each expected book is present in the result
        for expected_book in books:
            self.assertIn(expected_book, response['books'])


if __name__ == '__main__':
    unittest.main()
