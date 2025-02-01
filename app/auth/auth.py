from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.config import settings
import jwt
from pydantic import EmailStr
from app.users.dao import UserDAO
from app.exceptions import UserNotFoundExeption, UserPasswordIncorrectExeption


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# This is the function that will hash the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# This is the function that will verify the password
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# This is the function that will create the access token
def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# This is the function that will authenticate the user
async def authenticate_user(email:EmailStr, password:str):
    user = await UserDAO.find_by_filter(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user