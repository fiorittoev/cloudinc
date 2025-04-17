from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from utils import database as data
from sqlalchemy.exc import OperationalError
import time
import hashlib
import secrets

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# RDS Database configuration using mysql-connector
db_user = os.environ.get("MYSQL_USER")
db_password = os.environ.get("MYSQL_PASSWORD")
db_host = os.environ.get("MYSQL_HOST")
db_name = os.environ.get("MYSQL_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

def connect_to_db():
    with app.app_context():  # Ensure we are inside the application context
        while True:
            try:
                # Attempt to connect to the database
                db.engine.connect()
                print("Connected to database successfully")
                break  # Exit loop if successful
            except OperationalError:
                print("Database not ready, retrying in 5 seconds...")
                time.sleep(5)

# User authentication functions
def hash_password(password):
    """Hash a password using hashlib (SHA-256)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(conn, username, password):
    """Create a new user with hashed password"""
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, pass_word) VALUES (%s, %s)", 
                  (username, hashed_password))
    conn.commit()
    return cursor.lastrowid

def verify_user(conn, username, password):
    """Verify user credentials"""
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND pass_word = %s", 
                  (username, hashed_password))
    user = cursor.fetchone()
    return user is not None

# Make sure users table exists
def setup_user_table(conn):
    cursor = conn.cursor()

    conn.commit()

# Routes
@app.route('/')
def index():
    """Route to display all parts."""
    conn = data.create_connection()
    if conn:
        parts = data.fetch_parts(conn)
        conn.close()
        return render_template('index.html', parts=parts)
    else:
        return "Error connecting to the database"

@app.route('/products')
def products():
    """Route to display all products."""
    conn = data.create_connection()
    if conn:
        parts = data.fetch_parts(conn)
        print(parts)
        conn.close()
        return render_template('products.html', parts=parts)
    else:
        return "Error connecting to the database"

@app.route('/about')
def about():
    """Route to display about page."""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for user login."""
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = data.create_connection()
        if conn:
            if verify_user(conn, username, password):
                session['username'] = username
                flash('Login successful!', 'success')
                conn.close()
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
                conn.close()
        else:
            flash('Database connection error', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route for user registration."""
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        conn = data.create_connection()
        if conn:
            # Check if user already exists
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Username already exists', 'error')
                conn.close()
                return render_template('register.html')
            
            # Create new user
            create_user(conn, username, password)
            flash('Registration successful! Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        else:
            flash('Database connection error', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Route for user logout."""
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/account')
def account():
    """Route for user account page."""
    if 'username' not in session:
        flash('Please login to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('account.html', username=session['username'])
connect_to_db()
conn = data.create_connection()
if conn:
    data.create_table(conn)
    data.load_parts_from_csv(conn, './database/initial_data/parts.csv')
    
if __name__ == '__main__':
    # Setup the database and tables
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)