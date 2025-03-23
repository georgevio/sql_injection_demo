import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")  # Never use this in production

# Configure database - use PostgreSQL if DATABASE_URL is set, otherwise use SQLite
database_url = os.environ.get("DATABASE_URL", "sqlite:///sql_injection_demo.db")
# Fix for PostgreSQL URLs starting with "postgres://" instead of "postgresql://"
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes after app initialization to avoid circular imports
from routes import *

# Create database tables
with app.app_context():
    db.create_all()
