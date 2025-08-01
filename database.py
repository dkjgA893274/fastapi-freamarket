# データベース接続設定ファイル
# このファイルは、PostgreSQLデータベースとの接続を管理します
# SQLAlchemyというライブラリを使用してデータベース操作を行います

# SQLAlchemyライブラリから必要な機能をインポート
from sqlalchemy import create_engine  # データベースエンジンを作成するため
from sqlalchemy.orm import sessionmaker, declarative_base  # データベースセッションとベースクラスを作成するため
from config import get_settings


# PostgreSQLデータベースへの接続URL
# 形式: postgresql://ユーザー名:パスワード@ホスト:ポート/データベース名
SQLALCHEMY_DATABASE_URL = get_settings().sqlalchemy_database_url

# データベースエンジンを作成（データベースとの接続を管理）
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# データベースセッションを作成するためのファクトリ（工場）
# autocommit=False: 自動的に変更を保存しない
# autoflush=False: 自動的にデータベースを更新しない
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemyのベースクラスを作成
# このクラスを継承してデータベースのテーブルを定義します
Base = declarative_base()

def get_db():
    """
    データベースセッションを取得する関数
    この関数は、FastAPIの依存関係注入システムで使用されます
    """
    # 新しいデータベースセッションを作成
    db = SessionLocal()
    try:
        # セッションを呼び出し元に提供
        yield db
    finally:
        # 処理が終了したら、必ずデータベース接続を閉じる
        # これにより、データベースリソースの無駄遣いを防ぎます
        db.close()
