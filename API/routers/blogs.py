import aiofiles
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from schemas.blogs import CreateLikeSchema, CreateSaveSchema, PatchCommentSchema, PostDetailSchema, CreateCommentSchema
from database import get_session
from dependencies.users.user import UserHandling
from models.blogs import PostCommentTable, PostImageTable, PostLikeTable, PostSaveTable, PostTable, CategoryTable
from models.users import UserTable
from directories.posts import create_dir as post_create_dir, create_post_images_dir


router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


# GET Requests
@router.get("/posts")
async def get_posts(session: Session = Depends(get_session)):

    categories = session.execute(
        select(CategoryTable)).scalars().all()

    posts = session.execute(
        select(PostTable).join(UserTable).join(CategoryTable)).scalars().all()
    return posts, categories


@router.get("/posts/{post_id}", response_model=PostDetailSchema)
async def get_post_by_id(post_id: int, session: Session = Depends(get_session)):
    post = session.execute(
        select(PostTable)
        .options(
            selectinload(PostTable.images), 
            selectinload(PostTable.comments), 
            selectinload(PostTable.saves), 
            selectinload(PostTable.likes)
        )
        .where(PostTable.id == post_id)).scalar()
    return post


# POST Requests (Creating)
@router.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(
    main_image: UploadFile= File(...),
    images: list[UploadFile]= File(default=None),
    title: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    session: Session = Depends(get_session),
    user: UserTable = Depends(UserHandling().employee),
):
    post = PostTable(
        user_id=user.id,
        main_image=None,
        title=title,
        description=description,
        category_id=category_id
    )
    session.add(post)
    session.flush()

    for image in images:
        post_images = PostImageTable(
            post_id=post.id,
            image=None
        )
        file_dir_for_django = None
        if post_images is not None:
            image_data = await create_post_images_dir(post_id=post.id, filename=image.filename)
            content = image.file.read()
            async with aiofiles.open(image_data['file_full_path'], 'wb') as out_file:
                file_dir_for_django = image_data['file_dir'] + image.filename
                await out_file.write(content)
        post_images.image = file_dir_for_django
        session.add(post_images)

    file_dir_for_django = None
    if main_image is not None:
        file_data = await post_create_dir(post_id=post.id, filename=main_image.filename)
        content = main_image.file.read()
        async with aiofiles.open(file_data['file_full_path'], 'wb') as out_file:
            file_dir_for_django = file_data['file_dir'] + main_image.filename
            await out_file.write(content)
    post.main_image = file_dir_for_django
    session.commit()
    session.refresh(post)

    return {
        "message": "Created!"
    }


# Like, Save, Comment Endpoints
@router.post('/like/{post_id}', status_code=status.HTTP_201_CREATED)
async def create_like( 
    data: CreateLikeSchema,
    session: Session = Depends(get_session), 
    user: UserTable = Depends(UserHandling().user)
):

    post = session.execute(select(PostTable).where(PostTable.id == data.post_id)).scalar()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing_like = session.execute(select(PostLikeTable).where(PostLikeTable.post_id == data.post_id, PostLikeTable.user_id == user.id)).scalar()

    if existing_like:
        session.delete(existing_like)
        session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Like is Deleted')


    new_like = PostLikeTable(
        user_id=user.id,
        post_id=post.id,
    )
    if not existing_like:
        session.add(new_like)
        session.commit()
        session.refresh(new_like)

    return {
        "message": "Like Created!"
    }


@router.post('/save/{post_id}', status_code=status.HTTP_201_CREATED)
async def create_save(
    data: CreateSaveSchema,
    session: Session = Depends(get_session), 
    user: UserTable = Depends(UserHandling().user)
):

    post = session.execute(select(PostTable).where(PostTable.id == data.post_id)).scalar()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing_save = session.execute(select(PostSaveTable).where(PostSaveTable.post_id == data.post_id, PostSaveTable.user_id == user.id)).scalar()

    if existing_save:
        session.delete(existing_save)
        session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Save is Deleted')


    new_save = PostSaveTable(
        user_id=user.id,
        post_id=post.id,
    )
    if not existing_save:
        session.add(new_save)
        session.commit()
        session.refresh(new_save)

    return {
        "message": "Save Created!"
    }


@router.post("/comment/{post_id}", status_code=status.HTTP_201_CREATED)
async def write_comment(
    data: CreateCommentSchema,
    session: Session = Depends(get_session),
    user: UserTable = Depends(UserHandling().user)
):

    post = session.query(PostTable).filter(PostTable.id == data.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = PostCommentTable(
        user_id=user.id,
        post_id=data.post_id,
        text=data.text
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)

    return {
        "message": "Comment Wrote!"
    }

# Patch
@router.patch("/change_comment/{post_id}", status_code=status.HTTP_201_CREATED)
async def change_comment(
    data: PatchCommentSchema,
    session: Session = Depends(get_session),
    user: UserTable = Depends(UserHandling().user)
):  
    post = session.query(PostTable).filter(PostTable.id == data.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")