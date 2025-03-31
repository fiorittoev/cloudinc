from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from utils import database as data

# Initialize the Flask app
app = Flask(__name__)

# RDS Database configuration using mysql-connector instead of pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:MI361isfun@database-1.cxsaq0qa4oil.us-east-2.rds.amazonaws.com/database-1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
conn = data.create_connection()
data.create_table(conn)

# Your models and routes would go here

@app.route('/')
def index():
    """Route to display all parts."""
    if conn:
        parts = data.fetch_parts(conn)
        conn.close()  # Close connection after use
        return render_template('storefront.html', parts=parts)
    else:
        return "Error connecting to the database"

if __name__ == '__main__':
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)