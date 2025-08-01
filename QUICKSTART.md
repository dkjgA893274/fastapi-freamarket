# 🚀 クイックスタートガイド

このガイドでは、フリーマーケットAPIを**5分で**起動する方法を説明します。

## 📋 必要なもの

- **初期ユーザ**
  - ID: user1
  - Password: test1234
- **macOS/Linux/Windows**
- **Docker Desktop** (インストール済み)
- **Python 3.10以上** (インストール済み)

## ⚡ 超簡単セットアップ

### 1. セットアップスクリプトを実行

```bash
# スクリプトに実行権限を付与
chmod +x setup.sh

# セットアップを実行
./setup.sh
```

これだけで以下が自動で完了します：
- ✅ 仮想環境の作成
- ✅ 依存関係のインストール
- ✅ データベースの起動
- ✅ マイグレーションの実行

### 2. アプリケーションを起動

```bash
# 仮想環境をアクティベート
source freamarket/bin/activate

# アプリケーションを起動
uvicorn main:app --reload
```

### 3. ブラウザでアクセス

- **メインサイト**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs ← **ここから始めましょう！**

## 🎯 最初の一歩

### 1. API ドキュメントを開く
ブラウザで http://localhost:8000/docs にアクセス

### 2. ユーザーを登録
1. `/auth/signup` をクリック
2. "Try it out" をクリック
3. 以下のJSONを入力：
```json
{
  "username": "testuser",
  "password": "testpassword123"
}
```
4. "Execute" をクリック

### 3. ログインしてトークンを取得
1. `/auth/login` をクリック
2. "Try it out" をクリック
3. ユーザー名とパスワードを入力
4. "Execute" をクリック
5. レスポンスの `access_token` をコピー

### 4. 商品を出品
1. `/items` (POST) をクリック
2. "Try it out" をクリック
3. "Authorize" ボタンをクリック
4. トークンを入力（`Bearer YOUR_TOKEN`）
5. 商品情報を入力：
```json
{
  "name": "MacBook Pro",
  "price": 150000,
  "description": "美品のMacBook Proです"
}
```
6. "Execute" をクリック

### 5. 商品を確認
1. `/items` (GET) をクリック
2. "Try it out" → "Execute" をクリック
3. 出品した商品が表示されます！

## 🔧 トラブルシューティング

### よくある問題

#### 1. ポートが使用中
```bash
# 使用中のポートを確認
lsof -i :8000

# プロセスを終了
kill -9 <PID>
```

#### 2. データベースが起動しない
```bash
# Docker コンテナの状態確認
docker-compose ps

# コンテナを再起動
docker-compose restart
```

#### 3. マイグレーションエラー
```bash
# マイグレーションを再実行
alembic upgrade head
```

## 📚 次のステップ

- **README.md** を読んで詳細を理解
- **API ドキュメント** で全機能を試す
- **pgAdmin** (http://localhost:81) でデータベースを確認
- **テスト** を実行して動作確認

## 🆘 ヘルプ

問題が解決しない場合は：
1. **README.md** のトラブルシューティングを確認
2. **GitHub Issues** で質問を投稿
3. **API ドキュメント** でエンドポイントを確認

---

**🎉 お疲れ様でした！フリーマーケットAPIが正常に動作しています！**