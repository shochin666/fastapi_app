from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.memo as memo_schema
import models.memo as memo_model
from datetime import datetime

from utils.logger import get_logger

logger = get_logger()


# 新規登録
async def insert_memo(
    db_session: AsyncSession, memo_data: memo_schema.InsertAndUpdateMemoSchema
) -> memo_model.Memo:
    logger.debug("=== 新規登録：開始 ===")
    # スキーマからモデルにデータ変換する際は必ず以下の形で行う
    # 1. スキーマを作成
    # 2. モデルにdumpしたスキーマを渡す
    # 3. AsyncSessionを使ってadd->commit->refresh
    # なお、refreshはDBに変更が反映された後の最新の属性をオブジェクトに反映するためのもので、
    # DBが自動的に付与するIDなどを使用している場合などは必須。今回ならreturnしているnew_memo
    # オブジェクトがDBによってauto-incrementされたIDを持つ必要があるので必須。
    new_memo = memo_model(**memo_data.model_dump())
    # db_session.addはテーブルにデータを追加する操作。更新時には行わない。
    db_session.add(new_memo)
    await db_session.commit()
    await db_session.refresh(new_memo)
    logger.debug(">>> データ追加完了")
    return new_memo


# 全件取得
async def get_memos(db_session: AsyncSession) -> list[memo_model.Memo]:
    logger.debug("=== 全件取得：開始 ===")
    # 全てのMemoオブジェクトを取得するSQLを実行
    result = await db_session.execute(select(memo_model.Memo))
    # result: クエリの結果（各行ごと）
    # scalars(): クエリの結果の各行を個別のMemoオブジェクトとして抽出
    # all(): 1つに合体しているMemoオブジェクトを行ごとの要素に分け、リストとして返す
    memos = result.scalars().all()
    logger.debug(">>> データ全件取得完了")
    return memos


# IDによる取得
async def get_memo_by_id(
    db_session: AsyncSession, memo_id: int
) -> memo_model.Memo | None:
    logger.debug("=== IDによる取得：開始")
    result = await db_session.execute(
        select(memo_model).where(memo_model.Memo.memo_id == memo_id)
    )
    # 存在しなければNoneが返る
    memo = result.scalars().first()
    logger.debug(">>> データ取得完了")
    return memo


# 更新処理
async def update_memo(
    db_session: AsyncSession,
    memo_id: int,
    target_data: memo_schema.InsertAndUpdateMemoSchema,
) -> memo_model.Memo | None:
    logger.debug("=== データ更新：開始 ===")
    memo = await get_memo_by_id(db_session, memo_id)
    if memo:
        # スキーマのプロパティには.xxで普通にアクセスできる
        memo.title = target_data.title
        memo.description = target_data.description
        memo.updated_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(memo)
        logger.debug(">>> データ更新完了")

    return memo


# 削除処理
async def delete_memo(db_session: AsyncSession, memo_id: int) -> memo_model.Memo | None:
    logger.debug("=== データ削除：開始 ===")
    # 更新をするにしても、削除するにしてもまずは対象のオブジェクトをDBから持ってくる必要がある
    memo = await get_memo_by_id(db_session, memo_id)
    if memo:
        await db_session.delete(memo)
        await db_session.commit()
        logger.debug(">>> データ削除完了")

    return memo
