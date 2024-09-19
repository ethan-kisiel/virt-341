"""
Manages all database interactions
"""

from typing import Callable
from sqlalchemy import create_engine

from models import Base


class DatabaseManager:
    """
    Handles database interactions
    """

    database_url = ""
    engine = None

    @classmethod
    def with_engine(cls, callback: Callable, *args, **kwargs):
        """exectues callback with the class-based db engine

        Keyword arguments:
        cls -- class obj
        callback -- callable
        Return: None
        """

        with cls.engine.connect() as connection:
            callback(connection, *args, **kwargs)

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

        cls.with_engine(lambda connection: Base.metadata.create_all(connection))
