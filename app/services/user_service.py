from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class UserService:
    
    @staticmethod
    def create_user(user_data):
        """Create a new user"""
        try:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.set_password(user_data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            return user, None
        except IntegrityError as e:
            db.session.rollback()
            return None, "Username or email already exists"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """Get all users with pagination"""
        return User.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
    
    @staticmethod
    def update_user(user_id, user_data):
        """Update user information"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "User not found"
            
            # Update fields if provided
            for field in ['username', 'email', 'first_name', 'last_name']:
                if field in user_data:
                    setattr(user, field, user_data[field])
            
            if 'password' in user_data:
                user.set_password(user_data['password'])
            
            db.session.commit()
            return user, None
        except IntegrityError as e:
            db.session.rollback()
            return None, "Username or email already exists"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_user(user_id):
        """Delete user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate user instead of deleting"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "User not found"
            
            user.is_active = False
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e) 