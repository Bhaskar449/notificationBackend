from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = UserService.get_all_users(page, per_page)
        
        return jsonify({
            'message': 'Users retrieved successfully',
            'data': {
                'users': [user.to_dict() for user in users.items],
                'pagination': {
                    'page': users.page,
                    'pages': users.pages,
                    'per_page': users.per_page,
                    'total': users.total,
                    'has_next': users.has_next,
                    'has_prev': users.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'User retrieved successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400
        
        user, error = UserService.create_user(data)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User created successfully',
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user, error = UserService.update_user(user_id, data)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User updated successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user"""
    try:
        success, error = UserService.delete_user(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_user(user_id):
    """Deactivate user"""
    try:
        user, error = UserService.deactivate_user(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User deactivated successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 