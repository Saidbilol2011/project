from base.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime


class UserTable(BaseModel):
    __tablename__ = 'users_user'

    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str]
    gender: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    is_active: Mapped[bool]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)

    posts: Mapped[list["PostTable"]] = relationship("PostTable", back_populates="user")
    comments: Mapped[list["PostCommentTable"]] = relationship("PostCommentTable", back_populates="user")
    likes: Mapped[list["PostLikeTable"]] = relationship("PostLikeTable", back_populates="user")
    saves: Mapped[list["PostSaveTable"]] = relationship("PostSaveTable", back_populates="user")
