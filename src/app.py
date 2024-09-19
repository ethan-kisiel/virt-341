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
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from flask_wtf import FlaskForm
from flask_login import UserMixin
from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

from blueprints.organization.bp_organization import organization_bp
from blueprints.student.bp_student import student_bp

from managers.config_manager import ConfigManager
from managers.database_manager import DatabaseManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "ctrlaltelite"


# create form class
class RegisterForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    mname = StringField("Middle Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address")])
    pwd = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_pwd', message="Passwords must match")])
    confirm_pwd = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('pwd', message="Passwords must match")])
    submit = SubmitField("Submit")


## register blueprints:
app.register_blueprint(organization_bp, url_prefix="/organization")
app.register_blueprint(student_bp, url_prefix="/student")

# student/
#       profile, 341, analytics,
# student/<int: student_id>/


@app.route("/")
def index():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """

    print(DatabaseManager.get_account("test_email@gmail.com"))

    return render_template(
        "index.html", include_navbar=True
    )  # found in /src/templates/index.html


@app.route("/login", methods=["GET", "POST"])
def login():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template(
        "login.html", include_navbar=True
    )  # found in /src/templates/index.html


@app.route("/register", methods=["GET","POST"])
def register():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """

    form = RegisterForm()

    if request.method == "POST":
        print(form.validate_on_submit())
    if form.validate_on_submit():
        fname = form.fname.data
        form.fname.data = ''
        mname = form.mname.data
        form.mname.data = ''
        lname = form.lname.data
        form.lname.data = ''
        email = form.email.data
        form.email.data = ''
        pwd = form.pwd.data
        form.pwd.data = ''

        print(url_for('login'))
        return redirect(url_for('login'))

    return render_template("register.html",
                           form = form,
                           include_navbar = True)  # found in /src/templates/index.html


if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    app.debug = ConfigManager.config.is_development

    # host = ConfigManager.config.ip
    # port = ConfigManager.config.port

    app.run()  # TODO get control of host and port
