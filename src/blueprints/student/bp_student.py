"""
Student specific views
"""

# pylint: disable=import-error

from flask import request, send_file, url_for, redirect
from flask import Blueprint
from flask import render_template
from flask_login import current_user

from flask_login import login_required

from managers.database_manager import DatabaseManager

from utils import generate_qr_code

from forms import StudentProfileForm
from forms import Form341

student_bp = Blueprint(
    "bp_student", __name__, template_folder="templates", static_folder="static"
)


@student_bp.route("/")
def index():
    """Index endpoint for testing purposes

    Keyword arguments:
    None

    Return:
    Renders the 341-form template
    """
    return redirect(url_for("bp_student.profile"))


@student_bp.route("/<int:student_id>/341form", methods=["GET", "POST"])
@login_required
def form341(student_id: int):
    """
    Renders the pre-filled 341 form for the current logged-in user's account.

    Return:
    Renders the 341-form template with pre-filled student data
    """

    form = Form341()
    student = DatabaseManager.get_student(student_id)

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404

    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile

    if request.method == "GET":
        pass

    return render_template("341-form.html", student=student, form=form)


@student_bp.route("/profile")
@student_bp.route("/profile/<int:student_id>")
@login_required
def profile(student_id: int = None):
    """Endpoint to render student profile page

        return redirect(url_for("bp_student.home"))

    Return:
    Renders the profile template for the student with the given ID
    """
    form = StudentProfileForm()

    if student_id is None:
        student = DatabaseManager.get_student_by_account(current_user.email)
        user = current_user.user
    else:
        student = DatabaseManager.get_student(student_id)
        user = student.user

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404
    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile

    return render_template(
        "student-profile.html",
        student=student,
        user=user,
        form=form,
        include_navbar=True,
    )


@student_bp.route("/341-code")
@student_bp.route("/<int:student_id>/341-code")
@login_required
def generate_student_qr(student_id: int = None):
    """
    Generates a QR code that links to the logged-in student's 341 form.

    Return:
    Sends the generated QR code as an image file
    """
    student = DatabaseManager.get_student_by_account(current_user.email)

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404
    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile

    qr_data_url = url_for("bp_student.form341", _external=True)
    img_io = generate_qr_code(qr_data_url)

    return send_file(img_io, mimetype="image/png")
