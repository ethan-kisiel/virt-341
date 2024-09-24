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
from forms import Form341Form

from constants import DISABLED_KWARGS

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

    form = Form341Form()
    student = DatabaseManager.get_student(student_id)

    mtls = DatabaseManager.get_mtls()
    form.reporting_individual.choices = [(mtl.id, mtl.qualified_name) for mtl in mtls]

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404

    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile

    if request.method == "GET":
        form.name.data = f"{student.user.last_name}, {student.user.first_name}, {student.user.middle_initial}"
        form.grade.data = f"{student.grade}"
        form.organization.data = student.user.organization.organization_name
        form.class_flight.data = student.class_flight
    else:
        # POST STUFF

        if current_user.user.role.role_permission == 5:
            return "FORBIDDEN", 403

        form_341_data = {
            "comment": form.excellence_discrepancy.data,
            "place": form.place.data,
            "date": form.date.data,
            "time": form.time.data,
            "reporting_individual": form.reporting_individual.data,
            "student_id": student.id,
        }

        DatabaseManager.add_341(form_341_data)
        student.has_341 = True
        DatabaseManager.update_student(student.id, {"has_341": True})

    return render_template("341-form.html", student=student, form=form)


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

    user_profile_url = url_for("profile", user_id=user.id)

    if request.method == "GET":
        print("GET")

        current_user_student = DatabaseManager.get_student_by_account(
            current_user.email
        )
        # on get request populate form with existing data
        if current_user_student is not None and student_id == current_user_student.id:
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

        if current_user.user.role.role_permission not in [0, 1, 2]:

            form.first_name.render_kw = DISABLED_KWARGS
            form.middle_initial.render_kw = DISABLED_KWARGS
            form.last_name.render_kw = DISABLED_KWARGS
            form.rank.render_kw = DISABLED_KWARGS
            form.organization.render_kw = DISABLED_KWARGS

            form.class_flight.render_kw = DISABLED_KWARGS

            form.pay_grade.render_kw = DISABLED_KWARGS
            form.current_mtl.render_kw = DISABLED_KWARGS
            form.student_phase.render_kw = DISABLED_KWARGS
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

    student_341s = DatabaseManager.get_341_for_student(student.id)
    return render_template(
        "student-profile.html",
        student=student,
        user=user,
        form=form,
        include_navbar=True,
        show_save_button=current_user.user.role.role_permission != 3,
        user_profile_url=user_profile_url,
        student_341s=student_341s,
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
    student_id = DatabaseManager.get_student_by_account(current_user.email).id
    student = DatabaseManager.get_student(student_id)

    if not student and student_id is not None:
        return "404 Not found", 404  # if looking for nonexistent student, send 404
    elif not student:
        return redirect(
            url_for("profile")
        )  # if looking at own student profile, send to user profile
    student_id = student_id or student.id

    qr_data_url = url_for("bp_student.form341", student_id=student_id, _external=True)
    img_io = generate_qr_code(qr_data_url)

    return send_file(img_io, mimetype="image/png")


@student_bp.route("/341-form", methods=["GET", "POST"])
@login_required
def form_341():
    """Excellence/Discrepancy Report Form

    Handle the 341 report form submission and rendering.

    Keyword arguments:
    Return: Rendered form or handle form submission
    """
    form = Form341Form()
    student = DatabaseManager.get_student_by_account(current_user.email)

    if request.method == "GET":
        # Pre-fill form fields with current student's data
        form.student_phase.data = DatabaseManager.get_student_phase(current_user.id)
        form.organization.data = current_user.organization
        form.name.data = f"{current_user.last_name} - {current_user.first_name} - {current_user.middle_initial}"
        form.grade.data = student.grade if student else None
        form.class_flight.data = student.class_flight if student else None

        return render_template(
            "341-form.html",
            form=form,
            student=student,
        )

    elif request.method == "POST":
        if form.validate_on_submit():
            # Collect form data and save it to the database
            form_data = {
                "name": form.name.data,
                "grade": form.grade.data,
                "organization": form.organization.data,
                "class_flight": form.class_flight.data,
                "excellence_discrepancy": form.excellence_discrepancy.data,
                "time": form.time.data,
                "date": form.date.data,
                "place": form.place.data,
                "reporting_name": form.reporting_name.data,
                "signature": form.signature.data,
                "student_phase": form.student_phase.data,
            }

            DatabaseManager.submit_341_report(current_user.id, form_data)

            return redirect(url_for("bp_student.form_341"))

    # Handle any form errors
    return render_template(
        "341-form.html",
        form=form,
        student=student,
    )
