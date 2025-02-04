from flask import Blueprint, jsonify, request, json
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.models.principals import Principal
from core.libs import helpers


from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principals_assignments = Assignment.get_assignments_by_principal()
    principals_assignments_dump = AssignmentSchema().dump(principals_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'])
def get_teachers():
    # Extract principal data from X-Principal header
    principal_data = request.headers.get('X-Principal')
    if not principal_data:
        return jsonify({'error': 'X-Principal header is missing'}), 400
    
    try:
        # Parse the principal data using the helper function (if implemented)
        principal_info = json.loads(principal_data)  # or use json.loads if not
        principal_id = principal_info.get('principal_id')
        
        if not principal_id:
            return jsonify({'error': 'Principal ID is missing in header'}), 400
        
        # Query teachers linked to this principal
        teachers = Teacher.query.filter_by(principal_id=principal_id).all()

        # Prepare the response data
        teachers_data = [{
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at.isoformat(),
            'updated_at': teacher.updated_at.isoformat()
        } for teacher in teachers]

        return jsonify({'data': teachers_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500