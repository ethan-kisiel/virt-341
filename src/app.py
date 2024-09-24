"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

# pylint: disable=import-error


from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask_wtf import FlaskForm

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from constants import DISABLED_KWARGS

from blueprints.organization.bp_organization import organization_bp
from blueprints.student.bp_student import student_bp

from managers.config_manager import ConfigManager
from managers.database_manager import DatabaseManager

from forms import RegisterForm
from forms import LoginForm
from forms import UserAccountForm


from login_util import login_manager


app = Flask(__name__)
app.config["SECRET_KEY"] = "ctrlaltelite"


## register blueprints:
app.register_blueprint(organization_bp, url_prefix="/organization")
app.register_blueprint(student_bp, url_prefix="/student")

login_manager.init_app(app)  # init login manager

# student/
#       profile, 341, analytics,
# student/<int: student_id>/


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Unauthorized users will be sent to login screen
    """

    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """

    return redirect(url_for("profile"))


@app.route("/logout")
@login_required
def logout():
    """Logs out user

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    logout_user()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """

    form = LoginForm()
    if request.method == "POST":
        print(form.email.data)
        print(form.pwd.data)
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.pwd.data

            user = DatabaseManager.get_account(email)
            print(pwd)
            if user is not None and user.countersign == pwd:
                login_user(user)
                return redirect(url_for("index"))

    return render_template(
        "login.html", form=form, include_navbar=False
    )  # found in /src/templates/index.html


@app.route("/register", methods=["GET", "POST"])
def register():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    form = RegisterForm()

    if request.method == "POST":

        print("Form Data:")
        print(f"First Name: {form.fname.data}")
        print(f"Middle Name: {form.mname.data}")
        print(f"Last Name: {form.lname.data}")
        print(f"Email: {form.email.data}")
        print(f"Phone: {form.phone.data}")
        print(f"Password: {form.pwd.data}")

        fname = form.fname.data
        mname = form.mname.data
        lname = form.lname.data
        phone = form.phone.data
        email = form.email.data
        pwd = form.pwd.data

        new_user = {
            "first_name": fname,
            "middle_initial": mname,
            "last_name": lname,
            "phone_number": phone,
        }

        user = DatabaseManager.add_user(new_user)

        new_account = {"email": email, "countersign": pwd, "user_id": user.id}
        DatabaseManager.add_account(new_account)
        return redirect(url_for("login"))

    return render_template(
        "register.html", form=form, include_navbar=False
    )  # found in /src/templates/index.html


#### ROUTE FOR USER PROFILE
@app.route("/profile", methods=["GET", "POST", "DELETE"])
@app.route("/profile/<int:user_id>", methods=["GET", "POST", "DELETE"])
@login_required
def profile(user_id=None):
    """user profile

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    if user_id is not None:
        try:
            account = DatabaseManager.get_account_by_user_id(
                user_id
            )  # TODO Implement get account by user
            user = account.user
        except AttributeError:
            return "404 Not found.", 404
    else:
        account = current_user
        user = current_user.user

    if request.method == "DELETE":
        DatabaseManager.remove_user(user.id, account.id)

    form = UserAccountForm()

    roles = DatabaseManager.get_roles()
    organizations = DatabaseManager.get_organizations()

    form.role.choices = [(role.id, role.role_name) for role in roles]
    form.role.choices.insert(0, (None, "Unassigned"))  # add an unassigned role
    form.organization.choices = [
        (organization.id, organization.organization_name)
        for organization in organizations
    ]

    form.organization.choices.insert(0, (None, "Unassigned"))

    user_student = DatabaseManager.get_student_by_user_id(user.id)

    if user_student is not None:
        student_profile_url = url_for("bp_student.profile", student_id=user_student.id)
    else:
        student_profile_url = None

    if request.method == "GET":

        print("GET")
        if user_id == current_user.user_id:
            return redirect(url_for("profile"))

        form.first_name.data = user.first_name
        form.middle_initial.data = user.middle_initial
        form.last_name.data = user.last_name

        form.email.data = account.email

        form.phone.data = user.phone
        form.rank.data = user.rank
        form.role.data = str(user.role_id)

        form.organization.data = str(user.organization_id)

        if (
            current_user.user.role is None
            or current_user.user.role.role_permission not in [0, 1, 2]
        ):
            form.first_name.render_kw = DISABLED_KWARGS
            form.middle_initial.render_kw = DISABLED_KWARGS
            form.last_name.render_kw = DISABLED_KWARGS

            form.email.render_kw = DISABLED_KWARGS
            form.rank.render_kw = DISABLED_KWARGS
            form.role.render_kw = DISABLED_KWARGS

            form.organization.render_kw = DISABLED_KWARGS

    else:  # request is POST at this point
        print("POST ")
        if form.validate_on_submit():
            if form.organization.data == "None":
                flash("Please select an organization before submitting.", "danger")
                return render_template(
                    "profile.html",
                    account=account,
                    user=user,
                    roles=roles,
                    form=form,
                    include_navbar=True,
                )
            user_data = {
                "last_name": form.last_name.data,
                "first_name": form.first_name.data,
                "middle_initial": form.middle_initial.data,
                "rank": form.rank.data,
                "phone": form.phone.data,
                "role_id": int(form.role.data),
                "organization_id": int(form.organization.data),
            }
            student_data = {
                "id": user.id,
                "phase": 1,
                "class_flight": "Change me",
                "grade": "E1",
                "user_id": user.id,
                "supervisor_id": 1,
            }
            # if the user doesn't have edit privelages
            if current_user.user.role.role_permission not in [0, 1, 2]:
                user_data = {"phone": form.phone.data}

            DatabaseManager.update_user(user.id, user_data)
            DatabaseManager.add_student(student_data)
            flash("User information updated successfully.", "success")
            
    roles = DatabaseManager.get_roles()

    return render_template(
        "profile.html",
        account=account,
        user=user,
        roles=roles,
        form=form,
        student_profile_url=student_profile_url,
        include_navbar=True,
    )


if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    app.debug = ConfigManager.config.is_development

    # host = ConfigManager.config.ip
    # port = ConfigManager.config.port

    app.run(host="0.0.0.0", port=8080)  # TODO get control of host and port
