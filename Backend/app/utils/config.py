import secrets

from app import bcrypt


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:09024943627@localhost/db_interview'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(32)
    Testing = True


def generate_hashed_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
