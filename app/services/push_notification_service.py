from exponent_server_sdk import PushClient, PushMessage, PushServerError, PushTicketError, DeviceNotRegisteredError
from app.services.notification_service import NotificationService, DeviceTokenService
from app.models.notification import DeviceToken
import firebase_admin
from firebase_admin import credentials, messaging
import json
import requests
import logging
import time
import os

logger = logging.getLogger(__name__)

class PushNotificationService:
    
    def __init__(self):
        self.expo_client = PushClient()
        self.firebase_app = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # You should place your service account key file in the project root
                # For now, we'll use a placeholder path
                service_account_path = os.path.join(os.path.dirname(__file__), '..', '..', 'firebase-service-account.json')
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    self.firebase_app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized successfully")
                else:
                    logger.warning("Firebase service account file not found. FCM notifications will not work.")
            else:
                self.firebase_app = firebase_admin.get_app()
                logger.info("Firebase Admin SDK already initialized")
        except Exception as e:
            logger.error(f"Error initializing Firebase Admin SDK: {e}")
            self.firebase_app = None
    
    def send_push_notification(self, user_id, title, message, data=None):
        """Send push notification to all user's devices"""
        try:
            # Get user's device tokens
            device_tokens, error = DeviceTokenService.get_user_device_tokens(user_id)
            
            if error:
                logger.error(f"Error getting device tokens for user {user_id}: {error}")
                return False, error
            
            if not device_tokens:
                logger.info(f"No device tokens found for user {user_id}")
                return True, "No device tokens found"
            
            # Create notification in database
            notification, error = NotificationService.create_notification(
                user_id, title, message, 'info', data
            )
            
            if error:
                logger.error(f"Error creating notification: {error}")
                return False, error
            
            # Send push notifications to all devices
            success_count = 0
            failure_count = 0
            
            for device_token in device_tokens:
                try:
                    if device_token.token_type == 'fcm':
                        # Send FCM notification
                        success = self._send_fcm_notification(
                            device_token.token, title, message, data
                        )
                    else:
                        # Send Expo notification (default)
                        success = self._send_expo_notification(
                            device_token.token, title, message, data
                        )
                    
                    if success:
                        success_count += 1
                        logger.info(f"Push notification sent successfully to {device_token.token} ({device_token.token_type})")
                    else:
                        failure_count += 1
                        
                except DeviceNotRegisteredError:
                    # Device token is no longer valid, deactivate it
                    DeviceTokenService.deactivate_device_token(device_token.token)
                    logger.warning(f"Device token {device_token.token} is no longer valid, deactivated")
                    
                except Exception as e:
                    failure_count += 1
                    logger.error(f"Unexpected error sending push to {device_token.token}: {e}")
            
            result_message = f"Sent to {success_count} devices, failed for {failure_count} devices"
            return True, result_message
            
        except Exception as e:
            logger.error(f"Error in send_push_notification: {e}")
            return False, str(e)
    
    def _send_expo_notification(self, token, title, message, data=None):
        """Send Expo push notification"""
        try:
            push_message = PushMessage(
                to=token,
                title=title,
                body=message,
                data=data or {},
                sound='default',
                badge=1
            )
            
            response = self.expo_client.publish(push_message)
            return True
            
        except DeviceNotRegisteredError:
            DeviceTokenService.deactivate_device_token(token)
            logger.warning(f"Expo token {token} is no longer valid, deactivated")
            return False
            
        except PushServerError as e:
            logger.error(f"Expo push server error for token {token}: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error sending Expo push to token {token}: {e}")
            return False
    
    def _send_fcm_notification(self, token, title, message, data=None):
        """Send FCM push notification"""
        if not self.firebase_app:
            logger.error("Firebase Admin SDK not initialized")
            return False
            
        try:
            # Create FCM message
            fcm_message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                data=data or {},
                token=token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default',
                        channel_id='default',
                    ),
                ),
            )
            
            # Send message
            response = messaging.send(fcm_message)
            logger.info(f"FCM message sent successfully: {response}")
            return True
            
        except messaging.UnregisteredError:
            DeviceTokenService.deactivate_device_token(token)
            logger.warning(f"FCM token {token} is no longer valid, deactivated")
            return False
            
        except Exception as e:
            logger.error(f"Error sending FCM notification to token {token}: {e}")
            return False
    
    def send_push_notification_to_token(self, token, title, message, data=None, token_type='expo'):
        """Send push notification to a specific device token"""
        try:
            if token_type == 'fcm':
                success = self._send_fcm_notification(token, title, message, data)
            else:
                success = self._send_expo_notification(token, title, message, data)
            
            if success:
                logger.info(f"Push notification sent successfully to token {token} ({token_type})")
                return True, "Push notification sent successfully"
            else:
                return False, "Failed to send push notification"
            
        except Exception as e:
            logger.error(f"Unexpected error sending push to token {token}: {e}")
            return False, str(e)
    
    def send_bulk_push_notifications(self, notifications_data):
        """Send push notifications to multiple users"""
        try:
            results = []
            
            for notification_data in notifications_data:
                user_id = notification_data.get('user_id')
                title = notification_data.get('title')
                message = notification_data.get('message')
                data = notification_data.get('data')
                
                if not user_id or not title or not message:
                    results.append({
                        'user_id': user_id,
                        'success': False,
                        'error': 'Missing required fields'
                    })
                    continue
                
                success, error = self.send_push_notification(user_id, title, message, data)
                results.append({
                    'user_id': user_id,
                    'success': success,
                    'message': error
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in send_bulk_push_notifications: {e}")
            return []
    
    def verify_token(self, token, token_type='expo'):
        """Verify if a push token is valid"""
        try:
            if token_type == 'expo':
                # Expo tokens should start with ExponentPushToken
                if not token.startswith('ExponentPushToken'):
                    return False, "Invalid Expo token format"
                return True, "Expo token is valid"
            elif token_type == 'fcm':
                # FCM tokens are typically longer and contain specific characters
                if len(token) < 100:  # FCM tokens are usually much longer
                    return False, "Invalid FCM token format"
                return True, "FCM token is valid"
            else:
                return False, "Unknown token type"
            
        except Exception as e:
            logger.error(f"Error verifying token {token}: {e}")
            return False, str(e)
    
    def verify_expo_token(self, token):
        """Verify if an Expo push token is valid (legacy method)"""
        return self.verify_token(token, 'expo')
    
    def get_push_receipts(self, receipt_ids):
        """Get push notification receipts from Expo"""
        try:
            receipts = self.client.get_push_receipts(receipt_ids)
            return receipts
            
        except Exception as e:
            logger.error(f"Error getting push receipts: {e}")
            return {}
    
    def send_test_notification(self, user_id):
        """Send a test notification to a user"""
        try:
            title = "Test Notification"
            message = "This is a test push notification from your app!"
            data = {
                "type": "test",
                "timestamp": str(int(time.time()))
            }
            
            return self.send_push_notification(user_id, title, message, data)
            
        except Exception as e:
            logger.error(f"Error sending test notification: {e}")
            return False, str(e)

# Create a singleton instance
push_service = PushNotificationService()