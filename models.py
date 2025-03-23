from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)  # Intentionally not hashed for demo
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
        
    def to_dict(self):
        """Convert user object to dictionary for serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,  # Included for demo purposes only - never do this in real apps!
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }

class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    query = db.Column(db.Text)
    success = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LoginAttempt {self.username} {self.success}>'
        
    def to_dict(self):
        """Convert login attempt object to dictionary for serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'query': self.query,
            'success': self.success,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp
        }
