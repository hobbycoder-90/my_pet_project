from fastapi import Request, Depends
import jwt
from jwt.exceptions import InvalidTokenError
from app.config import settings
from datetime import datetime, timezone
from app.users.dao import UserDAO
from app.exceptions import TokenExpiredException, TokenIsNotFound, IncorrectTokenFormatException, UserIDIsNotInTokenJWTException, UserNotFoundExeption


def get_token(request: Request):
    token = request.cookies.get("login_access_token")
    if not token:
        raise TokenIsNotFound
    
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
    except InvalidTokenError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIDIsNotInTokenJWTException
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundExeption
    
    return user

