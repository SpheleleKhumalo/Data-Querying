# import important libraries
import sqlite3
import json
import xml.etree.ElementTree as ET

# Function to connect to a database safely
def connect_to_database(db_name="Hyperion.db"):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

conn = connect_to_database()
cur = conn.cursor() if conn else None

# Function to check if the usage of a command is incorrect
def usage_is_incorrect(user_input, num_args):
    # Check if the number of arguments provided by the user is correct
    if len(user_input) != num_args + 1:
        print(f"Incorrect usage. Expected {num_args} arguments, but got {len(user_input) - 1}.")
        return True
    return False


# Function to store data as JSON
def store_data_as_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully stored in {filename}")
    except Exception as e:
        print(f"Error storing data as JSON: {e}")


# Function to store data as XML
def store_data_as_xml(data, filename):
    try:
        root = ET.Element("root")
        for key, value in data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(filename)
        print(f"Data stored successully in {filename}")
    except Exception as e:
        print(f"Error storing data as XML: {e}")