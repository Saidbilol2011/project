from fastapi import APIRouter, Depends, status, HTTPException
from dependencies.JWT.handlers import JWTHandler
from dependencies.users.user import UserHandling
from utils import authenticate_user, hash_password
from database import get_session
from sqlalchemy.orm import Session
from models.users import UserTable
from sqlalchemy import select
from schemas.users import UserCreateSchema, UserLoginSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=['auth'])


# GET Requests
@router.get('/users', response_model=list[UserSchema])
async def get_users(role: str = None, session: Session =  Depends(get_session)):
    if not role:
        users = session.execute(select(UserTable)).scalars().all()
    else:
        users = session.execute(select(UserTable).where(
            UserTable.role == role
        )).scalars().all()
    
    return users


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def me(user: UserSchema = Depends(UserHandling().user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not Authenticated !")
    return user


# POST Requests (Creating)
@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreateSchema, session: Session = Depends(get_session)):
    try:
        user = UserTable(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=True,
            role=data.role,
            email=data.email,
            phone=data.phone,
            gender=data.gender,
            password=hash_password(data.password)
        )
        session.add(user)
        session.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already Created !")

    return "created successfully !"


@router.post('/signin', status_code=status.HTTP_200_OK)
async def signin(data: UserLoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(username=data.username, password=data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not Authenticated !")
    token = JWTHandler().create_token(username=user.username, user_id=user.id)
    return {
        "access_token": token,
        "type": "Bearer"
    }
