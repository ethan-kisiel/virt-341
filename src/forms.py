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


class UpdateAccount(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    mname = StringField('Middle Inital', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    clsflt = StringField('Last Name', validators=[DataRequired()])
    org = StringField('Last Name', validators=[DataRequired()])
    rank = StringField('Last Name', validators=[DataRequired()])
    pgrade = StringField('Last Name', validators=[DataRequired()])
    datearv = DateField()
    mtl = StringField()
    phase = StringField()
    
    submit = SubmitField('Update Account')