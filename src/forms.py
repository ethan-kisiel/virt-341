"""
Forms pertaining to the main portion of the website
(login forms, etc)
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email


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


class StudentProfileForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    middleInitial = StringField("Middle Initial", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    classFlight = StringField("Class/Flight")
    organization = StringField("Organization")
    rank = StringField("Rank", validators=[DataRequired()])
    payGrade = StringField("Pay Grade", validators=[DataRequired()])
    arrivalTime = DateField("Date Arrived", validators=[DataRequired()])
    currentMTL = StringField("Current MTL", validators=[DataRequired()])
    studentPhase = StringField("Current Phase", validators=[DataRequired()])
    submit = SubmitField("Save")