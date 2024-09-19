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
    reporting_individual: Mapped["User"] = relationship("User")

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    student: Mapped["Student"] = relationship("Student", back_populates="form_341s")
    
def __init__(self, comment, place, datetime, reporting_individual_id, student_id):
    self.comment = comment 
    self.place = place
    self.datetime = datetime
    self.reporting_individual_id = reporting_individual_id
    self.student_id = student_id 
    
def __repr__(self):
    return f"<form341(comment={self.comment}, place={self.place}, datetime={self.datetime}, reporting_individual_id={self.reporting_individual_id}, student_id={self.student_id})>"


class Student(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    phase: Mapped[int] = mapped_column(Integer(), default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")
    
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    supervisor: Mapped["User"] = relationship("User")

    form_341s: Mapped["Form341"] = relationship("Form341", back_populates="student")

    def __init__(self, id, phase, user_id, supervisor_id):
        self.id = id 
        self.phase = phase
        self.user_id = user_id
        self.supervisor_id = supervisor_id
       
    def __repr__(self):
        return f"<Student(id={self.id}, phase={self.phase}, user_id={self.user_id}, supervisor_id={self.supervisor_id})>"


class Role(Base):
    """
    Represents the role that a user might have
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    role_name: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    role_permission: Mapped[int] = mapped_column(Integer(), nullable=True, unique=True)

    def __init__(self, id, role_name, role_permission):
        self.id = id
        self.role_name = role_name
        self.role_permission = role_permission 
                 
    def __repr__(self):
        return f"<Role(id={self.id}, role_name={self.role_name}, role_permission={self.role_permission})>"


class Organization(Base):
    """
    Represents the organization which users can be assigned to
    """

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    class_flight: Mapped[str] = mapped_column(String(30), nullable=True, unique=True) 
    
    users: Mapped["User"] = relationship("User", back_populates="organization")

    def __init__(self, id, name, class_flight):
        self.id = id
        self.name = name
        self.class_flight = class_flight 

    def __repr__(self):
        return f"<Organization(id={self.id}, role_name={self.role_name}, role_permission={self.role_permission})>"


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
    phone: Mapped[str] = mapped_column(String(16), nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship("Role")

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="users"
    )

    def __init__(self, id, last_name, first_name, middle_initial, grade, phone, role_id, organization_id):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name 
        self.middle_initial = middle_initial
        self.grade = grade
        self.phone = phone
        self.role_id = role_id
        self.organization_id = organization_id

    def __repr__(self, ) -> str:
        
        lf = f"last_name={self.last_name}, first_name={self.first_name},"
        mi = f"middle_initial={self.middle_initial},"

        return f"<User({' '.join([lf, mi])} grade={self.grade}, id={self.id}, phone={self.phone},role_id={self.role_id}, organization_id={self.organization_id})>"


class Account(Base, UserMixin):
    """
    Represents Accounts, which contain just account/login related info
    """

    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")
    
    email: Mapped[str] = mapped_column(String(100), primary_key=True)

    # this is the password hash
    countersign: Mapped[str] = mapped_column(String(100))
    
    def __init__(self,email ,countersign):
        self.countersign = countersign
        self.email = email

    def __repr__(self) -> str:
        return f"<Account(email={self.email}, countersign={self.countersign})>"
