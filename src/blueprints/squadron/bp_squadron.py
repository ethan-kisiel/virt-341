"""
Squadron analytics and other organizational information
"""

# pylint: disable=import-error

from flask import Blueprint

from exceptions import UnimplementedException


squadron_bp = Blueprint("bp_squadron", __name__, template_folder="templates")


@squadron_bp.route("/<int:squadron_id>")
def squadron(squadron_id: int):
    """Endpoint for student profiles

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    raise UnimplementedException()
