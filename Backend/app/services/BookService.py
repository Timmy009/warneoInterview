
from app.utils.database import db
from app.models.books_model import Book
from app.exception.CustomExceptions import CustomExceptions
from app.services.BookServiceInterface import BookServiceInterface
from app.utils.ErrorMessages import ErrorMessages


class BookService(BookServiceInterface):
    def add_book(self, data):
        new_book = Book(title=data['title'], author=data['author'])
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully'}

    def get_book(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return {'book': {'title': book.title, 'author': book.author}}, 200
        else:
            raise CustomExceptions(ErrorMessages.BOOK_NOT_FOUND)

    def update_book(self, book_id, data):
        book = Book.query.get(book_id)
        if book:
            # Update book data
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)

            # Commit changes to the database
            db.session.commit()

            return {'message': ErrorMessages.BOOK_UPDATED_SUCCESSFULLY}, 200
        else:
            raise CustomExceptions(ErrorMessages.BOOK_NOT_FOUND)

    def delete_book(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': ErrorMessages.BOOK_DELETED_SUCCESSFULLY}, 200
        else:
            raise CustomExceptions(ErrorMessages.BOOK_NOT_FOUND)

    def list_books(self):
        books = Book.query.all()
        book_list = [{'title': book.title, 'author': book.author} for book in books]
        return {'books': book_list}
