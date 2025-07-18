from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService, DeviceTokenService, NotificationPreferenceService
from app.services.push_notification_service import push_service

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get notifications for current user"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        unread_only = request.args.get('unread_only', False, type=bool)
        
        notifications, error = NotificationService.get_user_notifications(
            user_id, page, per_page, unread_only
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Notifications retrieved successfully',
            'data': {
                'notifications': [notification.to_dict() for notification in notifications.items],
                'pagination': {
                    'page': notifications.page,
                    'pages': notifications.pages,
                    'per_page': notifications.per_page,
                    'total': notifications.total,
                    'has_next': notifications.has_next,
                    'has_prev': notifications.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    """Create a new notification"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'message']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Title and message are required'}), 400
        
        user_id = data.get('user_id') or get_jwt_identity()
        notification_type = data.get('type', 'info')
        notification_data = data.get('data')
        
        notification, error = NotificationService.create_notification(
            user_id, data['title'], data['message'], notification_type, notification_data
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Notification created successfully',
            'data': notification.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>/read', methods=['PATCH'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        user_id = get_jwt_identity()
        
        notification, error = NotificationService.mark_notification_as_read(
            notification_id, user_id
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Notification marked as read',
            'data': notification.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/read-all', methods=['PATCH'])
@jwt_required()
def mark_all_notifications_read():
    """Mark all notifications as read for current user"""
    try:
        user_id = get_jwt_identity()
        
        count, error = NotificationService.mark_all_notifications_as_read(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': f'{count} notifications marked as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = get_jwt_identity()
        
        success, error = NotificationService.delete_notification(notification_id, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Notification deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications for current user"""
    try:
        user_id = get_jwt_identity()
        
        count, error = NotificationService.get_unread_count(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Unread count retrieved successfully',
            'data': {'unread_count': count}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/device-tokens', methods=['POST'])
@jwt_required()
def register_device_token():
    """Register a device token for push notifications"""
    try:
        data = request.get_json()
        
        required_fields = ['token', 'device_type']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Token and device_type are required'}), 400
        
        user_id = get_jwt_identity()
        device_id = data.get('device_id')
        token_type = data.get('token_type', 'expo')  # Default to 'expo' for backward compatibility
        
        if data['device_type'] not in ['ios', 'android']:
            return jsonify({'error': 'Device type must be ios or android'}), 400
        
        if token_type not in ['expo', 'fcm']:
            return jsonify({'error': 'Token type must be expo or fcm'}), 400
        
        device_token, error = DeviceTokenService.register_device_token(
            user_id, data['token'], data['device_type'], device_id, token_type
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Device token registered successfully',
            'data': device_token.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/device-tokens', methods=['GET'])
@jwt_required()
def get_device_tokens():
    """Get device tokens for current user"""
    try:
        user_id = get_jwt_identity()
        
        tokens, error = DeviceTokenService.get_user_device_tokens(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Device tokens retrieved successfully',
            'data': [token.to_dict() for token in tokens]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/device-tokens/<token>', methods=['DELETE'])
@jwt_required()
def deactivate_device_token(token):
    """Deactivate a device token"""
    try:
        device_token, error = DeviceTokenService.deactivate_device_token(token)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Device token deactivated successfully',
            'data': device_token.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get notification preferences for current user"""
    try:
        user_id = get_jwt_identity()
        
        preferences, error = NotificationPreferenceService.get_user_preferences(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Notification preferences retrieved successfully',
            'data': preferences.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    """Update notification preferences for current user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = get_jwt_identity()
        
        preferences, error = NotificationPreferenceService.update_user_preferences(
            user_id, data
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Notification preferences updated successfully',
            'data': preferences.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/push', methods=['POST'])
@jwt_required()
def send_push_notification():
    """Send a push notification to a user"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'message']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Title and message are required'}), 400
        
        user_id = data.get('user_id') or get_jwt_identity()
        notification_data = data.get('data')
        
        success, result = push_service.send_push_notification(
            user_id, data['title'], data['message'], notification_data
        )
        
        if not success:
            return jsonify({'error': result}), 400
        
        return jsonify({
            'message': 'Push notification sent successfully',
            'data': {'result': result}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/push/test', methods=['POST'])
@jwt_required()
def send_test_push():
    """Send a test push notification to current user"""
    try:
        user_id = get_jwt_identity()
        
        success, result = push_service.send_test_notification(user_id)
        
        if not success:
            return jsonify({'error': result}), 400
        
        return jsonify({
            'message': 'Test push notification sent successfully',
            'data': {'result': result}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/push/bulk', methods=['POST'])
@jwt_required()
def send_bulk_push_notifications():
    """Send push notifications to multiple users"""
    try:
        data = request.get_json()
        
        if not data or 'notifications' not in data:
            return jsonify({'error': 'Notifications array is required'}), 400
        
        results = push_service.send_bulk_push_notifications(data['notifications'])
        
        return jsonify({
            'message': 'Bulk push notifications processed',
            'data': {'results': results}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500