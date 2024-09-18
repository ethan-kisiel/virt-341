"""
Student specific views
"""

# pylint: disable=import-error


from flask import Blueprint
from flask import render_template

from exceptions import UnimplementedException

from managers.database_manager import DatabaseManager

student_bp = Blueprint(
    "bp_student",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@student_bp.route("/")
def index():
    """index endpoint (for testing purposes)

    Keyword arguments:

    Return: Template
    """

    return render_template("341-form.html")

@student_bp.route("/<int:student_id>/profile")
def profile(student_id: int):
    """Endpoint for student profiles

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    return render_template("profile.html", student_id = student_id)

@student_bp.route("/<int:student_id>/reports")
def reports(student_id: int):
    """Endpoint for student reports

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    return render_template("reports.html", student_id = student_id)