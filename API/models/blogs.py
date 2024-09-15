from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from base.models import BaseModel

class CategoryTable(BaseModel):
    __tablename__ = "blogs_category"
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    posts: Mapped[list["PostTable"]] = relationship("PostTable", back_populates="category")


class PostImageTable(BaseModel):
    __tablename__ = "blogs_postimage"

    post_id: Mapped[int] = mapped_column(ForeignKey("blogs_post.id"))
    image: Mapped[str] = mapped_column(nullable=False)

    post: Mapped["PostTable"] = relationship("PostTable", back_populates="images")


class PostCommentTable(BaseModel):
    __tablename__ = 'blogs_postcomment'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'), nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('blogs_post.id'), nullable=False, index=True)
    text: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="comments")
    post: Mapped["PostTable"] = relationship("PostTable", back_populates="comments")


class PostLikeTable(BaseModel):
    __tablename__ = "blogs_postlike"

    user_id: Mapped[int] = mapped_column(ForeignKey("users_user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("blogs_post.id"))

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="likes")
    post: Mapped["PostTable"] = relationship("PostTable", back_populates="likes")


class PostSaveTable(BaseModel):
    __tablename__ = "blogs_postsave"

    user_id: Mapped[int] = mapped_column(ForeignKey("users_user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("blogs_post.id"))

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="saves")
    post: Mapped["PostTable"] = relationship("PostTable", back_populates="saves")



class PostTable(BaseModel):
    __tablename__ = "blogs_post"

    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    title: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("blogs_category.id"))
    main_image: Mapped[str]

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="posts")
    category: Mapped["CategoryTable"] = relationship("CategoryTable", back_populates="posts")
    images: Mapped[list["PostImageTable"]] = relationship("PostImageTable", back_populates="post")
    comments: Mapped[list["PostCommentTable"]] = relationship("PostCommentTable", back_populates="post")
    likes: Mapped[list["PostLikeTable"]] = relationship("PostLikeTable", back_populates="post")
    saves: Mapped[list["PostSaveTable"]] = relationship("PostSaveTable", back_populates="post")
