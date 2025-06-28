from flask import Blueprint, request, jsonify
import re

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@auth_bp.route('/register', methods=['POST'])
def register():
    from app import db
    from models.user import User
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate email format
    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email address.'}), 400

    # Validate password
    if not password or len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters.'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 409

    # Create new user
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Generate JWT token
    token = user.generate_jwt()
    return jsonify({'message': 'User registered successfully.', 'token': token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from app import db
    from models.user import User
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    token = user.generate_jwt()
    return jsonify({'message': 'Login successful.', 'token': token}), 200
