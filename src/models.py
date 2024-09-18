"""
Database models for the v341 application

TODO:
    - add constraints
    - finish/flesh out relationships
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


class Form341(Base):
    """
    Represents the 341 forms
    """

    __tablename__ = "form341s"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # TODO: Add relationships for reporting authority and the student

    # date_time: Mapped[dt] TODO: Figure out how to map a datetime

    comment: Mapped[str] = mapped_column(String(1000))
    place: Mapped[str] = mapped_column(String(80))


class Phase(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "phases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100))


class Student(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User")

    phase_id: Mapped[int] = mapped_column(ForeignKey("phase.id"))
    phase: Mapped["Phase"] = relationship("Phase")


class Role(Base):
    """
    Represents the role that a user might have
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    role_name: Mapped[str] = mapped_column(String(30))
    role_permission: Mapped[int] = mapped_column(Integer)


class Organization(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    # TODO: add admin account(s) field

    users: Mapped["User"] = relationship("User", back_populates="organization")


class User(Base):
    """
    Represents the base/core user
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    last_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(100))
    middle_initial: Mapped[str] = mapped_column(String(3))

    grade: Mapped[str] = mapped_column(String(3))

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship("Role")

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="users"
    )


class Account(Base):
    """
    Represents Accounts, which contain just account/login related info
    """

    email: Mapped[str] = mapped_column(String(100))

    # this is the password hash
    countersign: Mapped[str] = mapped_column(String(100))
