"""
Forms pertaining to the main portion of the website
(login forms, etc)
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import SelectField

from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from wtforms.validators import Optional


# create form class
class RegisterForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    mname = StringField("Middle Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address"),
        ],
    )
    phone = StringField("Phone", validators=[DataRequired()])
    pwd = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_pwd", message="Passwords must match"),
        ],
    )
    confirm_pwd = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("pwd", message="Passwords must match")],
    )
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address"),
        ],
    )
    pwd = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    submit = SubmitField("Submit")


class UserAccountForm(FlaskForm):

    first_name = StringField("First Name", validators=[DataRequired()])
    middle_initial = StringField("Middle Initial", validators=[Optional()])
    last_name = StringField("Last Name", validators=[DataRequired()])

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address"),
        ],
    )
    phone = StringField("Phone", validators=[Optional()])

    rank = StringField("Rank", validators=[DataRequired()])

    role = SelectField(
        "Role",
        choices=[],  # Example choices
        validators=[Optional()],
    )

    organization = SelectField(
        "Organization",
        choices=[],  # Example choices
        validators=[DataRequired()],
    )
    submit = SubmitField("Save")
    delete = SubmitField("Delete")


class StudentProfileForm(FlaskForm):

    first_name = StringField(
        "First Name", validators=[Optional()], render_kw={"disabled": True}
    )
    middle_initial = StringField(
        "Middle Initial",
        validators=[Optional()],
        render_kw={"maxlength": 1, "disabled": True},
    )
    last_name = StringField(
        "Last Name", validators=[Optional()], render_kw={"disabled": True}
    )

    class_flight = StringField("Class/Flight", validators=[Optional()])

    organization = StringField(
        "Organization", validators=[Optional()], render_kw={"disabled": True}
    )

    rank = StringField("Rank", validators=[Optional()], render_kw={"disabled": True})

    pay_grade = StringField(
        "Pay Grade", validators=[Optional()], render_kw={"disabled": True}
    )

    current_mtl = SelectField(
        "MTL",
        choices=[],  # Example choices
        validators=[Optional()],
    )

    student_phase = SelectField(
        "Current Phase",
        choices=[
            ("", "Select student phase"),  # Placeholder for default select option
            (0, "Phase I - Green Card"),
            (1, "Phase II - White Card"),
            (2, "Phase III - Yellow Card"),
            (3, "Phase IV - Blue Card"),
            (4, "Phase V - Red Card"),
        ],
        validators=[Optional()],
        coerce=str,
    )

    submit = SubmitField("Save")


class Form341(FlaskForm):

    student_phase = StringField("Student Phase", render_kw={"readonly": True})

    # Name and Grade section
    name = StringField(
        "Last Name - First Name - Middle Initial", validators=[DataRequired()]
    )
    grade = StringField("Grade", validators=[DataRequired()])

    # Organization and Class/Flight section
    organization = StringField("Organization", validators=[Optional()])
    class_flight = StringField("Class/Flight", validators=[Optional()])

    # Excellence/Discrepancy section
    excellence_discrepancy = TextAreaField(
        "Excellence/Exhibited Discrepancy (Be specific)", validators=[DataRequired()]
    )

    # Time, Date, and Place section
    time = StringField("Time", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    place = StringField("Place", validators=[Optional()])

    # Reporting individual section
    reporting_name = StringField(
        "Printed Name of Reporting Individual", validators=[DataRequired()]
    )
    signature = StringField(
        "Signature of Reporting Individual", validators=[Optional()]
    )

    # Submit button
    submit = SubmitField("Submit")
