"""
Student specific views
"""

# pylint: disable=import-error


from flask import Blueprint

from exceptions import UnimplementedException

student_bp = Blueprint("bp_student", __name__, template_folder="templates")


@student_bp.route("/<int:student_id>")
def student_profile(student_id: int):
    """Endpoint for student profiles

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    raise UnimplementedException()
