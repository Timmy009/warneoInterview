from flask import Blueprint, request
from flask_restful import Resource, Api
from app.exception.CustomExceptions import CustomExceptions
from app.exception.UserExceptionHandler import UserExceptionHandler
from app.services.AuthService import AuthService

auth_bp = Blueprint('auth', __name__)

api = Api(auth_bp)
user_service = AuthService()


class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response, status_code = user_service.register_user(data)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            response, status_code = user_service.login_user(data)
            return response, status_code
        except CustomExceptions as e:
            return UserExceptionHandler.handle_exception(e)



api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

