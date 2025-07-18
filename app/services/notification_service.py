from app import db
from app.models.notification import Notification, DeviceToken, NotificationPreference
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import desc

class NotificationService:
    
    @staticmethod
    def create_notification(user_id, title, message, notification_type='info', data=None):
        """Create a new notification"""
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type,
                data=data
            )
            
            db.session.add(notification)
            db.session.commit()
            
            return notification, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_notifications(user_id, page=1, per_page=20, unread_only=False):
        """Get notifications for a specific user"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
            
            query = Notification.query.filter_by(user_id=user_id)
            
            if unread_only:
                query = query.filter_by(is_read=False)
            
            notifications = query.order_by(desc(Notification.created_at)).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return notifications, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def mark_notification_as_read(notification_id, user_id):
        """Mark a notification as read"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            notification = Notification.query.filter_by(
                id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                return None, "Notification not found"
            
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            
            db.session.commit()
            return notification, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def mark_all_notifications_as_read(user_id):
        """Mark all notifications as read for a user"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            notifications = Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).all()
            
            for notification in notifications:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
            
            db.session.commit()
            return len(notifications), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """Delete a notification"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user_id
            ).first()
            
            if not notification:
                return False, "Notification not found"
            
            db.session.delete(notification)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            count = Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).count()
            
            return count, None
        except Exception as e:
            return None, str(e)


class DeviceTokenService:
    
    @staticmethod
    def register_device_token(user_id, token, device_type, device_id=None, token_type='expo'):
        """Register or update a device token"""
        try:
            # Check if token already exists
            existing_token = DeviceToken.query.filter_by(token=token).first()
            
            if existing_token:
                # Update existing token
                existing_token.user_id = user_id
                existing_token.device_type = device_type
                existing_token.token_type = token_type
                existing_token.device_id = device_id
                existing_token.is_active = True
                existing_token.updated_at = datetime.utcnow()
            else:
                # Create new token
                device_token = DeviceToken(
                    user_id=user_id,
                    token=token,
                    device_type=device_type,
                    token_type=token_type,
                    device_id=device_id
                )
                db.session.add(device_token)
            
            db.session.commit()
            return existing_token or device_token, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_device_tokens(user_id, active_only=True):
        """Get all device tokens for a user"""
        try:
            # Convert user_id to integer if it's a string
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            query = DeviceToken.query.filter_by(user_id=user_id)
            
            if active_only:
                query = query.filter_by(is_active=True)
            
            tokens = query.all()
            return tokens, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def deactivate_device_token(token):
        """Deactivate a device token"""
        try:
            device_token = DeviceToken.query.filter_by(token=token).first()
            
            if not device_token:
                return None, "Device token not found"
            
            device_token.is_active = False
            db.session.commit()
            return device_token, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)


class NotificationPreferenceService:
    
    @staticmethod
    def get_user_preferences(user_id):
        """Get notification preferences for a user"""
        try:
            preferences = NotificationPreference.query.filter_by(user_id=user_id).first()
            
            if not preferences:
                # Create default preferences if none exist
                preferences = NotificationPreference(user_id=user_id)
                db.session.add(preferences)
                db.session.commit()
            
            return preferences, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_user_preferences(user_id, preferences_data):
        """Update notification preferences for a user"""
        try:
            preferences = NotificationPreference.query.filter_by(user_id=user_id).first()
            
            if not preferences:
                preferences = NotificationPreference(user_id=user_id)
                db.session.add(preferences)
            
            # Update fields if provided
            for field in ['push_enabled', 'email_enabled', 'marketing_enabled', 'news_enabled']:
                if field in preferences_data:
                    setattr(preferences, field, preferences_data[field])
            
            preferences.updated_at = datetime.utcnow()
            db.session.commit()
            return preferences, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)