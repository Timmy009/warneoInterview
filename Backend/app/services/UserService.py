from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.IUserService import IUserService
from app.utils.database import db
from app.exception.CustomExceptions import CustomExceptions
from app.models.user_model import User
from app.utils.ErrorMessages import ErrorMessages


# ... (your existing imports)

class UserService(IUserService):
    @jwt_required()
    def get_user(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            raise CustomExceptions(ErrorMessages.USER_NOT_FOUND, status_code=404)

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            # Add other user data fields as needed
        }

        return {'user': user_data}, 200

    @jwt_required()
    def update_user(self, user_data):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            raise CustomExceptions(ErrorMessages.USER_NOT_FOUND, status_code=404)

    # Update user fields based on user_data
        for key, value in user_data.items():
            setattr(user, key, value)

        db.session.commit()

        return {'message': ErrorMessages.USER_UPDATED_SUCCESSFULLY}, 200

    @jwt_required()
    def delete_user(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            raise CustomExceptions(ErrorMessages.USER_NOT_FOUND, status_code=404)

        db.session.delete(user)
        db.session.commit()

        return {'message': ErrorMessages.USER_DELETED_SUCCESSFULLY}, 200
