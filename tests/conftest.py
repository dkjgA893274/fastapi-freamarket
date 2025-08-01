# テスト設定ファイル
# このファイルは、テスト実行時の共通設定とテストデータの準備を行います
# pytestフレームワークでテストを実行する際の環境を整えます

# 必要なライブラリをインポート
import pytest  # テストフレームワーク
from fastapi.testclient import TestClient  # FastAPIのテストクライアント
from sqlalchemy import create_engine  # データベースエンジン作成
from sqlalchemy.orm import sessionmaker  # データベースセッション作成
from database import get_db, Base  # データベース設定
from main import app  # FastAPIアプリケーション
from models import User, Item  # データベースモデル
from schemas import ItemStatus  # 商品状態の列挙型


# テスト用データベースのURL（SQLiteを使用）
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# テスト用データベースエンジンを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# テスト用データベースセッションを作成
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    テスト用のデータベースセッションを取得する関数
    本番環境のデータベースではなく、テスト用のデータベースを使用します
    """
    try:
        # テスト用データベースセッションを作成
        db = TestingSessionLocal()
        yield db
    finally:
        # テスト終了時にデータベース接続を閉じる
        db.close()


# アプリケーションの依存関係をテスト用に置き換え
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client_fixture():
    """
    テスト用のHTTPクライアントを作成するフィクスチャ
    各テストで使用するHTTPクライアントを提供します
    """
    # テスト用データベースのテーブルを作成
    Base.metadata.create_all(bind=engine)

    # テスト用HTTPクライアントを作成
    with TestClient(app) as client:
        yield client

    # テスト終了時にテスト用データベースのテーブルを削除
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_fixture():
    """
    テスト用のデータベースセッションを作成するフィクスチャ
    各テストで使用するデータベースセッションを提供します
    """
    # テスト用データベースのテーブルを作成
    Base.metadata.create_all(bind=engine)

    # テスト用データベースセッションを作成
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # テスト終了時にデータベースセッションを閉じる
        db.close()
        # テスト用データベースのテーブルを削除
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_fixture(db_fixture):
    """
    テスト用のユーザーデータを作成するフィクスチャ
    各テストで使用するユーザー情報を提供します
    """
    # テスト用ユーザーを作成
    user = User(
        username="testuser",
        password="hashed_password",
        salt="test_salt"
    )
    # データベースにユーザーを追加
    db_fixture.add(user)
    # 変更を保存
    db_fixture.commit()
    # ユーザー情報を返す
    return user


@pytest.fixture
def item_fixture(db_fixture, user_fixture):
    """
    テスト用の商品データを作成するフィクスチャ
    各テストで使用する商品情報を提供します
    """
    # テスト用商品を作成（2個）
    item1 = Item(
        name="PC1",
        price=10000,
        description="テスト用PC1",
        status=ItemStatus.ON_SALE,
        user_id=user_fixture.id
    )
    item2 = Item(
        name="PC2",
        price=20000,
        description="テスト用PC2",
        status=ItemStatus.ON_SALE,
        user_id=user_fixture.id
    )
    # データベースに商品を追加
    db_fixture.add(item1)
    db_fixture.add(item2)
    # 変更を保存
    db_fixture.commit()
    # 商品情報を返す
    return [item1, item2]
