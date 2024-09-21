"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

# pylint: disable=import-error


from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask_wtf import FlaskForm

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from blueprints.organization.bp_organization import organization_bp
from blueprints.student.bp_student import student_bp

from managers.config_manager import ConfigManager
from managers.database_manager import DatabaseManager

from forms import RegisterForm
from forms import LoginForm


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

    return render_template(
        "index.html", include_navbar=True
    )  # found in /src/templates/index.html


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


if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    app.debug = ConfigManager.config.is_development

    # host = ConfigManager.config.ip
    # port = ConfigManager.config.port

    app.run()  # TODO get control of host and port
