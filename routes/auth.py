from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.database import User
from utils.helpers import validate_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password') or not data.get('role'):
            return jsonify({'error': 'Email, password, and role are required'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if data['role'] not in ['student', 'company', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Create user
        from flask import current_app
        db = current_app.config['db']
        user_id, error = User.create(db, data['email'], data['password'], data['role'])
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': str(user_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate
        from flask import current_app
        db = current_app.config['db']
        user = User.authenticate(db, data['email'], data['password'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=str(user['_id']),
            additional_claims={'role': user['role']}
        )
        
        return jsonify({
            'token': access_token,
            'role': user['role'],
            'user_id': str(user['_id'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        user_id = get_jwt_identity()
        
        from flask import current_app
        db = current_app.config['db']
        user = User.get_by_id(db, user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user['role']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
