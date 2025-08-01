# データスキーマ定義ファイル
# このファイルは、APIでやり取りするデータの形式を定義します
# Pydanticライブラリを使用して、データの検証と変換を行います

# 必要なライブラリをインポート
from datetime import datetime  # 日時を扱うためのライブラリ
from enum import Enum  # 列挙型（選択肢を限定するための型）
from typing import Optional  # 任意項目を表す型
from pydantic import BaseModel, Field, ConfigDict  # データ検証と変換のためのライブラリ


class ItemStatus(Enum):
    """
    商品の状態を表す列挙型
    商品が販売中か売り切れかを管理します
    """
    ON_SALE = "ON_SALE"      # 販売中
    SOLD_OUT = "SOLD_OUT"    # 売り切れ


class ItemCreate(BaseModel):
    """
    商品作成時に使用するデータスキーマ
    新しい商品を登録する際に必要な情報を定義します
    """
    # 商品名（2文字以上20文字以下）
    name: str = Field(min_length=2, max_length=20, examples=['PC'])
    # 価格（0より大きい整数）
    price: int = Field(gt=0, examples=[10000])
    # 商品の説明（任意項目）
    description: Optional[str] = Field(None, examples=['美品です'])


class ItemUpdate(BaseModel):
    """
    商品更新時に使用するデータスキーマ
    既存の商品情報を更新する際に使用します（全て任意項目）
    """
    # 商品名（更新する場合のみ）
    name: Optional[str] = Field(None, min_length=2, max_length=20, examples=['PC'])
    # 価格（更新する場合のみ）
    price: Optional[int] = Field(None, gt=0, examples=[10000])
    # 商品の説明（更新する場合のみ）
    description: Optional[str] = Field(None, examples=['美品です'])
    # 商品の状態（更新する場合のみ）
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.SOLD_OUT])


class ItemResponse(BaseModel):
    """
    商品情報を返す際に使用するデータスキーマ
    APIレスポンスで商品情報を返す際の形式を定義します
    """
    # 商品のID
    id: int = Field(gt=0, examples=[1])
    # 商品名
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    # 価格
    price: int = Field(gt=0, examples=[10000])
    # 商品の説明
    description: Optional[str] = Field(None, examples=['備品です'])
    # 商品の状態
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    # 作成日時
    created_at: datetime
    # 更新日時
    updated_at: datetime
    # 出品者のユーザーID
    user_id: int

    # データベースモデルから自動的にデータを取得する設定
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    ユーザー作成時に使用するデータスキーマ
    新しいユーザーを登録する際に必要な情報を定義します
    """
    # ユーザー名（2文字以上）
    username: str = Field(min_length=2, examples=['users'])
    # パスワード（8文字以上）
    password: str = Field(min_length=8, examples=['test1234'])


class UserResponse(BaseModel):
    """
    ユーザー情報を返す際に使用するデータスキーマ
    APIレスポンスでユーザー情報を返す際の形式を定義します
    """
    # ユーザーのID
    id: int = Field(gt=0, examples=[1])
    # ユーザー名
    username: str = Field(min_length=2, examples=['user1'])
    # 登録日時
    created_at: datetime
    # 更新日時
    updated_at: datetime

    # データベースモデルから自動的にデータを取得する設定
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    認証トークンを表すデータスキーマ
    ログイン成功時に返される認証情報の形式を定義します
    """
    # メッセージ
    Message: str
    # アクセストークン（認証に使用する文字列）
    access_token: str
    # トークンの種類（通常は"bearer"）
    token_type: str


class DecodedToken(BaseModel):
    """
    デコードされたトークン情報を表すデータスキーマ
    認証トークンから取り出されたユーザー情報の形式を定義します
    """
    # ユーザー名
    username: str
    # ユーザーのID
    user_id: int
