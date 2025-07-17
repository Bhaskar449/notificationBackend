#!/usr/bin/env python3
"""
Database setup script for Flask application
Run this script to initialize the database and create all tables
"""

from app import create_app, db
from app.models import User
import os

def init_database():
    """Initialize the database and create all tables"""
    # Create the Flask application
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Optionally create a default admin user
        create_admin = input("Do you want to create an admin user? (y/n): ").lower()
        if create_admin == 'y':
            username = input("Enter admin username: ")
            email = input("Enter admin email: ")
            password = input("Enter admin password: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print("❌ User already exists!")
                return
            
            # Create admin user
            admin_user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"✅ Admin user '{username}' created successfully!")

if __name__ == "__main__":
    print("🚀 Initializing database...")
    init_database()
    print("✅ Database initialization complete!") 