from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import jwt
import os

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def hash_password(password: str) -> str:
        # Hash a password with a generated salt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def generate_salt() -> str:
        # Generate a new salt
        return bcrypt.gensalt().decode('utf-8')

    @staticmethod
    def hash_with_salt(password: str, salt: str) -> str:
        # Hash a password using a provided salt
        return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

    def set_password(self, password: str):
        self.password_hash = self.hash_password(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_jwt(self, expires_in=3600):
        """
        Generate a JWT token for the user.
        :param expires_in: Expiration time in seconds (default: 1 hour)
        :return: JWT token as string
        """
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow().timestamp() + expires_in
        }
        secret = os.getenv('SECRET_KEY', 'dev-secret-key')
        token = jwt.encode(payload, secret, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    @staticmethod
    def validate_jwt(token):
        """
        Validate a JWT token and return the payload if valid, else None.
        :param token: JWT token as string
        :return: payload dict or None
        """
        secret = os.getenv('SECRET_KEY', 'dev-secret-key')
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
