"""
Sets up the database to have necessary data for demonstrating the website
"""

from managers.database_manager import DatabaseManager
from managers.config_manager import ConfigManager


def main():
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    ## CREATE ROLES
    ## CREATE STUDENTS

    organization_data = {
        "organization_name": "336 TRS",
    }

    try:
        DatabaseManager.add_organization(organization_data)
    except Exception as e:
        print(e)

    roles_data = [
        {"role_name": "Admin", "role_permission": 0},
        {"role_name": "Flight Chief", "role_permission": 1},
        {"role_name": "MTL", "role_permission": 2},
        {"role_name": "Instructor", "role_permission": 2},
        {"role_name": "Student", "role_permission": 3},
    ]

    for rd in roles_data:
        try:
            DatabaseManager.add_role(rd)
        except Exception as e:
            pass


if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    main()
