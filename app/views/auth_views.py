from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username_or_email') or not data.get('password'):
            return jsonify({'error': 'Username/email and password are required'}), 400
        
        result, error = AuthService.login(
            data['username_or_email'],
            data['password']
        )
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Login successful',
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register endpoint"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400
        
        result, error = AuthService.register(data)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Registration successful',
            'data': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh token endpoint"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string back to integer for database query
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        result, error = AuthService.refresh_token(user_id)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string back to integer for database query
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        from app.services.user_service import UserService
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile retrieved successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 