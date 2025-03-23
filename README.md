# SQL Injection Demo Application

## Introduction

This educational web application demonstrates SQL injection vulnerabilities commonly found in web applications. It is designed for university students and cybersecurity enthusiasts to learn about SQL injection attacks in a safe, controlled environment.

## Purpose

SQL injection remains one of the most dangerous web application security flaws. This application intentionally contains vulnerable code to help students:

- Understand how SQL injection attacks work
- Learn to identify vulnerable code patterns
- Practice exploitation techniques safely
- Compare vulnerable code with secure alternatives
- Develop secure coding habits

## Warning

**This application contains intentional security vulnerabilities for educational purposes only.**

- Do not use this code in production environments
- Do not deploy this application to public-facing servers
- Only run this application in controlled, educational settings

## Features

1. **Vulnerable Login Form:** Demonstrates classic SQL injection through authentication bypass
2. **Admin Panel:** Shows executed queries and login attempts
3. **Dual Database Support:** Works with both SQLite (local development) and PostgreSQL (Docker)
4. **Interactive Examples:** Pre-configured SQL injection payloads
5. **Secure vs. Insecure Code:** Side-by-side comparison of vulnerable and secure implementations

## Getting Started

### Option 1: Running with Docker (Recommended)

#### PostgreSQL Mode (Full Setup)

1. Ensure Docker and Docker Compose are installed on your system
2. Clone or download this repository
3. Open a terminal and navigate to the project directory
4. Run the application with PostgreSQL:
   ```bash
   docker-compose up --build
   ```
5. Access the application at: http://localhost:5000

#### SQLite Mode (Simplified Setup)

If you prefer a simpler setup without a separate database container:

1. Ensure Docker and Docker Compose are installed on your system
2. Clone or download this repository
3. Open a terminal and navigate to the project directory
4. Run the application with SQLite:
   ```bash
   docker-compose -f docker-compose.sqlite.yml up --build
   ```
5. Access the application at: http://localhost:5000

### Option 2: Running Locally (Development)

1. Ensure Python 3.8+ is installed
2. Clone or download this repository
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r docker-requirements.txt
   ```
5. Initialize the SQLite database:
   ```bash
   python init_db.py
   ```
6. Run the application:
   ```bash
   python main.py
   ```
7. Access the application at: http://localhost:5000

## SQL Injection Examples

### Authentication Bypass

Try these payloads in the username field (leave password blank or enter anything):

1. `' OR 1=1 --` (Always returns true and comments out the rest of the query)
2. `admin'--` (Logs in as admin by commenting out the password check)
3. `' UNION SELECT 'admin', 'password', 'admin@example.com', 'admin', '2023-01-01'--` (Creates a fake admin record)

### Understanding the Vulnerability

The vulnerable login code executes raw SQL queries with user input directly concatenated:

```python
# Vulnerable code
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

Secure alternative using parameterized queries:

```python
# Secure code
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

## Learning Exercises

1. **Authentication Bypass:**
   - Try different SQL injection payloads in the login form
   - Observe the executed SQL in the admin panel
   - Identify why the attack succeeded

2. **UNION Attacks:**
   - Experiment with UNION-based SQL injection to extract additional data
   - Example: `' UNION SELECT id, username, password, email, role FROM users --`

3. **Blind SQL Injection:**
   - Practice boolean-based blind injection techniques
   - Example: `admin' AND (SELECT SUBSTR(username,1,1) FROM users WHERE id=1)='a`

4. **Code Analysis:**
   - Review the source code to identify vulnerable patterns
   - Compare with secure implementations provided in the codebase

5. **Mitigation Strategies:**
   - Implement input validation
   - Use parameterized queries
   - Apply principle of least privilege
   - Implement proper error handling

## File Structure

- `main.py`: Entry point for the Flask application
- `app.py`: Flask application configuration
- `models.py`: Database models
- `database.py`: Contains both vulnerable and secure query execution
- `routes.py`: Application routes and endpoints
- `init_db.py`: Database initialization script
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
- `Dockerfile`: Docker container configuration
- `docker-compose.yml`: Multi-container Docker configuration (PostgreSQL)
- `docker-compose.sqlite.yml`: Simplified Docker configuration (SQLite)
- `docker-entrypoint.sh`: Entry point script for Docker container

## Creating a Distribution Package

To create a distribution package for sharing with students:

```bash
# Package the essential files
tar -czf sql_injection_demo.tar.gz \
    app.py database.py init_db.py main.py models.py routes.py \
    docker-compose.yml docker-compose.sqlite.yml Dockerfile docker-entrypoint.sh docker-requirements.txt \
    templates/ static/ README.md
```

This creates a compressed archive (`sql_injection_demo.tar.gz`) that can be easily distributed and contains all necessary files to run the demonstration.

## Additional Resources

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger SQL Injection Tutorial](https://portswigger.net/web-security/sql-injection)

## Credits

This application was created as an educational tool for cybersecurity and web application security courses. It is intended to be used in controlled environments under proper supervision.

## License

This project is licensed for educational purposes only. Do not use in production environments.
