from app.database import async_session_maker
from sqlalchemy import delete, select, insert
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
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
    
    #@classmethod
    #async def addee(cls, **data):
    #    try:
    #        query = insert(cls.model).values(**data).returning(cls.model.id)
    #        async with async_session_maker() as session:
    #            result = await session.execute(query)
    #            await session.commit()
    #            return result.mappings().first()
    #    except (SQLAlchemyError, Exception) as e:
    #        if isinstance(e, SQLAlchemyError):
    #            msg = "Database Exc: Cannot insert data into table"
    #        elif isinstance(e, Exception):
    #            msg = "Unknown Exc: Cannot insert data into table"
#
    #        logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
    #        return None

    
    #@classmethod
    #async def add_bulk(cls, *data):
    #    # Для загрузки массива данных [{"id": 1}, {"id": 2}]
    #    # мы должны обрабатывать его через позиционные аргументы *args.
    #    try:
    #        query = insert(cls.model).values(*data).returning(cls.model.id)
    #        async with async_session_maker() as session:
    #            result = await session.execute(query)
    #            await session.commit()
    #            return result.mappings().first()
    #    except (SQLAlchemyError, Exception) as e:
    #        if isinstance(e, SQLAlchemyError):
    #            msg = "Database Exc"
    #        elif isinstance(e, Exception):
    #            msg = "Unknown Exc"
    #        msg += ": Cannot bulk insert data into table"
#
    #        logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
    #        return None
    
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