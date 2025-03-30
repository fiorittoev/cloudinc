import mysql.connector
from mysql.connector import Error

# Function to create a connection to the RDS database
def create_connection():
    """Create a connection to the MySQL RDS database."""
    try:
        conn = mysql.connector.connect(
            host="your-rds-endpoint.amazonaws.com",  # Change this to your RDS endpoint
            database="your_database_name",           # Database name
            user="your_username",                    # RDS username
            password="your_password"                 # RDS password
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
            part_id           TEXT NOT NULL PRIMARY KEY,
            part_name         TEXT NOT NULL,
            part_cost         FLOAT NOT NULL,
            part_manufacturer TEXT NOT NULL
        );
        """
        cursor.execute(sql_create_table)
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


# Function to close the connection
def close_connection(conn):
    """Close the database connection."""
    if conn.is_connected():
        conn.close()
        print("Connection closed.")
