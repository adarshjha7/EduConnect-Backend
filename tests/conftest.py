import pytest
import json
from tests import app
import pytest
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum, db
from datetime import datetime

@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def create_draft_assignment():
    # Use datetime objects for created_at and updated_at
    created_at = datetime(2025, 1, 27, 16, 4, 56)  # Use datetime.datetime for DateTime
    updated_at = datetime(2025, 1, 27, 16, 4, 56)

    assignment = Assignment(
        id=5,
        student_id=2,
        teacher_id=2,
        content="THESIS T3",
        grade=None,  # No grade for draft
        state=AssignmentStateEnum.DRAFT.value,  # DRAFT state
        created_at=created_at,
        updated_at=updated_at
    )
    db.session.add(assignment)
    db.session.commit()  # Commit the new assignment to the database
    return assignment