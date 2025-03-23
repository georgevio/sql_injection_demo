"""
SQL Injection Demo - Database Initializer
This script sets up the initial database with sample data
"""

import os
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database file
DB_FILE = 'sql_injection_demo.db'

def init_database():
    """Initialize the SQLite database with tables and sample data."""
    # Check if database file already exists
    db_exists = os.path.exists(DB_FILE)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Create users table
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
        
        # Create login_attempts table
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
        
        # Insert sample data if this is a new database
        if not db_exists:
            # Sample users
            sample_users = [
                ('admin', 'securepassword123', 'admin@example.com', 'admin'),
                ('john', 'password123', 'john@example.com', 'user'),
                ('jane', 'jane123', 'jane@example.com', 'user'),
                ('bob', 'bob456', 'bob@example.com', 'user')
            ]
            
            cursor.executemany(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                sample_users
            )
            
            logging.info(f"Inserted {len(sample_users)} sample users into the database")
        
        # Commit changes
        conn.commit()
        logging.info("Database initialization complete")
        
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    logging.info("Initializing SQL Injection Demo database...")
    init_database()
    logging.info("Database setup complete")
