import unittest
from flask_jwt_extended import create_access_token
from app import db
from app.models.books_model import Book
from app import create_app


class BookServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and configure it
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Set up the database
        db.create_all()

        # Create a test book
        test_book = Book(title='Test Book', author='Test Author')
        db.session.add(test_book)
        db.session.commit()

        # Get an access token (assuming authentication is required)
        self.access_token = create_access_token(identity='test_user_id')

    def tearDown(self):
        # Remove the database and the app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_book(self):
        # Test getting a single book
        response = self.client.get('/book/1', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('book', response.json)
        book_data = response.json['book']
        self.assertEqual(book_data['title'], 'Test Book')
        self.assertEqual(book_data['author'], 'Test Author')

    def test_get_nonexistent_book(self):
        # Test getting a book that does not exist
        response = self.client.get('/book/999', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        # self.assertEqual(response.json['error'], 'Book not found')

    def test_update_book(self):
        # Test updating a book
        data = {'title': 'Updated Title', 'author': 'Updated Author'}
        response = self.client.put('/book/1', json=data, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Book updated successfully')

        # Verify that the book has been updated in the database
        updated_book = Book.query.get(1)
        self.assertIsNotNone(updated_book)
        self.assertEqual(updated_book.title, 'Updated Title')
        self.assertEqual(updated_book.author, 'Updated Author')

    def test_update_nonexistent_book(self):
        # Test updating a book that does not exist
        data = {'title': 'Updated Title', 'author': 'Updated Author'}
        response = self.client.put('/book/999', json=data, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Book not found')

    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete('/book/1', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Book deleted successfully')

        # Verify that the book has been deleted from the database
        deleted_book = Book.query.get(1)
        self.assertIsNone(deleted_book)

    def test_delete_nonexistent_book(self):
        # Test deleting a book that does not exist
        response = self.client.delete('/book/999', headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Book not found')

    def test_list_books(self):
        # Add more books to the database
        additional_books = [
            {'title': 'Book 2', 'author': 'Author 2'},
            {'title': 'Book 3', 'author': 'Author 3'}
        ]

        for book_data in additional_books:
            new_book = Book(title=book_data['title'], author=book_data['author'])
            db.session.add(new_book)

        db.session.commit()

        # Test listing all books
        response = self.client.get('/books', headers={'Authorization': f'Bearer {self.access_token}'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.json)
        books_list = response.json['books']

        self.assertIsInstance(books_list, list)
        self.assertGreaterEqual(len(books_list), len(additional_books))  # At least the added books should be present

        # Check the details of the first book in the list
        first_book = books_list[0]
        self.assertIn('title', first_book)
        self.assertIn('author', first_book)

        # Optional: Check details of other books in the list if needed
        second_book = books_list[1]
        self.assertIn('title', second_book)
        self.assertIn('author', second_book)

        third_book = books_list[2]
        self.assertIn('title', third_book)
        self.assertIn('author', third_book)
        print(books_list)


if __name__ == '__main__':
    unittest.main()
