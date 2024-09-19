"""
Manages all database interactions
"""

from typing import Any
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base
from models import Account
from models import User
from models import Student
from models import Form341


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

        with Session(cls.engine) as session:
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
    def get_user(cls, pk: int) -> User | None:
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        return cls.with_session(lambda session, pk: session.get(User, pk), pk)

    @classmethod
    def create_user(cls):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

    @classmethod
    def get_account(cls, email: str) -> Account | None:
        """gets an account with the given pk of email

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        return cls.with_session(
            lambda session, email: session.get(Account, email), email
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
    def get_341s_by_date(cls, dt) -> list[Form341]:
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

    @classmethod
    def create_341_for_student(cls, form: Form341):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
