# Import relevant libraries
import os
import sqlite3
import json
import xml.etree.ElementTree as ET
import pytest

from lookup import (
    usage_is_incorrect,
    store_data_as_json,
    store_data_as_xml
)

@pytest.fixture
def setup_database():
    return [(1, "Alice", "Smith"), (2, "Bob", "Jones")]


# Function to test the usage_is_incorrect function with correct arguments
def test_usage_is_incorrect_correct_args():
    assert usage_is_incorrect(["vs", "123"], 1) is False
    assert usage_is_incorrect(["la", "John", "Doe"], 2) is False

# Function to test the usage_is_incorrect function with incorrect arguments
def test_usage_is_incorrect_incorrect_args():
    assert usage_is_incorrect(["vs"], 1) is True
    assert usage_is_incorrect(["la", "John"], 2) is True
    assert usage_is_incorrect(["la", "John", "Doe", "Extra"], 2) is True

# Function to test the store_data_as_json function
def test_store_data_as_json(tmp_path, sample_data):
    filename = tmp_path / "test_json.json"
    store_data_as_json(sample_data, filename)
    assert filename.exists()
    with open(filename, 'r') as f:
        data =json.load(f)
    assert data == sample_data

# Function to test the store_data_as_xml function
def test_store_data_as_xml(tmp_path, sample_data):
    filename = tmp_path / "test_xml.xml"
    store_data_as_xml(sample_data, filename)
    assert filename.exists()
    tree = ET.parse(filename)
    root = tree.getroot()
    entries = root.findall('entry')
    assert len(entries) == len(sample_data)
    assert entries[0].find("field1").text == "Alice"

# Function to test the database connection
def test_database_connection(tmp_path):
    # Create a temporal SQLite DataBase
    df_file = tmp_path / "test.db"
    conn = sqlite3.connect(df_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE Student (student_id INTEGER, first_name TEXT, last_name TEXT)")
    cur.execute("INSERT INTO Student VALUES (1, 'Alice', 'Smith')")
    cur.commit()

    cur.execute("SELECT fist_name, last_name FROM Student WHERE student_id = ?")
    result = cur.fetchone()
    assert result == ("Alice", "Smith")

    conn.close()
