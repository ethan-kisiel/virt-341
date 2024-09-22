"""
Squadron analytics and other organizational information
"""

# pylint: disable=import-error

from flask import Blueprint
from flask import render_template

from flask_login import login_required

from exceptions import UnimplementedException

from managers.database_manager import DatabaseManager


organization_bp = Blueprint(
    "bp_organization", __name__, template_folder="templates", static_folder="static"
)


@organization_bp.route("/")
@login_required
def index():
    """index endpoint (for testing purposes)

    Keyword arguments:

    Return: Template
    """

    return render_template("organization.html")


# @organization_bp.route("/<int:organization_id>")
@organization_bp.route("/<int:organization_id>")
@login_required
def organization(organization_id: int):
    """Endpoint for student profiles

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    raise UnimplementedException()
