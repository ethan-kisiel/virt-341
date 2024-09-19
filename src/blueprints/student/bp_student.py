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

@student_bp.route('/home')
def home():
    """Home endpoint

    Keyword arguments:
    None

    Return: 
    Renders the 341-form template
    """
    return render_template('341-form.html')

@student_bp.route('/<int:student_id>/341form')
def home():
    """Home endpoint

    Keyword arguments:
    None

    Return: 
    Renders the 341-form template
    """
    return render_template('341-form.html')


@student_bp.route("/")
def index():
    """Index endpoint for testing purposes

    Keyword arguments:
    None

    Return: 
    Renders the 341-form template
    """
    return render_template("341-form.html")


@student_bp.route("/<int:student_id>/profile")
def profile(student_id: int):
    """Endpoint to render student profile page

    Keyword arguments:
    student_id -- an integer representing the primary key of the student user

    Return: 
    Renders the profile template for the student with the given ID
    """
    return render_template("profile.html", student_id=student_id)


@student_bp.route("/<int:student_id>/reports")
def reports(student_id: int):
    """Endpoint to render student reports page

    Keyword arguments:
    student_id -- an integer representing the primary key of the student user

    Return: 
    Renders the reports template for the student with the given ID
    """
    return render_template("reports.html", student_id=student_id)

