from models.users import UserTable
from passlib.context import CryptContext
from sqlalchemy.orm import Session

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return bcrypt_context.hash(password)

def authenticate_user(username: str, password: str, session: Session):
    user = session.query(UserTable).filter(UserTable.username == username).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False
    
    return user