from app.database import async_session_maker
from sqlalchemy import delete, select, insert, update
from sqlalchemy import insert


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(cls.model.id == id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    @classmethod
    async def find_by_filter(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            new_user = await session.execute(query)
            await session.commit()
            return new_user.mappings().one()
    

    @classmethod
    async def delete(cls, id:int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(
                cls.model.id == id
                ).returning(cls.model.__table__.columns)

            deleted = await session.execute(query)
            await session.commit()
            return deleted.mappings().one()
    