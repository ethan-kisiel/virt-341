"""
Database models for the v341 application

TODO:
    - add constraints
    - finish/flesh out relationships
"""

from datetime import datetime as dt
from typing import Any

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


class Role(Base):
    """
    Represents the role that a user might have
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    role_name: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    role_permission: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)

    def __repr__(self):
        return f"<Role(id={self.id}, role_name={self.role_name}, role_permission={self.role_permission})>"


class Organization(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    organization_name: Mapped[str] = mapped_column(String(100), unique=True)

    users: Mapped["User"] = relationship("User", back_populates="organization")

    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.organization_name}, organization_name={self.organization_name}>"


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

    reporting_individual_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reporting_individual: Mapped["User"] = relationship(
        "User", foreign_keys=[reporting_individual_id]
    )

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    student: Mapped["Student"] = relationship(
        "Student", back_populates="form_341s", foreign_keys=[student_id]
    )

    def __repr__(self):
        return f"<form341(comment={self.comment}, place={self.place}, datetime={self.datetime}, reporting_individual_id={self.reporting_individual_id}, student_id={self.student_id})>"


class Student(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    phase: Mapped[int] = mapped_column(Integer(), default=0)

    class_flight: Mapped[str] = mapped_column(String(30), nullable=True)

    grade: Mapped[str] = mapped_column(String(3), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])

    supervisor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    supervisor: Mapped["User"] = relationship("User", foreign_keys=[supervisor_id])

    form_341s: Mapped["Form341"] = relationship("Form341", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.id}, phase={self.phase}, class_flight={self.class_flight}, user_id={self.user_id}, supervisor_id={self.supervisor_id})>"


class User(Base):
    """
    Represents the base/core user
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    last_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(100))
    middle_initial: Mapped[str] = mapped_column(String(3), nullable=True)

    rank: Mapped[str] = mapped_column(String(4), nullable=True)
    phone: Mapped[str] = mapped_column(String(16), nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship("Role")

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=True
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="users"
    )

    @property
    def qualified_name(self) -> str:
        return f"{self.rank} {self.last_name}, {self.first_name}, {self.middle_initial}".upper()

    def __repr__(self) -> str:
        return f"<User(id={self.id}, last_name={self.last_name}, first_name={self.first_name}, middle_initial={self.middle_initial}, grade={self.grade}, phone={self.phone}, role_id={self.role_id}, organization_id={self.organization_id})>"


class Account(Base, UserMixin):
    """
    Represents Accounts, which contain just account/login related info
    """

    __tablename__ = "accounts"

    email: Mapped[str] = mapped_column(String(100), primary_key=True)

    # this is the password hash
    countersign: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<Account(email={self.email}, countersign={self.countersign})>"

    @property
    def id(self):
        """
        computed property for flask login to read
        """

        return self.email
