# 商品（アイテム）関連のAPIエンドポイント定義ファイル
# このファイルは、商品の作成・取得・更新・削除などのAPI機能を提供します
# FastAPIのルーターを使用して、URLパスと処理を関連付けます

# 必要なライブラリをインポート
from typing import Annotated  # 型注釈をより詳細に書くためのライブラリ
from fastapi import APIRouter, Path, Query, HTTPException, Depends  # FastAPIの機能
from sqlalchemy.orm import Session  # データベースセッション
from starlette import status  # HTTPステータスコード
from cruds import item as item_cruds, auth as auth_cruds  # ビジネスロジック（CRUD操作）
from schemas import ItemCreate, ItemUpdate, ItemResponse, DecodedToken  # データスキーマ
from database import get_db  # データベース接続取得関数


# データベースセッションの依存関係を定義（自動的にデータベース接続を提供）
DbDependency = Annotated[Session, Depends(get_db)]

# ユーザー認証の依存関係を定義（自動的にログインユーザー情報を提供）
UserDependency = Annotated[DecodedToken, Depends(auth_cruds.get_current_user)]

# 商品関連のAPIルーターを作成（URLの先頭に"/items"が付きます）
router = APIRouter(prefix="/items", tags=["Items"])


@router.get('', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    """
    全ての商品を取得するAPIエンドポイント
    GET /items でアクセスすると、データベース内の全ての商品情報を返します
    """
    return item_cruds.find_all(db)


@router.get('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db:DbDependency, user: UserDependency, id: int=Path(gt=0)):
    """
    指定されたIDの商品を取得するAPIエンドポイント
    GET /items/{id} でアクセスすると、指定されたIDの商品情報を返します
    認証が必要で、自分の商品のみ取得可能です
    """
    # 指定されたIDの商品を検索（自分の商品のみ）
    found_item = item_cruds.find_by_id(db, id, user.user_id)
    if not found_item:
        # 商品が見つからない場合は404エラーを返す
        raise HTTPException(status_code=404, detail='Item not found')
    return found_item


@router.get('/', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(db:DbDependency, name: str = Query(min_length=2, max_length=20)):
    """
    商品名で検索するAPIエンドポイント
    GET /items/?name=検索したい商品名 でアクセスすると、商品名に一致する商品を返します
    """
    return item_cruds.find_by_name(db, name)

@router.post('', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create(db:DbDependency, user: UserDependency, item_create: ItemCreate):
    """
    新しい商品を作成するAPIエンドポイント
    POST /items でアクセスすると、新しい商品をデータベースに登録します
    認証が必要で、ログインユーザーが商品の出品者になります
    """
    return item_cruds.create(db, item_create, user.user_id)


@router.put('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDependency, user: UserDependency, item_update: ItemUpdate, id: int = Path(gt=0)):
    """
    商品情報を更新するAPIエンドポイント
    PUT /items/{id} でアクセスすると、指定されたIDの商品情報を更新します
    認証が必要で、自分の商品のみ更新可能です
    """
    # 指定されたIDの商品を更新（自分の商品のみ）
    updated_item = item_cruds.update(db, id, item_update, user.user_id)
    if not updated_item:
        # 更新に失敗した場合は404エラーを返す
        raise HTTPException(status_code=404, detail='Item not updated')
    return updated_item


@router.delete('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDependency, user: UserDependency, id: int = Path(gt=0)):
    """
    商品を削除するAPIエンドポイント
    DELETE /items/{id} でアクセスすると、指定されたIDの商品を削除します
    認証が必要で、自分の商品のみ削除可能です
    """
    # 指定されたIDの商品を削除（自分の商品のみ）
    deleted_item = item_cruds.delete(db, id, user.user_id)
    if not deleted_item:
        # 削除に失敗した場合は404エラーを返す
        raise HTTPException(status_code=404, detail='Item not deleted')
    return deleted_item
