# 🛍️ フリーマーケットAPI

このプロジェクトは、FastAPIを使用したフリーマーケットアプリケーションのバックエンドAPIです。ユーザーが商品を出品・購入できるWebサービスを提供します。

## 📋 目次

- [機能概要](#機能概要)
- [技術スタック](#技術スタック)
- [セットアップ手順](#セットアップ手順)
- [使用方法](#使用方法)
- [API仕様](#api仕様)
- [データベース設計](#データベース設計)
- [セキュリティ](#セキュリティ)
- [開発環境](#開発環境)
- [トラブルシューティング](#トラブルシューティング)

## 機能概要

### 主要機能
- **初期ユーザ**
  - ID: user1
  - Password: test1234
- **ユーザー管理**: アカウント登録・ログイン・認証
- **商品管理**: 商品の出品・編集・削除・検索
- **セキュリティ**: JWT認証による安全なAPIアクセス
- **データベース**: PostgreSQLによる永続化

### ユーザーストーリー
1. ユーザーがアカウントを登録
2. ログイン(バックエンドでJWTトークンを取得)
3. 商品を出品・管理
4. 他のユーザーの商品を検索・閲覧

### ターゲットユーザー

#### 主要ユーザー層
- **フリーマーケットの出品者**
  - **目的**: 自分が販売したい商品を登録・管理する
  - **使用場面**:
    - 不要になった家電、家具、衣類などを売りたい
    - 趣味で作った手作り品を販売したい
    - 引っ越しや断捨離で処分したい物品を売りたい

- **フリーマーケットの管理者・運営者**
  - **目的**: サイト全体の商品管理とユーザー管理
  - **使用場面**:
    - 出品された商品の審査・承認
    - 不適切な商品の削除
    - ユーザーアカウントの管理

#### 想定される利用シーン
1. **個人の断捨離**: 使わなくなった物を売って収入を得る
2. **趣味の副業**: 手作り品や収集品を販売
3. **地域コミュニティ**: 近隣住民同士での物品交換
4. **環境配慮**: リサイクル・リユースの促進

#### システムの目的
従来のフリーマーケットをデジタル化し、より多くの人々が簡単に物品の売買を行えるようにすることを目的としています。

## 技術スタック

| 技術 | バージョン | 用途 |
|------|------------|------|
| **FastAPI** | 最新 | Web APIフレームワーク |
| **Python** | 3.10+ | プログラミング言語 |
| **PostgreSQL** | 16 | データベース |
| **SQLAlchemy** | 2.0+ | ORM（データベース操作） |
| **Pydantic** | 2.0+ | データ検証・シリアライゼーション |
| **JWT** | - | 認証トークン |
| **Docker** | - | コンテナ化 |
| **Alembic** | - | データベースマイグレーション |

## セットアップ手順

### 前提条件
- Docker と Docker Compose がインストールされていること
- Python 3.10以上がインストールされていること

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd fastapi-freamarket
```

### 2. 仮想環境の作成とアクティベート
```bash
# 仮想環境を作成
python -m venv freamarket

# 仮想環境をアクティベート
# macOS/Linux:
source freamarket/bin/activate
# Windows:
# freamarket\Scripts\activate
```

### 3. 依存関係のインストール
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] python-multipart python-dotenv alembic
```

### 4. データベースの起動
```bash
# Docker ComposeでPostgreSQLとpgAdminを起動
docker-compose up -d
```

### 5. データベースマイグレーションの実行
```bash
# マイグレーションを実行
alembic upgrade head
```

### 6. アプリケーションの起動
```bash
# 開発サーバーを起動
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. アクセス確認
- **API**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs
  - ブラウザからAPIを実行・検証ができる
- **pgAdmin**: http://localhost:81 (email: fastapi@example.com, password: password)
  - DBをブラウザがら操作できる

## 使用方法

### 1. ユーザー登録
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'
```

### 2. ログイン
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword123"
```

### 3. 商品の出品
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro",
    "price": 150000,
    "description": "美品のMacBook Proです"
  }'
```

### 4. 商品の検索
```bash
# 全商品取得
curl "http://localhost:8000/items"

# 商品名で検索
curl "http://localhost:8000/items/?name=MacBook"
```

## API仕様

### 認証エンドポイント

#### POST /auth/signup
ユーザー登録
```json
{
  "username": "string (2文字以上)",
  "password": "string (8文字以上)"
}
```

#### POST /auth/login
ログイン（JWTトークン取得）
```json
{
  "username": "string",
  "password": "string"
}
```

### 商品エンドポイント

#### GET /items
全商品取得（認証不要）

#### GET /items/{id}
特定商品取得（認証必要）

#### GET /items/?name={name}
商品名検索（認証不要）

#### POST /items
商品出品（認証必要）
```json
{
  "name": "string (2-20文字)",
  "price": "integer (0より大きい)",
  "description": "string (オプション)"
}
```

#### PUT /items/{id}
商品更新（認証必要）
```json
{
  "name": "string (オプション)",
  "price": "integer (オプション)",
  "description": "string (オプション)",
  "status": "ON_SALE | SOLD_OUT (オプション)"
}
```

#### DELETE /items/{id}
商品削除（認証必要）

## データベース設計

### テーブル構造

#### users テーブル
| カラム | 型 | 説明 |
|--------|----|----|
| id | INTEGER | 主キー |
| username | VARCHAR | ユーザー名（一意） |
| password | VARCHAR | ハッシュ化されたパスワード |
| salt | VARCHAR | パスワードハッシュ化用ソルト |
| created_at | TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | 更新日時 |

#### items テーブル
| カラム | 型 | 説明 |
|--------|----|----|
| id | INTEGER | 主キー |
| name | VARCHAR | 商品名 |
| price | INTEGER | 価格 |
| description | VARCHAR | 商品説明 |
| status | ENUM | 商品ステータス（ON_SALE/SOLD_OUT） |
| user_id | INTEGER | 出品者ID（外部キー） |
| created_at | TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | 更新日時 |

### リレーションシップ
- **User** (1) ←→ (多) **Item**: 1人のユーザーが複数の商品を出品可能

## セキュリティ

### 認証・認可
- **JWT認証**: トークンベースの認証システム
- **パスワードハッシュ化**: PBKDF2 + ソルトによる安全なパスワード保存
- **ユーザー権限**: 自分のリソースのみ操作可能

### データ検証
- **Pydantic**: 厳密な入力データ検証
- **SQLAlchemy**: SQLインジェクション対策
- **型安全性**: Pythonの型ヒントによる安全性確保

## 開発環境

### テスト実行
```bash
# テストを実行
pytest

# カバレッジ付きでテスト実行
pytest --cov=.
```

### コードフォーマット
```bash
# コードをフォーマット
black .

# インポートを整理
isort .
```

### リンター
```bash
# コード品質チェック
flake8 .
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. データベース接続エラー
```bash
# PostgreSQLコンテナの状態確認
docker-compose ps

# コンテナの再起動
docker-compose restart postgres
```

#### 2. マイグレーションエラー
```bash
# マイグレーション履歴確認
alembic history

# 特定のマイグレーションまで戻す
alembic downgrade <revision>
```

#### 3. ポート競合
```bash
# 使用中のポート確認
lsof -i :8000
lsof -i :5432
lsof -i :81

# プロセス終了
kill -9 <PID>
```

#### 4. 仮想環境の問題
```bash
# 仮想環境の再作成
rm -rf freamarket
python -m venv freamarket
source freamarket/bin/activate
pip install -r requirements.txt
```

### ログ確認
```bash
# アプリケーションログ
uvicorn main:app --reload --log-level debug

# Dockerログ
docker-compose logs postgres
docker-compose logs pgadmin
```

## プロジェクト構造

```
fastapi-freamarket/
├── main.py                 # アプリケーションエントリーポイント
├── models.py              # データベースモデル
├── schemas.py             # Pydanticスキーマ
├── database.py            # データベース設定
├── docker-compose.yml     # Docker設定
├── alembic.ini           # マイグレーション設定
├── docs/                  # ドキュメント
│   ├── user-stories.md    # ユーザーストーリー
│   ├── system-overview.md # システム概要
│   └── user-guide.md      # ユーザーガイド
├── routers/              # APIルーター
│   ├── auth.py           # 認証エンドポイント
│   └── item.py           # 商品エンドポイント
├── cruds/                # ビジネスロジック
│   ├── auth.py           # 認証ロジック
│   └── item.py           # 商品ロジック
├── migrations/           # データベースマイグレーション
│   └── versions/         # マイグレーションファイル
└── docker/              # Docker関連ファイル
    ├── postgres/         # PostgreSQL設定
    └── pgadmin/          # pgAdmin設定
```

## ドキュメント

詳細なドキュメントは `docs/` ディレクトリにあります：

- **[ユーザーストーリー](docs/user-stories.md)**: ターゲットユーザーと機能要件
- **[システム概要](docs/system-overview.md)**: アーキテクチャと技術仕様
- **[ユーザーガイド](docs/user-guide.md)**: エンドユーザー向け操作ガイド

## コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## サポート

問題や質問がある場合は、以下の方法でお問い合わせください：

- GitHub Issues: バグ報告や機能要望
- ドキュメント: `/docs` エンドポイントでAPI仕様を確認

---

**Happy Coding! 🚀**