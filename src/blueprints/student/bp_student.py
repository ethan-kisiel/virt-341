"""
Student specific views
"""

# pylint: disable=import-error

from flask import request, send_file, url_for, redirect, abort
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


@student_bp.route("/<int:student_id>/341form")
@login_required
def form341(student_id: int):
    """
    Renders the pre-filled 341 form for the current logged-in user's account.

    Return:
    Renders the 341-form template with pre-filled student data
    """

    form = Form341()
    student = DatabaseManager.get_student_by_account(current_user.email)

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404
    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile

    return render_template("341-form.html", student=student, form=form)


# @student_bp.route("/profile")
# @student_bp.route("/profile/<int:student_id>")
# @login_required
# def profile(student_id: int = None):
#     """Endpoint to render student profile page

#         return redirect(url_for("bp_student.home"))

#     Return:
#     Renders the profile template for the student with the given ID
#     """
#     form = StudentProfileForm()

#     if student_id is None:
#         student = DatabaseManager.get_student_by_account(current_user.email)
#         user = current_user.user
#     else:
#         student = DatabaseManager.get_student(student_id)
#         user = student.user

#     if not student and student_id is not None:
#         return "404 Not found", 404  # if looking for nonexistent student, send 404
#     elif not student:
#         return redirect(
#             url_for("profile")
#         )  # if looking at own student profile, send to user profile

#     return render_template(
#         "student-profile.html",
#         student=student,
#         user=user,
#         form=form,
#         include_navbar=True,
#     )


@student_bp.route("/profile", methods=["GET", "POST", "DELETE"])
@student_bp.route("/profile/<int:student_id>", methods=["GET", "POST", "DELETE"])
@login_required
def profile(student_id=None):
    """Manage student profile (GET, POST, DELETE)

    Keyword arguments:
    student_id -- the ID of the student profile to retrieve, update, or delete
    Return:
    Renders the profile template or processes the form submission or deletion
    """

    if student_id is not None:
        try:
            # this endpoint is the current user looking at someone elses profile
            student = DatabaseManager.get_student(student_id)
            user = student.user
        except AttributeError:
            return "404 Not found.", 404
    else:
        # this endpoint is the current user looking at their student profile
        student = DatabaseManager.get_student_by_account(current_user.email)
        if not student:
            return "404 Not found.", 404

        user = student.user

    if request.method == "DELETE":
        DatabaseManager.delete_student(student.id)
        return "", 204

    form = StudentProfileForm()

    mtls = DatabaseManager.get_mtls()

    form.current_mtl.choices = [(mtl.id, mtl.qualified_name) for mtl in mtls]

    organizations = DatabaseManager.get_organizations()

    form.organization.choices = [  # populating the organization dropdown
        (organization.id, organization.organization_name)
        for organization in organizations
    ]

    if request.method == "GET":
        print("GET")

        current_user_student = DatabaseManager.get_student_by_account(
            current_user.email
        )
        # on get request populate form with existing data
        if student_id == current_user_student.id:
            return redirect(url_for("bp_student.profile"))

        form.first_name.data = user.first_name
        form.middle_initial.data = user.middle_initial
        form.last_name.data = user.last_name

        form.class_flight.data = student.class_flight

        form.organization.data = str(user.organization_id)
        form.rank.data = user.rank
        form.pay_grade.data = student.grade

        form.current_mtl.data = str(student.supervisor_id)

        form.student_phase.data = str(student.phase)

        if current_user.user.role.role_permission in [0, 1, 2]:
            form.first_name.render_kw = {"disabled": True}
            form.middle_initial.render_kw = {"disabled": True}
            form.last_name.render_kw = {"disabled": True}

            form.rank.render_kw = {"disabled": True}
            form.organization.render_kw = {"disabled": True}

    elif request.method == "POST":
        print("POST")
        if form.validate_on_submit():
            print("form is valid")
            student_data = {
                "rank": form.rank.data,
                "class_flight": form.class_flight.data,
                "supervisor_id": int(form.current_mtl.data),
                "phase": int(form.student_phase.data),
            }

            if current_user.user.role.role_permission not in [0, 1, 2]:
                student_data = {}

            DatabaseManager.update_student(student.id, student_data)

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
