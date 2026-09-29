# 📊 Data Querying Application

This project is a **command-line data querying tool** built with **Python** and **SQLite**. It allows users to interact with a student–course database, run queries, and optionally export results to **JSON** or **XML** formats.  

---

## 🚀 Features
- Interactive CLI for querying student and course data.
- Safe, parameterized SQL queries to prevent injection.
- Export query results to **JSON** or **XML**.
- Commands to:
  - View subjects taken by a student.
  - Lookup student addresses.
  - List reviews for a student.
  - List courses taught by a teacher.
  - Identify students who haven’t completed their course.
  - Identify students who completed with low marks.
  - Demo listing of all student names.

---

## 🛠️ Technologies Used
- **Python**
- **SQLite**
- **JSON** (for structured data export)
- **XML** (for structured data export)

---

## 🧪 Testing
Unit tests are included using pytest.

**Tests cover**:
- Argument validation (usage_is_incorrect)
- JSON/XML export functions
- Database connection and queries
