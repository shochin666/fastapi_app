import os
from sqlalchemy.ext.asyncio import create_async_engine

# なぜmodels.memoからのBaseを使うのかわからない。db.pyからのBaseではいけないの？
from models.memo import Base
import asyncio

from utils.logger import get_logger

logger = get_logger()

base_dir = os.path.dirname(__file__)
DATABASE_URL = "sqlite+aiosqlite:///" + os.path.join(base_dir, "memodb.sqlite")

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_db():
    logger.debug("=== データベースの初期化を開始===")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.debug(">>> 既存のテーブルを削除しました")
        # 素朴な疑問なのだが、このcreate_allをした時に作成されるテーブルはmodels配下のファイルを元に作成されるのか？
        await conn.run_sync(Base.metadata.create_all)
        logger.debug(">>> 新しいテーブルを作成しました")

    # TODO: ログデータ（app.log）の初期化を実装


if __name__ == "__main__":
    asyncio.run(init_db())
