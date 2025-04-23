import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

base_dir = os.path.dirname(__file__)
DATABASE_URL = "sqlite+aiosqlite:///" + os.path.join(base_dir, "memodb.sqlite")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Async function for DI.
async def get_dbsession():
    async with async_session() as session:
        # Yielded session make it possible to operate DB.
        # WHY USE YIELD?
        # Because user have to make session open during operating DB.
        # So, this function provide session with yield in async with statement.
        yield session
