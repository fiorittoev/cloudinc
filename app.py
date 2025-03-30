from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# RDS Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:MI361isfun@database-1.cxsaq0qa4oil.us-east-2.rds.amazonaws.com/parts'

# Initialize the database
db = SQLAlchemy(app)

if __name__ == '__main__':
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)
