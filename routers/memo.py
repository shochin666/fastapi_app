from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.memo import InsertAndUpdateMemoSchema, MemoSchema, ResponseSchema
import cruds.memo as memo_crud
import db

# tagsはSawggerUIのためのタグ
router = APIRouter(tags=["Memos"], prefix="/memos")


# メモ新規登録用エンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_memo(
    memo: InsertAndUpdateMemoSchema,
    # Depends(db.get_dbsession)により、毎回、独自のセッションを新たに生成・クローズを行うので
    # 従来のようにセッションをグローバルに定義していちいち処理ごとにセッションを閉じるコードを記述しなくてもよい。
    # また、独自のセッションを確立するので、リクエストの競合などが発生しづらくなる。
    db: AsyncSession = Depends(db.get_dbsession),
):
    try:
        await memo_crud.insert_memo(db, memo)
        # スキーマをreturnするとフロントエンドにJSON形式でレスポンスできる。->直感的。
        return ResponseSchema(message="メモが正常に登録されました")
    except Exception as e:
        raise HTTPException(status_code=400, detail="メモの登録に失敗しました")


# メモ情報全件取得用エンドポイント
@router.get("/", response_model=list[MemoSchema])
async def get_memos_list(db: AsyncSession = Depends(db.get_dbsession)):
    memos = await memo_crud.get_memos(db)
    return memos


# 特定のメモ情報取得用エンドポイント
@router.get("/{memo_id}", response_model=MemoSchema)
async def get_memo_detail(memo_id: int, db: AsyncSession = Depends(db.get_dbsession)):
    memo = await memo_crud.get_memo_by_id(db, memo_id)
    if not memo:
        # raiseした時はreturnは不要
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    return memo


# 特定のメモ情報更新用エンドポイント
@router.put("/{memo_id}", response_model=ResponseSchema)
async def modify_memo(
    memo_id: int,
    memo: InsertAndUpdateMemoSchema,
    db: AsyncSession = Depends(db.get_dbsession),
):
    updated_memo = await memo_crud.update_memo(db, memo_id, memo)
    if not updated_memo:
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="メモが正常に更新されました")


# 特定のメモを削除するエンドポイント
@router.delete("/{memo_id}", response_model=ResponseSchema)
async def remove_memo(memo_id: int, db: AsyncSession = Depends(db.get_dbsession)):
    result = await memo_crud.delete_memo(db, memo_id)
    if not result:
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="メモが正常に削除されました")
