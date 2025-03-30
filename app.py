from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import routes

# Initialize the Flask app
app = Flask(__name__)

# RDS Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:your_password@your-rds-endpoint.amazonaws.com/my_database'

# Initialize the database
db = SQLAlchemy(app)

# Home route - Display a welcome message or homepage
@app.route('/')
def index():
    return render_template('storefront.html')

if __name__ == '__main__':
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)
