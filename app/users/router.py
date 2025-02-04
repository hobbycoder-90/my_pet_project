from fastapi import APIRouter, Depends
from sqlalchemy import update

from app.users.schema import UserCreateSchema, UserResponseSchema, UserUpdatePasswordSchema, UserUpdateEmailSchema, UserUpdateSchema, UserSchema
from app.users.models import Users
from app.users.dao import UserDAO
from app.exceptions import UserAlreadyExistsExeption, UserAlreadyExistsExeption, UserNotFoundExeption
from app.auth.auth import get_password_hash
from app.auth.dependencies import get_current_user
from app.database import async_session_maker




router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/all", response_model=list[UserSchema], status_code=200)
async def get_all_users(current_user: UserResponseSchema = Depends(get_current_user)):
    return await UserDAO.find_all()


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: UserResponseSchema = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserSchema, status_code=200)
async def get_user(user_id: int, current_user: UserResponseSchema = Depends(get_current_user)):
    result = await UserDAO.find_one_or_none(id=user_id)
    if not result:
        raise UserNotFoundExeption 
    return result


@router.post("/register", response_model=UserSchema, status_code=201)
async def register_user(user_data: UserCreateSchema):
    exist_user = await UserDAO.find_one_or_none(email=user_data.email)
    if exist_user:
        raise UserAlreadyExistsExeption
    
    hashed_password = get_password_hash(user_data.hashed_password)
    user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    return user

@router.patch("/pass", response_model=UserResponseSchema, status_code=200)
async def update_user_password_me(user_data: UserUpdatePasswordSchema, current_user: UserResponseSchema = Depends(get_current_user)):
    async with async_session_maker() as session:
        query = update(Users).where(Users.id == current_user.id).values( 
            hashed_password=get_password_hash(user_data.hashed_password)
            ).returning(Users.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one()

@router.patch("/email", response_model=UserResponseSchema, status_code=200)
async def update_user_email_me(user_data: UserUpdateEmailSchema, current_user: UserResponseSchema = Depends(get_current_user)):
    async with async_session_maker() as session:
        new_email_control = await UserDAO.find_one_or_none(email=user_data.email)
        if new_email_control:
            raise UserAlreadyExistsExeption
        query = update(Users).where(Users.id == current_user.id).values( 
            email=user_data.email
            ).returning(Users.__table__.columns)
        result = await session.execute(query)
        await session.commit()

        return result.mappings().one()

@router.put("/email&pass", response_model=UserResponseSchema, status_code=200)
async def update_user_email_pass_me(user_data: UserUpdateSchema, current_user: UserResponseSchema = Depends(get_current_user)):
    async with async_session_maker() as session:
        new_email_control = await UserDAO.find_one_or_none(email=user_data.email)
        if new_email_control:
            raise UserAlreadyExistsExeption
        
        query = update(Users).where(Users.id == current_user.id).values(
            hashed_password=get_password_hash(user_data.hashed_password),
            email=user_data.email
            ).returning(Users.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one()
    
@router.delete("/my_user_items", response_model=UserSchema, status_code=202)
async def delete_user_me(current_user: UserResponseSchema = Depends(get_current_user)):
    return await UserDAO.delete(current_user.id)
        