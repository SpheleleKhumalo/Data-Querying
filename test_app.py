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


def test_usage_is_incorrect_incorrect_args():
    assert usage_is_incorrect(["vs"], 1) is True
    assert usage_is_incorrect(["la", "John"], 2) is True
    assert usage_is_incorrect(["la", "John", "Doe", "Extra"], 2) is True