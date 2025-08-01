# 認証関連のビジネスロジックファイル
# このファイルは、ユーザー認証・パスワード管理・トークン生成などの認証機能を担当します
# セキュリティを考慮したパスワードハッシュ化とJWTトークン管理を行います

# 必要なライブラリをインポート
from datetime import datetime, timedelta  # 日時と時間計算
import hashlib  # パスワードのハッシュ化
import base64  # バイナリデータのエンコード/デコード
import os  # ランダムデータ生成
from typing import Annotated  # 型注釈
from fastapi import Depends  # 依存関係注入
from fastapi.security import OAuth2PasswordBearer  # OAuth2認証スキーム
from jose import jwt, JWTError  # JWTトークンの生成・検証
from sqlalchemy.orm import Session  # データベースセッション
from schemas import UserCreate, DecodedToken  # データスキーマ
from models import User  # ユーザーモデル
from config import get_settings


# JWTトークンの暗号化アルゴリズム
ALGORITHM = 'HS256'
# JWTトークンの暗号化キー（本番環境では環境変数から取得すべき）
SECRET_KEY = get_settings().secret_key

# OAuth2パスワード認証スキーム（ログインエンドポイントを指定）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def create_user(db: Session, user_create: UserCreate):
    """
    新しいユーザーを作成する関数
    パスワードを安全にハッシュ化してデータベースに保存します
    """
    # パスワードのソルト（塩）を生成（セキュリティ強化のためのランダム文字列）
    salt = base64.b64encode(os.urandom(32))
    # パスワードをハッシュ化（PBKDF2アルゴリズムを使用）
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', user_create.password.encode(), salt, 1000
    ).hex()

    # 新しいユーザーを作成
    new_user = User(
        username = user_create.username,  # ユーザー名
        password = hashed_password,       # ハッシュ化されたパスワード
        salt = salt.decode()              # ソルト（文字列として保存）
    )
    # データベースにユーザーを追加
    db.add(new_user)
    # 変更を保存
    db.commit()

    return new_user


def authenticate_user(db: Session, username: str, password: str):
    """
    ユーザー認証を行う関数
    ユーザー名とパスワードを確認し、正しければユーザー情報を返します
    """
    # ユーザー名でユーザーを検索
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # ユーザーが見つからない場合はNoneを返す
        return None

    # 入力されたパスワードをハッシュ化（保存されているソルトを使用）
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), user.salt.encode(), 1000
    ).hex()
    # ハッシュ化されたパスワードを比較
    if user.password != hashed_password:
        # パスワードが一致しない場合はNoneを返す
        return None

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """
    アクセストークン（JWT）を生成する関数
    ユーザー情報と有効期限を含むトークンを作成します
    """
    # トークンの有効期限を計算
    expires = datetime.now() + expires_delta
    # トークンに含める情報（ペイロード）
    payload = {'sub': username, 'id': user_id, 'exp': expires}
    # JWTトークンを生成
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    現在のユーザー情報を取得する関数
    JWTトークンからユーザー情報を復号化して返します
    """
    try:
        # JWTトークンを復号化
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # ペイロードからユーザー情報を取得
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            # 必要な情報が不足している場合はNoneを返す
            return None
        # デコードされたトークン情報を返す
        return DecodedToken(username=username, user_id=user_id)
    except JWTError:
        # トークンの復号化に失敗した場合はエラーを発生
        raise JWTError