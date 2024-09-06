"""
Main app file (Web Server Gateway Interface)

includes routes, flask app, etc
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Initial view

    Keyword arguments:
    argument -- description
    Return: Template
    """
    return render_template("index.html")  # found in /src/templates/index.html


if __name__ == "__main__":
    app.run()
