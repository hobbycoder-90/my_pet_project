from sqlalchemy import select

from app.users.models import Users
from app.database import async_session_maker
from app.dao.basedao import BaseDAO


class UserDAO(BaseDAO):
    model = Users
    