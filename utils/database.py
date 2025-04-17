import mysql.connector
import csv
import os
from mysql.connector import Error

# Function to create a connection to the RDS database
def create_connection():
    """Create a connection to the MySQL RDS database."""
    try:
        conn = mysql.connector.connect(
           host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        if conn.is_connected():
            print("Connected to MySQL RDS database")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create the table
def create_table(conn):
    """Create the parts table in the RDS database."""
    try:
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS parts (
            part_id           VARCHAR(255) NOT NULL PRIMARY KEY, 
            part_name         TEXT NOT NULL,
            part_cost         FLOAT NOT NULL,
            part_manufacturer TEXT NOT NULL
        );"""
        
        cursor.execute(sql_create_table)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT NOT NULL,
            pass_word TEXT NOT NULL
        )
        ''')
        conn.commit()

        print("Table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

# Function to insert a new part into the table
def insert_part(conn, part):
    """Insert a new part into the parts table."""
    try:
        cursor = conn.cursor()
        sql_insert = """
        INSERT INTO parts (part_id, part_name, part_cost, part_manufacturer)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql_insert, part)
        conn.commit()
        print("Part inserted successfully.")
    except Error as e:
        print(f"Error inserting part: {e}")
        conn.rollback()

# Function to load parts from a CSV file and insert them into the database
def load_parts_from_csv(conn, csv_file):
    """Load parts from a CSV file and insert them into the database."""
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # Row format: part_id, part_name, part_cost, part_manufacturer
                part = (row[0], row[1], float(row[2]), row[3])
                insert_part(conn, part)
    except Exception as e:
        print(f"Error reading CSV file: {e}")

# Function to fetch parts from the database
def fetch_parts(conn):
    """Fetch all parts from the parts table."""
    try:
        cursor = conn.cursor()
        sql_query = """
        SELECT part_id, part_name, part_cost, part_manufacturer 
        FROM parts;
        """
        cursor.execute(sql_query)
        parts = cursor.fetchall()
        cursor.close()
        print(f"Retrieved {len(parts)} parts from database.")
        return parts
    except Error as e:
        print(f"Error fetching parts: {e}")
        return []
    
# Function to close the connection
def close_connection(conn):
    """Close the database connection."""
    if conn.is_connected():
        conn.close()
        print("Connection closed.")
