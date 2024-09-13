"""
Manages all database interactions
"""

from typing import Callable
from sqlalchemy import create_engine


class DatabaseManager:
    """
    Handles database interactions
    """

    database_route = ""
    engine = create_engine(database_route)

    @classmethod
    def with_engine(cls, callback: Callable):
        """exectues callback with the class-based db engine

        Keyword arguments:
        cls -- class obj
        callback -- callable
        Return: None
        """

        with cls.engine.connect() as connection:
            callback(connection)
