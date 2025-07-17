from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.services.user_service import UserService
from datetime import timedelta

class AuthService:
    
    @staticmethod
    def authenticate_user(username_or_email, password):
        """Authenticate user with username/email and password"""
        # Try to find user by username first, then by email
        user = UserService.get_user_by_username(username_or_email)
        if not user:
            user = UserService.get_user_by_email(username_or_email)
        
        if user and user.check_password(password) and user.is_active:
            return user
        return None
    
    @staticmethod
    def generate_tokens(user):
        """Generate access and refresh tokens for authenticated user"""
        try:
            access_token = create_access_token(
                identity=str(user.id),  # Convert to string
                expires_delta=timedelta(hours=24)  # Extended for development
            )
            refresh_token = create_refresh_token(
                identity=str(user.id),  # Convert to string
                expires_delta=timedelta(days=7)   # Extended for development
            )
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            print(f"Token generation error: {e}")
            # Fallback - simple token without expiration for development
            return {
                'access_token': f"dev_token_{user.id}_{user.username}",
                'refresh_token': f"dev_refresh_{user.id}_{user.username}"
            }
    
    @staticmethod
    def login(username_or_email, password):
        """Login user and return tokens"""
        user = AuthService.authenticate_user(username_or_email, password)
        if not user:
            return None, "Invalid credentials"
        
        tokens = AuthService.generate_tokens(user)
        return {
            'user': user.to_dict(),
            'tokens': tokens
        }, None
    
    @staticmethod
    def register(user_data):
        """Register new user"""
        # Check if username or email already exists
        if UserService.get_user_by_username(user_data['username']):
            return None, "Username already exists"
        
        if UserService.get_user_by_email(user_data['email']):
            return None, "Email already exists"
        
        # Create new user
        user, error = UserService.create_user(user_data)
        if error:
            return None, error
        
        # Generate tokens for new user
        tokens = AuthService.generate_tokens(user)
        return {
            'user': user.to_dict(),
            'tokens': tokens
        }, None
    
    @staticmethod
    def refresh_token(user_id):
        """Generate new access token using refresh token"""
        user = UserService.get_user_by_id(user_id)
        if not user or not user.is_active:
            return None, "User not found or inactive"
        
        try:
            access_token = create_access_token(
                identity=str(user.id),  # Convert to string
                expires_delta=timedelta(hours=24)
            )
            return {'access_token': access_token}, None
        except Exception as e:
            print(f"Token refresh error: {e}")
            # Fallback for development
            return {
                'access_token': f"dev_token_{user.id}_{user.username}"
            }, None 