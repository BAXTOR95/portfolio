from datetime import datetime
from typing import List
from flask_login import UserMixin
from sqlalchemy import Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active or not.
        is_admin (bool): Indicates whether the user is an admin.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Project(db.Model):
    """
    Represents a project in the portfolio.

    Attributes:
        id (int): The unique identifier for the project.
        category (str): The category of the project.
        client (str): The client of the project.
        date (Date): The date of the project.
        url (str): The URL of the project.
        description (str): The description of the project.
        title (str): The title of the project.
    """

    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    client: Mapped[str] = mapped_column(String(128), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    url: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)

    images: Mapped[List["ProjectImage"]] = relationship(
        "ProjectImage", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project {self.title}>"


class ProjectImage(db.Model):
    """
    Represents an image related to a project.

    Attributes:
        id (int): The unique identifier for the project image.
        image_url (str): The URL of the image.
        project_id (int): The identifier of the project the image belongs to.
    """

    __tablename__ = "project_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(String(256), nullable=False)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('projects.id'), nullable=False
    )

    project: Mapped["Project"] = relationship("Project", back_populates="images")

    def __repr__(self) -> str:
        return f"<ProjectImage {self.image_url}>"
