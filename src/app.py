"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

# pylint: disable=import-error


from flask import Flask
from flask import render_template

from blueprints.organization.bp_organization import organization_bp
from blueprints.student.bp_student import student_bp

from managers.config_manager import ConfigManager
from managers.database_manager import DatabaseManager

app = Flask(__name__)

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
    return render_template(
        "index.html", include_navbar=True
    )  # found in /src/templates/index.html


@app.route("/login")
def login():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template(
        "login.html", include_navbar=True
    )  # found in /src/templates/index.html


@app.route("/register")
def register():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template(
        "register.html", include_navbar=True
    )  # found in /src/templates/index.html


if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    app.debug = ConfigManager.config.is_development

    # host = ConfigManager.config.ip
    # port = ConfigManager.config.port

    app.run()  # TODO get control of host and port
