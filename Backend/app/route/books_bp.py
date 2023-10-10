from flask import Blueprint, request
from flask_restful import Resource, Api
from app.exception.CustomExceptions import CustomExceptions
from app.exception.UserExceptionHandler import UserExceptionHandler
from app.services.BookService import BookService

book_bp = Blueprint('book', __name__)
api = Api(book_bp)
book_service = BookService()


class BookResource(Resource):
    def get(self, book_id):
        try:
            response, status_code = book_service.get_book(book_id)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)

    def put(self, book_id):
        try:
            data = request.get_json()
            response, status_code = book_service.update_book(book_id, data)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)

    def delete(self, book_id):
        try:
            response, status_code = book_service.delete_book(book_id)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)


class BooksListResource(Resource):
    def get(self):
        response = book_service.list_books()
        return response


class AddBookResource(Resource):
        def post(self):
            try:
                data = request.get_json()
                response, status_code = book_service.add_book(data)
                return response, status_code
            except CustomExceptions as e:
                return UserExceptionHandler.handle_exception(e)



api.add_resource(BookResource, '/book/<int:book_id>')
api.add_resource(BooksListResource, '/books')
api.add_resource(AddBookResource, '/book/add')
