from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Home route - Display a welcome message or homepage
@app.route('/')
def index():
    return render_template('storefront.html')

if __name__ == '__main__':
    # Ensure this works in both development and production modes
    app.run(host='0.0.0.0', port=5000, debug=True)
