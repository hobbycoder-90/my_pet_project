from fastapi import APIRouter, Response, Request
from app.users.schema import UserCreateSchema
from app.auth.auth import authenticate_user, create_access_token
from app.exceptions import UserUnauthorizedExeption, TokenIsNotFound

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", status_code=200)
async def login_user(response: Response, user_data: UserCreateSchema):
    user = await authenticate_user(user_data.email, user_data.hashed_password)
    if not user:
        raise UserUnauthorizedExeption
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("login_access_token", access_token, httponly=True) #httponly=True - cookie can't be accessed by JavaScript
    return {
        "message": "Successfully logged in",
        "access_token": access_token
        }


@router.post("/logout", status_code=200)
async def logout_user(response: Response, requests: Request):
    get_cookie = requests.cookies.get("login_access_token")
    if not get_cookie:
        raise TokenIsNotFound
    response.delete_cookie("login_access_token")
    return {
        "message": "Successfully logged out"
        }

