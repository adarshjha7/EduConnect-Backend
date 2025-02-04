---

# EduConnect Backend

## Description

**EduConnect Backend** is a Flask-based RESTful API designed to manage educational data such as students, teachers, assignments, and user roles (principals). The backend uses custom header-based authentication to manage user access and integrates with a **SQLite** database for efficient data management. The database is managed using **DB Browser for SQLite** for ease of viewing and editing database contents.

## Features

- **Custom Header-based Authentication** via `X-Principal`
- **CRUD Operations** for Teachers, Students, and Assignments
- **Role-based Access Control**: Principals can view all teachers and assignments, while students and teachers have role-specific access
- **Database Integration** with **SQLite**
- **REST API Endpoints** for educational operations like viewing and grading assignments
- **Database Management** using **DB Browser for SQLite**

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (managed with DB Browser for SQLite)
- **Authentication**: Custom header-based authentication using `X-Principal`
- **Environment Management**: Virtualenv
- **Testing**: Pytest

## Installation

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/adarshjha7/EduConnect-Backend.git
cd EduConnect-Backend
```

### 2. Set Up Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
python -m venv env
```

Activate the virtual environment:

- On Windows:
  ```bash
  source env/Scripts/activate
  ```

- On macOS/Linux:
  ```bash
  source env/bin/activate
  ```

### 3. Install Dependencies

Once the virtual environment is activated, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following variables:

```env
DB_HOST=your-database-host
DB_PORT=3306
DB_USERNAME=your-database-username
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
```

### 5. Reset the Database

To reset the database and apply the migrations, run:

```bash
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```

### 6. Database Management with DB Browser for SQLite

For viewing, editing, and managing the SQLite database, you can use **[DB Browser for SQLite](https://sqlitebrowser.org/)**. This tool provides a GUI to easily manage the database schema, view tables, and run SQL queries.

- **Open the Database**: Open the `store.sqlite3` file in **DB Browser for SQLite**.
- **View Data**: View and edit data in the tables.
- **Run Queries**: Execute SQL queries for managing data.

### 7. Start the Server

To start the server, run:

```bash
bash run.sh
```

### 8. Run Tests

To run tests, use the following command:

```bash
pytest -vvv -s tests/
```

For test coverage report:

```bash
# pytest --cov
# open htmlcov/index.html
```

---

## Implemented APIs

### 1. **Authentication**

**Header**: `X-Principal`  
**Value**: `{"user_id":1, "student_id":1}`  
For APIs to work, the `X-Principal` header is required to establish identity and context.

### 2. **Student APIs**

- **GET** `/student/assignments`  
  List all assignments created by a student.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":1, "student_id":1}
  }
  ```

  **Response**:
  ```json
  {
    "data": [
      {
        "content": "ESSAY T1",
        "created_at": "2024-09-17T02:53:45.028101",
        "grade": null,
        "id": 1,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2024-09-17T02:53:45.034289"
      },
      {
        "content": "THESIS T1",
        "created_at": "2024-09-17T02:53:45.028876",
        "grade": null,
        "id": 2,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2024-09-17T02:53:45.028882"
      }
    ]
  }
  ```

- **POST** `/student/assignments`  
  Create a new assignment.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":2, "student_id":2}
  }
  ```

  **Payload**:
  ```json
  {
    "content": "some text"
  }
  ```

  **Response**:
  ```json
  {
    "data": {
      "content": "some text",
      "created_at": "2024-09-17T03:14:08.572545",
      "grade": null,
      "id": 5,
      "state": "DRAFT",
      "student_id": 1,
      "teacher_id": null,
      "updated_at": "2024-09-17T03:14:08.572560"
    }
  }
  ```

- **POST** `/student/assignments/submit`  
  Submit an assignment.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":1, "student_id":1}
  }
  ```

  **Payload**:
  ```json
  {
    "id": 2,
    "teacher_id": 2
  }
  ```

  **Response**:
  ```json
  {
    "data": {
      "content": "THESIS T1",
      "created_at": "2024-09-17T03:14:01.580467",
      "grade": null,
      "id": 2,
      "state": "SUBMITTED",
      "student_id": 1,
      "teacher_id": 2,
      "updated_at": "2024-09-17T03:17:20.147349"
    }
  }
  ```

### 3. **Teacher APIs**

- **GET** `/teacher/assignments`  
  List all assignments submitted to this teacher.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":3, "teacher_id":1}
  }
  ```

  **Response**:
  ```json
  {
    "data": [
      {
        "content": "ESSAY T1",
        "created_at": "2024-09-17T03:14:01.580126",
        "grade": null,
        "id": 1,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2024-09-17T03:14:01.584644"
      }
    ]
  }
  ```

- **POST** `/teacher/assignments/grade`  
  Grade an assignment.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":3, "teacher_id":1}
  }
  ```

  **Payload**:
  ```json
  {
    "id": 1,
    "grade": "A"
  }
  ```

  **Response**:
  ```json
  {
    "data": {
      "content": "ESSAY T1",
      "created_at": "2024-09-17T03:14:01.580126",
      "grade": "A",
      "id": 1,
      "state": "GRADED",
      "student_id": 1,
      "teacher_id": 1,
      "updated_at": "2024-09-17T03:20:42.896947"
    }
  }
  ```

### 4. **Principal APIs**

- **GET** `/principal/assignments`  
  List all submitted and graded assignments.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":5, "principal_id":1}
  }
  ```

  **Response**:
  ```json
  {
    "data": [
      {
        "content": "ESSAY T1",
        "created_at": "2024-09-17T03:14:01.580126",
        "grade": null,
        "id": 1,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2024-09-17T03:14:01.584644"
      }
    ]
  }
  ```

- **POST** `/principal/assignments/grade`  
  Grade or re-grade an assignment.

  **Headers**:
  ```json
  {
    "X-Principal": {"user_id":5, "principal_id":1}
  }
  ```

  **Payload**:
  ```json
  {
    "id": 1,
    "grade": "A"
  }
  ```

  **Response**:
  ```json
  {
    "data": {
      "content": "ESSAY T1",
      "created_at": "2024-09-17T03:14:01.580126",
      "grade": "A",
      "id": 1,
      "state": "GRADED",
      "student_id": 1,
      "teacher_id": 1,
      "updated_at": "2024-09-17T03:20:42.896947"
    }
  }
  ```

---
