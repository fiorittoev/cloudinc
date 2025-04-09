from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from utils import database as data
from sqlalchemy.exc import OperationalError
import time

# Initialize the Flask app
app = Flask(__name__)

# RDS Database configuration using mysql-connector instead of pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:MI361isfun@database-1.cxsaq0qa4oil.us-east-2.rds.amazonaws.com'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

def connect_to_db():
    with app.app_context():  # Ensure we are inside the application context
        while True:
            try:
                # Attempt to connect to the database
                db.engine.connect()
                break  # Exit loop if successful
            except OperationalError:
                print("Database not ready, retrying in 5 seconds...")
                time.sleep(5)

# Your models and routes would go here

connect_to_db()
conn = data.create_connection()
data.create_table(conn)
data.load_parts_from_csv(conn, './database/initial_data/parts.csv')

@app.route('/')
def index():
    """Route to display all parts."""
    if conn:
        # Load data from CSV and insert it into the database
        
        parts = data.fetch_parts(conn)
        conn.close()
        return render_template('storefront.html', parts=parts)
    else:
        return "Error connecting to the database"


if __name__ == '__main__':
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)