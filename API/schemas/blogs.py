from typing import Optional
from pydantic import BaseModel
from schemas.users import UserSchema 


# Response Schemas
class SimpleUserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class CategroySchemas(BaseModel):
    id: int
    name: str


class PostImagesSchemas(BaseModel):
    id: int
    image: Optional[str] | None = None


class PostCommentsSchemas(BaseModel):
    id: int
    post_id: int
    text: str
    user: SimpleUserSchema

    class Config:
        from_attributes = True


class PostLikesSchemas(BaseModel):
    id: int
    post_id: int
    user: SimpleUserSchema

    class Config:
        from_attributes = True


class PostSavesSchemas(BaseModel):
    id: int
    post_id: int
    user: SimpleUserSchema

    class Config:
        from_attributes = True


class PostDetailSchema(BaseModel):
    id: int
    title: str
    description: str
    main_image: str
    images: list[PostImagesSchemas] | None = None
    comments: list[PostCommentsSchemas]
    likes: list[PostLikesSchemas]
    saves: list[PostSavesSchemas]
    user: SimpleUserSchema

    class Config:
        from_attributes = True


class PostRensponseSchema(BaseModel):
    id: int
    title: str
    main_image: str
    user: SimpleUserSchema
    category: CategroySchemas

    class Config:
        from_attributes = True


# Create Schemas
class CreateLikeSchema(BaseModel):
    post_id: int


class CreateSaveSchema(BaseModel):
    post_id: int


class CreateCommentSchema(BaseModel):
    post_id: int
    text: str


# Patch
class PatchCommentSchema(BaseModel):
    post_id: int
    text: str
