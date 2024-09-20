"""
Utility file for login
"""

from flask_login import LoginManager

from managers.database_manager import DatabaseManager

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(email: str):
    """Loads account obj as user

    Keyword arguments:
    email -- account pk/email
    Return: returns none or user obj
    """

    return DatabaseManager.get_account(email)


@login_manager.request_loader
def request_loader(request):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    email = request.form.get("email")
    return DatabaseManager.get_account(email)
