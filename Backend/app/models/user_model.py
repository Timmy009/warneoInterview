from app.security.password import bcrypt
from app.utils.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            # ... other fields you want to include ...
        }
