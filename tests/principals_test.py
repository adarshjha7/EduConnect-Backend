import pytest
from core.models import Assignment, AssignmentStateEnum, GradeEnum, db
from datetime import datetime

# Fixture to create a draft assignment@pytest.fixture
def create_draft_assignment():
    # Convert string to datetime object
    created_at = datetime.strptime("2025-01-27 16:04:56", "%Y-%m-%d %H:%M:%S")
    updated_at = datetime.strptime("2025-01-27 16:04:56", "%Y-%m-%d %H:%M:%S")

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

# Fixture to create a graded assignment
@pytest.fixture
def create_graded_assignment():
    # Create a graded assignment before each test
    assignment = Assignment(
        id=4,
        student_id=2,
        teacher_id=2,
        content="THESIS T2",
        grade=GradeEnum.B.value,  # Already graded
        state=AssignmentStateEnum.GRADED.value,
        created_at="2025-01-27 16:04:56",
        updated_at="2025-01-30 04:59:37",  # Use your desired updated timestamp
    )
    db.session.add(assignment)
    db.session.commit()  # Commit the new assignment to the database
    return assignment

# Test: Ensure only assignments in the 'SUBMITTED' or 'GRADED' state are returned
def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

# Test: Ensure that draft assignments cannot be graded by a principal
def test_grade_assignment_draft_assignment(client, h_principal, create_draft_assignment):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    # Use the fixture to get the draft assignment
    draft_assignment = create_draft_assignment

    # Try to grade the draft assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': draft_assignment.id,  # Use the ID of the draft assignment
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    # Expecting a 400 response because the assignment is in DRAFT state
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'


# Test: Grade an assignment that is in 'GRADED' state
def test_grade_assignment(client, h_principal, create_graded_assignment):
    graded_assignment = create_graded_assignment

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': graded_assignment.id,  # Use the ID of the graded assignment
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


# Test: Regrade an assignment that has already been graded
def test_regrade_assignment(client, h_principal, create_graded_assignment):
    graded_assignment = create_graded_assignment

    # Regrade the assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': graded_assignment.id,  # Use the ID of the graded assignment
            'grade': GradeEnum.B.value  # Regrade to 'B'
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
