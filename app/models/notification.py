from datetime import datetime
from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'info', 'success', 'warning', 'error'
    is_read = db.Column(db.Boolean, default=False)
    data = db.Column(db.JSON, nullable=True)  # Additional data for deep linking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship
    user = db.relationship('User', backref='notifications')
    
    def to_dict(self):
        """Convert notification object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    def __repr__(self):
        return f'<Notification {self.title}>'


class DeviceToken(db.Model):
    __tablename__ = 'device_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True)
    device_type = db.Column(db.String(20), nullable=False)  # 'ios', 'android'
    device_id = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='device_tokens')
    
    def to_dict(self):
        """Convert device token object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'device_type': self.device_type,
            'device_id': self.device_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DeviceToken {self.device_type}>'


class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    push_enabled = db.Column(db.Boolean, default=True)
    email_enabled = db.Column(db.Boolean, default=True)
    marketing_enabled = db.Column(db.Boolean, default=True)
    news_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='notification_preferences')
    
    def to_dict(self):
        """Convert notification preference object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'push_enabled': self.push_enabled,
            'email_enabled': self.email_enabled,
            'marketing_enabled': self.marketing_enabled,
            'news_enabled': self.news_enabled,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<NotificationPreference {self.user_id}>'