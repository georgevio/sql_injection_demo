import sqlite3
import logging
import os
from flask import g
from app import db
from models import User, LoginAttempt
from sqlalchemy import text
from datetime import datetime

# Database configuration
DATABASE = 'sql_injection_demo.db'

def is_using_postgresql():
    """Check if we're using PostgreSQL or SQLite"""
    return 'DATABASE_URL' in os.environ and os.environ.get('DATABASE_URL', '').startswith(('postgres://', 'postgresql://'))

def get_db_connection():
    """Create a connection to the SQLite database."""
    # Check if we're using PostgreSQL or SQLite
    if is_using_postgresql():
        # For PostgreSQL, we'll use SQLAlchemy instead of direct connection
        return None
    else:
        # For SQLite, use the original connection method
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Initialize the database with seed data."""
    # Check if we're using PostgreSQL or SQLite
    if is_using_postgresql():
        # For PostgreSQL, use SQLAlchemy ORM
        from app import db
        
        # Create all tables defined in models
        db.create_all()
        
        # Check if users exist; if not, insert sample data
        user_count = User.query.count()
        
        if user_count == 0:
            # Insert sample users
            users = [
                User(username='admin', password='securepassword123', email='admin@example.com', role='admin'),
                User(username='john', password='password123', email='john@example.com', role='user'),
                User(username='jane', password='jane123', email='jane@example.com', role='user'),
                User(username='bob', password='bob456', email='bob@example.com', role='user')
            ]
            
            for user in users:
                db.session.add(user)
            
            db.session.commit()
            logging.info("PostgreSQL database initialized with sample data")
    else:
        # For SQLite, use the original connection method
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create login_attempts table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            success BOOLEAN DEFAULT 0,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Check if users exist; if not, insert sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Insert some sample users
            users = [
                ('admin', 'securepassword123', 'admin@example.com', 'admin'),
                ('john', 'password123', 'john@example.com', 'user'),
                ('jane', 'jane123', 'jane@example.com', 'user'),
                ('bob', 'bob456', 'bob@example.com', 'user')
            ]
            
            cursor.executemany(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                users
            )
            
            logging.info("SQLite database initialized with sample data")
        
        conn.commit()
        conn.close()

# WARNING: This function is intentionally vulnerable to SQL injection for educational purposes
def execute_login_query(username, password):
    """
    Execute a raw SQL query for login.
    THIS FUNCTION IS INTENTIONALLY VULNERABLE TO SQL INJECTION!
    DO NOT USE THIS PATTERN IN PRODUCTION CODE!
    """
    # Vulnerable SQL query construction (DO NOT DO THIS IN REAL APPLICATIONS)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    logging.info(f"Executing query: {query}")
    
    # Check if we're using PostgreSQL or SQLite
    if is_using_postgresql():
        # For PostgreSQL, use SQLAlchemy with raw SQL
        try:
            # Execute raw SQL query (intentionally vulnerable)
            result = db.session.execute(text(query))
            user_data = result.fetchone()
            
            # Record the login attempt
            success = user_data is not None
            login_attempt = LoginAttempt(
                username=username,
                query=query,
                success=success,
                ip_address="127.0.0.1"
            )
            db.session.add(login_attempt)
            db.session.commit()
            
            # Convert user_data to dict if not None
            user_dict = None
            if user_data:
                user_dict = dict(zip(user_data.keys(), user_data))
            
            return {
                "user": user_dict,
                "query": query,
                "success": success
            }
        except Exception as e:
            logging.error(f"Database error: {e}")
            # Record the error in login attempts
            login_attempt = LoginAttempt(
                username=username,
                query=query,
                success=False,
                ip_address="127.0.0.1"
            )
            db.session.add(login_attempt)
            db.session.commit()
            
            return {
                "user": None,
                "query": query,
                "success": False,
                "error": str(e)
            }
    else:
        # For SQLite, use the original connection method
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            # Record the login attempt
            success = user is not None
            cursor.execute(
                "INSERT INTO login_attempts (username, query, success, ip_address) VALUES (?, ?, ?, ?)",
                (username, query, success, "127.0.0.1")
            )
            conn.commit()
            
            return {
                "user": dict(user) if user else None,
                "query": query,
                "success": success
            }
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            # Record the error in login attempts
            cursor.execute(
                "INSERT INTO login_attempts (username, query, success, ip_address) VALUES (?, ?, ?, ?)",
                (username, query, False, "127.0.0.1")
            )
            conn.commit()
            return {
                "user": None,
                "query": query,
                "success": False,
                "error": str(e)
            }
        finally:
            conn.close()

def get_login_attempts():
    """Get the 10 most recent login attempts."""
    # Check if we're using PostgreSQL or SQLite
    if is_using_postgresql():
        # For PostgreSQL, use SQLAlchemy
        attempts = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(10).all()
        return [
            {
                'id': attempt.id,
                'username': attempt.username,
                'query': attempt.query,
                'success': attempt.success,
                'ip_address': attempt.ip_address,
                'timestamp': attempt.timestamp
            } for attempt in attempts
        ]
    else:
        # For SQLite, use the original connection method
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM login_attempts 
        ORDER BY timestamp DESC
        LIMIT 10
        """)
        
        attempts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return attempts

def get_secure_login(username, password):
    """
    Secure way to perform login (for comparison).
    THIS DEMONSTRATES THE PROPER WAY TO HANDLE DATABASE QUERIES.
    """
    # Check if we're using PostgreSQL or SQLite
    if is_using_postgresql():
        # For PostgreSQL, use SQLAlchemy
        user = User.query.filter_by(username=username, password=password).first()
        
        return {
            "user": user.to_dict() if user else None,
            "success": user is not None
        }
    else:
        # For SQLite, use the original connection method
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Secure parameterized query
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
        return {
            "user": dict(user) if user else None,
            "success": user is not None
        }
