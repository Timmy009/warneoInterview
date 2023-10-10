from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.security.password import bcrypt
from app.utils.database import db
from app.exception.CustomExceptions import CustomExceptions
from app.models.user_model import User
from app.services.AuthServiceInterface import AuthServiceInterface
from app.utils.ErrorMessages import ErrorMessages


class AuthService(AuthServiceInterface):
    def register_user(self, data):
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise CustomExceptions(ErrorMessages.USER_ALREADY_EXISTS)

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201  # 201 Created

    def login_user(self, data):
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200  # 200 OK
        else:
            # In UserService.login_user method
            raise CustomExceptions(ErrorMessages.INVALID_CREDENTIALS, status_code=401)

