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

student_bp = Blueprint(
    "bp_student", __name__, template_folder="templates", static_folder="static"
)



# @student_bp.route("/<int:student_id>/341form")
# @login_required
# def form341(student_id: int):
#     """
#     Renders the pre-filled 341 form for a specific student.

#     Keyword arguments:
#     student_id -- an integer representing the student's unique ID

#     Return:
#     Renders the 341-form template with pre-filled student data
#     """
#     student = DatabaseManager.get_student(student_id)

#     if not student:
#         return redirect(url_for("bp_student.home"))

#     return render_template("341-form.html", student=student)


@student_bp.route("/341form")
@login_required
def form341():
    """
    Renders the pre-filled 341 form for the current logged-in user's account.

    Return:
    Renders the 341-form template with pre-filled student data
    """
    student = DatabaseManager.get_student_by_account(current_user.email)

    if not student:
        return redirect(url_for("bp_student.home"))

    return render_template("341-form.html", student=student)



@student_bp.route("/generate-qr")
@login_required
def generate_student_qr():
    """
    Generates a QR code that links to the logged-in student's 341 form.

    Return:
    Sends the generated QR code as an image file
    """
    student = DatabaseManager.get_student_by_account(current_user.email)

    if not student:
        return redirect(url_for("bp_student.home"))

    qr_data_url = url_for("bp_student.form341", _external=True)
    img_io = generate_qr_code(qr_data_url)

    return send_file(img_io, mimetype="image/png")


# @student_bp.route("/<int:student_id>/generate-qr")
# @login_required
# def generate_student_qr(student_id: int):
#     """
#     Generates a QR code that links to the student's 341 form.

#     Keyword arguments:
#     student_id -- an integer representing the student's unique ID

#     Return:
#     Sends the generated QR code as an image file
#     """
#     qr_data_url = url_for("bp_student.form341", student_id=student_id, _external=True)
#     img_io = generate_qr_code(qr_data_url)

#     return send_file(img_io, mimetype="image/png")


@student_bp.route("/")
def index():
    """Index endpoint for testing purposes

    Keyword arguments:
    None

    Return:
    Renders the 341-form template
    """
    return redirect(url_for("bp_student.profile"))


@student_bp.route("/profile")
@student_bp.route("/profile/<int:student_id>")
@login_required
def profile(student_id: int = None):
    """Endpoint to render student profile page

        return redirect(url_for("bp_student.home"))

    Return:
    Renders the profile template for the student with the given ID
    """

    if student_id is None:
        student = DatabaseManager.get_student_by_account(current_user.email)
    else:
        student = DatabaseManager.get_student(student_id)

    if not student:
        return redirect(url_for("bp_student.home"))

    return render_template("student-profile.html", student=student)



@student_bp.route("/profile/<int:student_id>/save", methods=["POST"])
@login_required
def save_profile(student_id: int):
    student = DatabaseManager.get_student(student_id)

    if not student:
        return redirect(url_for("bp_student.home"))

    updated_data = {
        "first_name": request.form.get("firstName"),
        "last_name": request.form.get("lastName"),
    }

    DatabaseManager.update_student(student_id, updated_data)

    return redirect(url_for("bp_student.profile", student_id=student_id))



@student_bp.route("/profile/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_profile(student_id: int):
    """Endpoint to delete student profile

    Keyword arguments:
    student_id -- an integer representing the primary key of the student user

    Return:
    Redirects to the home page after deleting the student
    """
    if student_id is None:
        student = DatabaseManager.get_student_by_account(current_user.email)
    else:
        student = DatabaseManager.get_student(student_id)

    if not student:
        return redirect(url_for("bp_student.home"))

    DatabaseManager.delete_student(student_id)

    return redirect(url_for("bp_student.home"))


# @student_bp.route("/<int:student_id>/reports")
# @login_required
# def reports(student_id: int):
#     """Endpoint to render student reports page

#     Keyword arguments:
#     student_id -- an integer representing the primary key of the student user

#     Return:
#     Renders the reports template for the student with the given ID
#     """

#     student = DatabaseManager.get_student()
#     return render_template("reports.html", student_id=student_id)





# @student_bp.route("/<int:student_id>/341form")
# @login_required
# def form341(student_id: int):
#     """
#     Renders the pre-filled 341 form for a specific student.

#     Keyword arguments:
#     student_id -- an integer representing the student's unique ID

#     Return:
#     Renders the 341-form template with pre-filled student data
#     """
#     student = DatabaseManager.get_student(student_id)
    
#     if not student:
#         return redirect(url_for("bp_student.home"))

#     return render_template("341-form.html", student=student)


# @student_bp.route("/<int:student_id>/generate-qr")
# @login_required
# def generate_student_qr(student_id: int):
#     """
#     Generates a QR code that links to the student's 341 form.

#     Keyword arguments:
#     student_id -- an integer representing the student's unique ID

#     Return:
#     Sends the generated QR code as an image file
#     """
#     qr_data_url = url_for("bp_student.form341", student_id=student_id, _external=True)
#     img_io = generate_qr_code(qr_data_url)

#     return send_file(img_io, mimetype="image/png")