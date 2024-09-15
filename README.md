# virt-341
A webapp for tracking, managing, and providing insight on AETC Form 341 Excellence/Discrepancy reports


# Installation/Setup
1. Clone this repository
2. Ensure your working directory is the same the setup.bat file
3. Run the setup.bat file

# Packages
This project uses the [SQLAlchemy ORM](https://pypi.org/project/SQLAlchemy/) for database management.
This project uses [Flask Login](https://pypi.org/project/Flask-Login/) for user logins and session management.
This project uses [Segno](https://pypi.org/project/segno/) for generating QR codes.


# Project Architecture
.<br>
├── src/<br>
│   ├── blueprints/ <-- This chunks out a few core items for separation of concerns<br>
│   │   ├── squadron/ <-- All views and viewmodels for squadron related functionality goes here<br>
│   │   │   ├── static/<br>
│   │   │   │   ├── js/<br>
│   │   │   │   └── css/<br>
│   │   │   ├── templates/<br>
│   │   │   └── bp_squadron.py<br>
│   │   └── student/ <-- All views and viewmodels for student related functionality goes here<br>
│   │       ├── static/<br>
│   │       │   ├── js/<br>
│   │       │   └── css/<br>
│   │       ├── templates/<br>
│   │       └── bp_student.py<br>
│   ├── managers/<br>
│   │   ├── config_manager.py <-- Application configuration is managed here<br>
│   │   └── database_manager.py <-- All database operations happen here<br>
│   ├── persistent/<br>
│   │   ├── images/<br>
│   │   ├── migrations/ <-- Most likely not going to be used<br>
│   │   └── app.db<br>
│   ├── static/ <-- Static files for app.py views<br>
│   │   ├── js/<br>
│   │   └── css/<br>
│   ├── templates/ <-- Views for app.py<br>
│   ├── app.py <-- Main coordinator, topmost viewmodel<br>
│   ├── constants.py<br>
│   ├── exceptions.py<br>
│   ├── models.py<br>
│   └── utils.py<br>
└── tests/<br>