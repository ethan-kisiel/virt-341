"""
Manages all database interactions
"""

from typing import Any
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from models import Base
from models import Account
from models import User
from models import Student
from models import Role
from models import Organization
from models import Form341


def create_account(session, account_data: dict):
    """function that creates an account object on the session, given

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    try:
        account = Account(
            email=account_data.get("email"),
            countersign=account_data.get("countersign"),
        )
        account.user_id = account_data.get("user_id")
        session.add(account)

        session.commit()

        return account
    except ValueError:
        print("Value error")
    except Exception as e:
        print(e)


def create_user(session, user_data: dict):
    """function that creates a user object on the session, given

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    # change these
    try:
        user = User(
            first_name=user_data.get("first_name"),
            middle_initial=user_data.get("middle_initial"),
            last_name=user_data.get("last_name"),
            phone=user_data.get("phone"),
        )

        session.add(user)

        session.commit()

        return user

    except ValueError:

        print("Value error")
    except Exception as e:
        print(e)


def create_role(session, role_data: dict):
    """function that creates a user object on the session, given

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    # change these
    try:
        role = Role(
            role_name=role_data.get("role_name"),
            role_permission=role_data.get("role_permission"),
        )

        session.add(role)

        session.commit()

        return role

    except ValueError:
        print("Value error")
    except Exception as e:
        print(e)


class DatabaseManager:
    """
    Handles database interactions
    """

    database_url = ""
    engine = None

    @classmethod
    def with_connection(cls, callback: Callable, *args, **kwargs) -> Any:
        """exectues callback with the class-based db engine

        Keyword arguments:
        cls -- class obj
        callback -- callable
        Return: Any
        """

        with cls.engine.connect() as connection:
            return callback(connection, *args, **kwargs)

    @classmethod
    def with_session(cls, callback: Callable, *args, **kwargs) -> Any:
        """executes callback with a session

        Keyword arguments:
        cls -- class obj
        callback -- callable
        Return: Any
        """

        with Session(cls.engine, expire_on_commit=False) as session:
            return callback(session, *args, **kwargs)

    @classmethod
    def set_database_url(cls, url: str) -> None:
        """Sets the value of cls.database_route

        Keyword arguments:
        url -- url of the database
        Return: None
        """

        cls.database_url = url
        cls.engine = create_engine(url)

    @classmethod
    def create_tables(cls) -> None:
        """Creates all tables

        Keyword arguments:
        Return: None
        """

        cls.with_connection(Base.metadata.create_all)

    @classmethod
    def add_user(cls, new_user: dict):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        print(f"account added: {new_user}")
        return cls.with_session(create_user, new_user)

    @classmethod
    def add_account(cls, account_data: dict) -> Account:
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        print(f"account added: {account_data}")
        return cls.with_session(create_account, account_data)

    @classmethod
    def add_role(cls, role_data: dict):
        """adds a role object"""
        return cls.with_session(create_role, role_data)

    @classmethod
    def get_user(cls, pk: int) -> User | None:
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        return cls.with_session(lambda session, pk: session.get(User, pk), pk)

    @classmethod
    def get_account(cls, email: str) -> Account | None:
        """gets an account with the given pk of email

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        return cls.with_session(
            lambda session, email: session.query(Account)
            .options(joinedload(Account.user).joinedload(User.role),joinedload(Account.user).joinedload(User.organization))
            .get(email),
            email,
        )

    @classmethod
    def get_student(cls, pk: int) -> Student | None:
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        return cls.with_session(lambda session, pk: session.get(Student, pk), pk)

    @classmethod
    def get_roles(cls):
        """Gets all roles

        Keyword arguments:
        Return: List[Role]
        """

        return cls.with_session(lambda session: session.query(Role).all())

    @classmethod
    def get_organizations(cls):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        return cls.with_session(lambda session: session.query(Organization).all())

    @classmethod
    def get_student_by_account(cls, email: str) -> Student | None:
        """
        Fetch a student by the account's email using the associated user.

        Keyword arguments:
        email -- the account's email address
        Return: Student object or None
        """
        return cls.with_session(
            lambda session, email: session.query(Student)
            .join(User, Student.user_id == User.id)
            .join(Account, Account.user_id == User.id)
            .filter(Account.email == email)
            .first(),
            email,
        )

    @classmethod
    def get_student_by_user_id(cls, user_id: int) -> Student | None:
        """
        Fetch a student by the user id using the associated user.

        Keyword arguments:
        user_id -- the user's id
        Return: Student object or None
        """

        return cls.with_session(
            lambda session, user_id: session.query(Student)
            .join(User, Student.user_id == User.id)
            .filter(User.id == user_id)
            .first(),
            user_id,
        )

    def update_student(self, student_id, updated_data):
        student = self.get_student(student_id)
        if student:
            student.first_name = updated_data.get("first_name")
            student.last_name = updated_data.get("last_name")
            self.db.session.commit()
            return True
        return False

