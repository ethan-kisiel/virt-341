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
            student = DatabaseManager.get_student(student_id)
            user = student.user
        except AttributeError:
            return "404 Not found.", 404
    else:
        student = DatabaseManager.get_student_by_account(current_user.email)
        if not student:
            return "404 Not found.", 404
        user = current_user.user

    if request.method == "DELETE":
        DatabaseManager.delete_student(student.id)
        return "", 204  

    form = StudentProfileForm()

    roles = DatabaseManager.get_roles()
    organizations = DatabaseManager.get_organizations()

    form.role.choices = [(role.id, role.role_name) for role in roles]
    form.role.choices.insert(0, (None, "Unassigned"))
    form.organization.choices = [(org.id, org.organization_name) for org in organizations]
    form.organization.choices.insert(0, (None, "Unassigned"))

    if request.method == "GET":

        if student_id == current_user.user_id:
            return redirect(url_for("bp_student.profile"))

        form.first_name.data = student.first_name
        form.middle_initial.data = student.middle_initial
        form.last_name.data = student.last_name

        form.email.data = user.email
        form.phone_number.data = student.phone_number
        form.rank.data = student.rank
        form.role.data = str(student.role_id)
        form.organization.data = str(student.organization_id)
        
        if current_user.user.role.role_permission not in [0, 1, 2]:
            form.first_name.render_kw = {'disabled': True}
            form.middle_initial.render_kw = {'disabled': True}
            form.last_name.render_kw = {'disabled': True}
            form.email.render_kw = {'disabled': True}
            form.rank.render_kw = {'disabled': True}
            form.role.render_kw = {'disabled': True}
            form.organization.render_kw = {'disabled': True}

    elif request.method == "POST":
        if form.validate_on_submit():
            student_data = {
                "last_name": form.last_name.data,
                "first_name": form.first_name.data,
                "middle_initial": form.middle_initial.data,
                "rank": form.rank.data,
                "phone_number": form.phone_number.data,
                "role_id": int(form.role.data),
                "organization_id": int(form.organization.data),
            }

            if current_user.user.role_id not in [0, 1, 2]:
                student_data = {"phone_number": form.phone_number.data}

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
