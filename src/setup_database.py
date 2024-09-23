"""
Sets up the database to have necessary data for demonstrating the website
"""
import json
import os
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
        {"role_name": "Instructor", "role_permission": 3},
        {"role_name": "Student", "role_permission": 4},
    ]

    for rd in roles_data:
        try:
            DatabaseManager.add_role(rd)
        except Exception as e:
            pass
    
   
      

    with open('src/user_data.json', 'r') as file:
        user_data = json.loads(file.read())["users"] 
        print(user_data)
        for ud in user_data:
            try:
                DatabaseManager.add_user(ud)
            except Exception as e:
                pass
            
    with open('src/account_data.json', 'r') as file:
        account_data = json.loads(file.read())["accounts"] 
        print(account_data)
        for ad in account_data:
            try:
                DatabaseManager.add_account(ad)
            except Exception as e:
                pass
            
    with open('src/student_data.json', 'r') as file:
        student_data = json.loads(file.read())
        print(student_data)
        for sd in student_data:
            try:
                DatabaseManager.add_student(sd["student"])
            except Exception as e:
                pass




    
if __name__ == "__main__":

    ConfigManager.load_config("config.ini")
    DatabaseManager.set_database_url(ConfigManager.config.database_url)
    DatabaseManager.create_tables()

    main()
