"""
Database models for the v341 application
"""

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
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
    __tablename__ = "phases"


class Student(Base):
    __tablename__ = "students"


class Role(Base):
    __tablename__ = "roles"


class Organization(Base):
    __tablename__ = "organizations"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    last_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(100))
    middle_initial: Mapped[str] = mapped_column(String(3))

    grade: Mapped[str] = mapped_column(String(3))

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship("Role")

    organization: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
