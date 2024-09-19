"""
Database models for the v341 application

TODO:
    - add constraints
    - finish/flesh out relationships
"""

from datetime import datetime as dt

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from flask_login import UserMixin


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
    place: Mapped[str] = mapped_column(String(120))

    datetime: Mapped[dt] = mapped_column(DateTime)

    reporting_individual_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    reporting_individual: Mapped["User"] = relationship("User")

    student_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    student: Mapped["Student"] = relationship("Student", back_populates="form_341s")


class Student(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    phase: Mapped[int] = mapped_column(Integer(), default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User")

    form_341s: Mapped["Form341"] = relationship("Form341", back_populates="student")


class Role(Base):
    """
    Represents the role that a user might have
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    role_name: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    role_permission: Mapped[int] = mapped_column(Integer(), nullable=True, unique=True)


class Organization(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # TODO: add admin account(s) field

    users: Mapped["User"] = relationship("User", back_populates="organization")


class User(Base):
    """
    Represents the base/core user
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    last_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(100))
    middle_initial: Mapped[str] = mapped_column(String(3))

    grade: Mapped[str] = mapped_column(String(3))

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship("Role")

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="users"
    )

    def __repr__(self) -> str:
        lf = f"last_name: {self.last_name}, first_name: {self.first_name},"
        mi = f"middle_initial: {self.middle_initial},"

        return f"<User: [{' '.join([lf, mi])} grade: {self.grade}]>"


class Account(Base, UserMixin):
    """
    Represents Accounts, which contain just account/login related info
    """

    __tablename__ = "accounts"

    email: Mapped[str] = mapped_column(String(100), primary_key=True)

    # this is the password hash
    countersign: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"<Account: [email: {self.email}]>"
