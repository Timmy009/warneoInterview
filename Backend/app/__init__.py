from flask import Flask
from flask_cors import CORS

from app.security.password import bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.utils.config import Config
from app.route.AuthRoute import RegisterResource, LoginResource, auth_bp
from app.route.UserResources import UserResource
from app.route.books_bp import BookResource, BooksListResource, AddBookResource
from app.utils.database import db

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "http://192.168.x.x:19006"}})

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    # Register authentication routes
    app.register_blueprint(auth_bp)
    api.add_resource(RegisterResource, '/auth/register')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(UserResource, '/user')

    api.add_resource(BookResource, '/book/<int:book_id>')
    api.add_resource(BooksListResource, '/books')
    api.add_resource(AddBookResource, '/book/add')

    return app
