import logging
from flask import render_template, request, jsonify, session, redirect, url_for, flash
from app import app
from database import execute_login_query, get_login_attempts, get_secure_login, init_db

# Initialize the database
with app.app_context():
    init_db()

@app.route('/')
def index():
    """Render the main page with the login form."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login attempts, intentionally vulnerable to SQL injection."""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Execute the vulnerable query
    result = execute_login_query(username, password)
    
    if result['success']:
        session['user'] = result['user']
        session['logged_in'] = True
        flash('Login successful!', 'success')
        
        # If admin, redirect to admin panel
        if result['user']['role'] == 'admin':
            return redirect(url_for('admin'))
        return redirect(url_for('index'))
    else:
        # For AJAX requests, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(result)
        
        # For standard form submission, redirect with flash message
        flash('Login failed. Try again or try SQL injection techniques.', 'danger')
        return redirect(url_for('index'))

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login (for AJAX requests)."""
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    result = execute_login_query(username, password)
    
    return jsonify(result)

@app.route('/admin')
def admin():
    """Admin panel to view login attempts and queries."""
    if not session.get('logged_in'):
        flash('You must be logged in to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    if session.get('user', {}).get('role') != 'admin':
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    # Get recent login attempts
    login_attempts = get_login_attempts()
    
    return render_template('admin.html', 
                           user=session.get('user'), 
                           login_attempts=login_attempts)

@app.route('/logout')
def logout():
    """Handle logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/api/login_attempts')
def api_login_attempts():
    """API endpoint to get login attempts."""
    if not session.get('logged_in') or session.get('user', {}).get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    
    login_attempts = get_login_attempts()
    return jsonify(login_attempts)

@app.route('/api/secure_login', methods=['POST'])
def api_secure_login():
    """API endpoint for secure login (for comparison)."""
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    result = get_secure_login(username, password)
    
    return jsonify(result)

@app.context_processor
def inject_user():
    """Inject user information into all templates."""
    return dict(
        user=session.get('user', None),
        logged_in=session.get('logged_in', False)
    )
