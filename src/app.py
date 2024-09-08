"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

from flask import Flask
from flask import render_template

from exceptions import UnimplementedException

app = Flask(__name__)


@app.route("/")
def index():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template("index.html")  # found in /src/templates/index.html


@app.route("/student-profile/")
def student_profile(student_id: int):
    """Endpoint for student profiles

    Keyword arguments:
    student_id -- primary key of the user object which is a student
    Return: Template
    """

    raise UnimplementedException()


if __name__ == "__main__":
    app.run()
