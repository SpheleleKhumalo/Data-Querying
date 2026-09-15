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

# Function to promot user to store data in JSON or XML format
def offer_to_store(data):
    while True:
        choice = input("Do you want to store this data? Y/N: ").strip().lower()
        if choice == 'y':
            filename = input("Specify the filename (with .json or .xml extension): ").strip()
            if filename.endswith('.xml'):
                store_data_as_xml(data, filename)
            elif filename.endswith('.json'):
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .json or .xml.")
        elif choice in ("n", "no"):
            print("Data will not be stored.")
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


USAGE = """
Available commands:

d                          - demo (list all student names)
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who completed their course with marks <= 30
e                          - exit program
"""

print("Welcome to Data Querying Application!")

while True:
    print()
    user_input = input(USAGE + "\nType your option here: ").split()
    if not user_input:
        print("No input provided. Please enter a command.")
        continue

    command, *args = user_input

    if command == "d":
        data = cur.execute("SELECT first_name, last_name FROM students")
        for firstname, surname in data:
            print(f"{firstname} {surname}")

    elif command == "vs":
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        cur.execute("""
            SELECT c.course_name
            FROM Course c
            INNER JOIN StudentCourse sc ON c.course_code = sc.course_code
            WHERE sc.student_id = ?
        """, (student_id,))
        subjects = cur.fetchall()
        print(f"Subjects for student ID {student_id}:")
        for subject in subjects:
            print(subject[0])
        offer_to_store(subjects)

    elif command == "la":
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args
        cur.execute("""
            SELECT a.street, a.city
            FROM Address a
            INNER JOIN Student s ON a.address_id = s.address_id
            WHERE s.first_name = ? AND s.last_name = ?
        """, (firstname, surname))
        address = cur.fetchall()
        if address:
            print(f"Address for {firstname} {surname}: {address[0][0]}, {address[0][1]}")
            offer_to_store(address)
        else:
            print(f"No address found for {firstname} {surname}.")

    elif command == "lr":
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        cur.execute("""
            SELECT r.review_text, r.completeness, r.efficiency, r.style, r.documentation
            FROM Review r
            WHERE r.student_id = ?
            """, (student_id,))
        reviews = cur.fetchall()
        print(f"Reviews for student {student_id}:")
        for review_text, completeness, efficiency, style, documentation in reviews:
            print(f"Scores: {completeness}, Efficiency: {efficiency}, Style: {style}, Documentation: {documentation}")
            print(f"Review: {review_text},")
        offer_to_store(reviews)

    elif command == "lc":
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        cur.execute("""
            Select c.course_name
            FROM Course c
            WHERE c.teacher_id = ?
        """, (teacher_id,))
        courses = cur.fetchall()
        print(f"Course tought by teacher {teacher_id}:")
        for course in courses:
            print(course[0])
        offer_to_store(courses)

    elif command == "lnc":
        cur.execute("""
            SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name
            FROM Student s
            LEFT JOIN StudentCourse sc ON s.student_id = sc.student_id
            LEFT JOIN Course c ON sc.course_code = c.course_code
            WHERE sc.is_complete = 0
        """)
        incomplete_student = cur.fetchall()
        print("Students who haven't completed their course:")
        for student in incomplete_student:
            print(f"ID: {student[0]}, Name: {student[1]} {student[2]}, Email: {student[3]}, Course: {student[4]}")
        offer_to_store(incomplete_student)
        