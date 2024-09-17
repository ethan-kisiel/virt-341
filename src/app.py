"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

# pylint: disable=import-error


from flask import Flask
from flask import render_template

from blueprints.squadron.bp_squadron import squadron_bp
from blueprints.student.bp_student import student_bp

from managers.config_manager import ConfigManager
from managers.database_manager import DatabaseManager

ConfigManager.load_config("config.ini")
DatabaseManager.set_database_url(ConfigManager.config.database_url)


app = Flask(__name__)

## register blueprints:
app.register_blueprint(squadron_bp, url_prefix="/squadron")
app.register_blueprint(student_bp, url_prefix="/student")


@app.route("/")
def index():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template("index.html")  # found in /src/templates/index.html

@app.route("/login")
def login():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template("login.html")  # found in /src/templates/index.html

if __name__ == "__main__":
    app.debug = ConfigManager.config.is_development

    # host = ConfigManager.config.ip
    # port = ConfigManager.config.port

    app.run()  # TODO get control of host and port
