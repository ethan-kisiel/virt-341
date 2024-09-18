"""
Database models for the v341 application
"""

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """
    Base model class
    """

    # TODO: implement id, date created, last updated fields


class Phase(Base):
    pass


class Student(Base):
    pass


class Role(Base):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)

    last_name = Column("last_name", String)
    first_name = Column("first_name", String)
    middle_initial = Column("middle_initial", String)

    grade = Column("grade", String)

    role_id = Column("role_id", ForeignKey)
