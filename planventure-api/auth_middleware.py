from functools import wraps
from flask import request, jsonify

def token_required(f):
    from models.user import User
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is expected in the Authorization header as 'Bearer <token>'
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        payload = User.validate_jwt(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired!'}), 401
        # Optionally, attach user info to request context
        request.user = payload
        return f(*args, **kwargs)
    return decorated
