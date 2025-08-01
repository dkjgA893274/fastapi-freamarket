# 認証関連のAPIエンドポイント定義ファイル
# このファイルは、ユーザー登録・ログインなどの認証機能を提供します
# FastAPIのルーターを使用して、認証関連のURLパスと処理を関連付けます

# 必要なライブラリをインポート
from datetime import timedelta  # 時間の計算を行うためのライブラリ

from typing import Annotated  # 型注釈をより詳細に書くためのライブラリ
from fastapi import APIRouter, Depends, HTTPException  # FastAPIの機能
from fastapi.security import OAuth2PasswordRequestForm  # パスワード認証フォーム
from sqlalchemy.orm import Session  # データベースセッション
from starlette import status  # HTTPステータスコード
from cruds import auth as auth_cruds  # 認証関連のビジネスロジック
from schemas import UserCreate, UserResponse, Token  # データスキーマ
from database import get_db  # データベース接続取得関数


# 認証関連のAPIルーターを作成（URLの先頭に"/auth"が付きます）
router = APIRouter(prefix='/auth', tags=['auth'])

# データベースセッションの依存関係を定義（自動的にデータベース接続を提供）
DbDependency = Annotated[Session, Depends(get_db)]
# パスワード認証フォームの依存関係を定義（ログイン時に使用）
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post(
    '/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(db: DbDependency, user_create: UserCreate):
    """
    ユーザー登録APIエンドポイント
    POST /auth/signup でアクセスすると、新しいユーザーを登録します
    ユーザー名とパスワードを受け取り、データベースに保存します
    """
    return auth_cruds.create_user(db, user_create)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(db: DbDependency, form_data: FormDependency):
    """
    ユーザーログインAPIエンドポイント
    POST /auth/login でアクセスすると、ユーザー認証を行い、アクセストークンを返します
    ユーザー名とパスワードを確認し、正しければ認証トークンを発行します
    """
    # ユーザー名とパスワードで認証を行う
    user = auth_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # 認証に失敗した場合は401エラーを返す
        raise HTTPException(status_code=401, detail='Incorrect username or password')

    # 認証成功時、20分間有効なアクセストークンを作成
    token = auth_cruds.create_access_token(user.username, user.id, timedelta(minutes=20))
    # 認証成功メッセージとトークンを返す
    return {'Message': 'Successful Authentication!', 'access_token': token, 'token_type': 'bearer'}
