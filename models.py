# データベースモデル定義ファイル
# このファイルは、データベースのテーブル構造を定義します
# SQLAlchemyのORM（Object-Relational Mapping）を使用して、Pythonクラスでデータベーステーブルを表現します

# 必要なライブラリをインポート
from datetime import datetime  # 日時を扱うためのライブラリ
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey  # SQLAlchemyのデータ型
from sqlalchemy.orm import relationship  # テーブル間の関係を定義するため
from database import Base  # データベースのベースクラス
from schemas import ItemStatus  # アイテムの状態を表す列挙型


class Item(Base):
    """
    商品（アイテム）を表すデータベースモデル
    フリーマーケットで売買される商品の情報を管理します
    """
    # データベースのテーブル名を指定
    __tablename__ = 'items'

    # 商品のID（主キー：データベース内で一意に識別するための番号）
    id = Column(Integer, primary_key=True)
    # 商品名（必須項目）
    name = Column(String, nullable=False)
    # 価格（必須項目）
    price = Column(Integer, nullable=False)
    # 商品の説明（任意項目）
    description = Column(String, nullable=True)
    # 商品の状態（販売中/売り切れ）
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE)
    # 商品の作成日時（自動設定）
    created_at = Column(DateTime, default=datetime.now)
    # 商品の更新日時（自動更新）
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # 商品を出品したユーザーのID（外部キー：usersテーブルと関連付け）
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # ユーザーテーブルとの関係を定義（1対多：1人のユーザーが複数の商品を出品可能）
    user = relationship('User', back_populates='items')


class User(Base):
    """
    ユーザーを表すデータベースモデル
    フリーマーケットの利用者情報を管理します
    """
    # データベースのテーブル名を指定
    __tablename__ = 'users'

    # ユーザーのID（主キー）
    id = Column(Integer, primary_key=True)
    # ユーザー名（必須項目、重複不可）
    username = Column(String, nullable=False, unique=True)
    # パスワード（必須項目、ハッシュ化して保存）
    password = Column(String, nullable=False)
    # パスワードのソルト（セキュリティ強化のためのランダム文字列）
    salt = Column(String, nullable=False)
    # ユーザー登録日時（自動設定）
    created_at = Column(DateTime, default=datetime.now)
    # ユーザー情報更新日時（自動更新）
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # アイテムテーブルとの関係を定義（1対多：1人のユーザーが複数の商品を出品可能）
    items = relationship('Item', back_populates='user')
