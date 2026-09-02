# import important libraries
import sqlite3
import json
import xml.etree.ElementTree as ET

# Function to connect to a database safely
def connect_to_database(sd_name="Hyperion.db"):
    try:
        conn = sqlite3.connect(sd_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

conn = connect_to_database()
cur = conn.cursor() if conn else None

