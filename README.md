# virt-341
A webapp for tracking, managing, and providing insight on AETC Form 341 Excellence/Discrepancy reports


# Installation/Setup
1. Clone this repository
2. Ensure your working directory is the same the setup.bat file
3. Run the setup.bat file

# Run the program
Enter the following command to run the program (in the virt-341 base folder): ```python src/app.py```

# Packages
This project uses the [SQLAlchemy ORM](https://pypi.org/project/SQLAlchemy/) for database management.
This project uses [Flask Login](https://pypi.org/project/Flask-Login/) for user logins and session management.
This project uses [Segno](https://pypi.org/project/segno/) for generating QR codes.


# Project Architecture
```
.
├── src/
│   ├── blueprints/ <-- This chunks out a few core items for separation of concerns
│   │   ├── squadron/ <-- All views and viewmodels for squadron related functionality goes here
│   │   │   ├── static/
│   │   │   │   ├── js/
│   │   │   │   └── css/
│   │   │   ├── templates/
│   │   │   └── bp_squadron.py
│   │   └── student/ <-- All views and viewmodels for student related functionality goes here
│   │       ├── static/
│   │       │   ├── js/
│   │       │   └── css/
│   │       ├── templates/
│   │       └── bp_student.py
│   ├── managers/
│   │   ├── config_manager.py <-- Application configuration is managed here
│   │   └── database_manager.py <-- All database operations happen here
│   ├── persistent/
│   │   ├── images/
│   │   ├── migrations/ <-- Most likely not going to be used
│   │   └── app.db
│   ├── static/ <-- Static files for app.py views
│   │   ├── js/
│   │   └── css/
│   ├── templates/ <-- Views for app.py
│   ├── app.py <-- Main coordinator, topmost viewmodel
│   ├── constants.py
│   ├── exceptions.py
│   ├── models.py
│   └── utils.py
└── tests/
```