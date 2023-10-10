from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.UserService import UserService
from app.exception.CustomExceptions import CustomExceptions
from app.exception.UserExceptionHandler import UserExceptionHandler

user_bp = Blueprint('user', __name__)
api = Api(user_bp)
user_service = UserService()


class UserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            response, status_code = user_service.get_user()
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)

    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            response, status_code = user_service.update_user(data)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)

    @jwt_required()
    def delete(self):
        try:
            response, status_code = user_service.delete_user()
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)


api.add_resource(UserResource, '/user')
