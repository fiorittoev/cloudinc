from flask import render_template
from app import app
import database as db

@app.route('/')
def index():
    """Route to display all parts."""
    conn = db.create_connection()
    if conn:
        parts = db.fetch_parts(conn)
        conn.close()  # Close connection after use
        return render_template('storefront.html', parts=parts)
    else:
        return "Error connecting to the database"
