# フリーマーケットシステム - システム概要

## システムアーキテクチャ

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   フロントエンド   │    │    バックエンド    │    │   データベース    │
│                 │    │                 │    │                 │
│  HTML/CSS/JS    │◄──►│    FastAPI      │◄──►│   PostgreSQL    │
│                 │    │                 │    │                 │
│  Static Files   │    │  Python 3.10+   │    │   SQLAlchemy    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Docker Compose │    │   JWT Auth      │    │   Alembic       │
│                 │    │                 │    │                 │
│  Containerized  │    │  Token-based    │    │  Migration      │
│   Environment   │    │   Security      │    │   Management    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## システム構成

### フロントエンド
- **技術**: HTML5, CSS3, JavaScript (Vanilla)
- **特徴**:
  - レスポンシブデザイン
  - モダンなUI/UX
  - 静的ファイル配信
- **ファイル構成**:
  ```
  static/
  ├── index.html      # メインページ
  ├── css/
  │   └── style.css   # スタイルシート
  └── js/
      └── app.js      # JavaScript機能
  ```

### バックエンド
- **技術**: FastAPI (Python 3.10+)
- **特徴**:
  - RESTful API
  - 自動APIドキュメント生成
  - 型安全性
  - 高速なパフォーマンス
- **ファイル構成**:
  ```
  ├── main.py         # アプリケーションエントリーポイント
  ├── models.py       # データベースモデル
  ├── schemas.py      # Pydanticスキーマ
  ├── database.py     # データベース設定
  ├── config.py       # 設定管理
  ├── routers/        # APIルーター
  │   ├── auth.py     # 認証エンドポイント
  │   └── item.py     # 商品エンドポイント
  └── cruds/          # ビジネスロジック
      ├── auth.py     # 認証ロジック
      └── item.py     # 商品ロジック
  ```

### データベース
- **技術**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0+
- **マイグレーション**: Alembic
- **テーブル構成**:
  ```
  users テーブル
  ├── id (主キー)
  ├── username (一意)
  ├── password (ハッシュ化)
  ├── salt
  ├── created_at
  └── updated_at

  items テーブル
  ├── id (主キー)
  ├── name
  ├── price
  ├── description
  ├── status
  ├── user_id (外部キー)
  ├── created_at
  └── updated_at
  ```

## セキュリティ設計

### 認証・認可
- **JWT認証**: トークンベースの認証システム
- **パスワードハッシュ化**: PBKDF2 + ソルト
- **ユーザー権限**: 自分のリソースのみ操作可能

### データ保護
- **入力値検証**: Pydanticによる厳密な検証
- **SQLインジェクション対策**: SQLAlchemy ORM
- **型安全性**: Pythonの型ヒント

## 開発環境

### Docker構成
```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: fastapi_example
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - ./docker/postgres:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: fastapi@example.com
      PGADMIN_DEFAULT_PASSWORD: password
    ports:
      - "81:80"
    depends_on:
      - postgres
```

### 開発ワークフロー
1. **環境構築**: Docker Composeでインフラ起動
2. **マイグレーション**: AlembicでDBスキーマ適用
3. **アプリケーション起動**: uvicornでFastAPI起動
4. **開発・テスト**: ホットリロード対応

## デプロイメント

### 本番環境要件
- **Webサーバー**: Nginx/Apache
- **WSGIサーバー**: Gunicorn
- **データベース**: PostgreSQL
- **コンテナ**: Docker/Kubernetes

### CI/CD
- **テスト**: pytest
- **コード品質**: flake8, black
- **セキュリティ**: 依存関係スキャン

## パフォーマンス最適化

### 現在実装済み
- **データベースインデックス**: 主キー、外部キー
- **効率的なクエリ**: SQLAlchemy ORM
- **軽量なフロントエンド**: バニラJavaScript

### 今後の改善予定
- **キャッシュ**: Redis
- **CDN**: 静的ファイル配信
- **データベース最適化**: クエリ最適化
- **画像最適化**: 圧縮・リサイズ

## 監視・ログ

### ログ管理
- **アプリケーションログ**: uvicorn
- **データベースログ**: PostgreSQL
- **アクセスログ**: Nginx

### 監視項目
- **レスポンス時間**: API応答時間
- **エラー率**: 500エラー発生率
- **リソース使用量**: CPU、メモリ、ディスク
- **データベース性能**: クエリ実行時間

## 拡張性

### 水平スケーリング
- **ロードバランサー**: 複数インスタンス
- **データベース**: レプリケーション
- **キャッシュ**: Redis クラスター

### 垂直スケーリング
- **リソース増強**: CPU、メモリ
- **ストレージ**: SSD、高速ディスク
- **ネットワーク**: 高帯域幅

## 障害対策

### バックアップ
- **データベース**: 定期バックアップ
- **設定ファイル**: バージョン管理
- **ログ**: 長期保存

### 復旧手順
1. **データベース復旧**: バックアップから復元
2. **アプリケーション再起動**: 設定変更反映
3. **動作確認**: ヘルスチェック