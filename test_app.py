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