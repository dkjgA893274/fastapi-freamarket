#!/bin/bash

# フリーマーケットAPI セットアップスクリプト
echo "🛍️ フリーマーケットAPI セットアップを開始します..."

# 色付きの出力関数
print_success() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ️  $1\033[0m"
}

# 前提条件チェック
print_info "前提条件をチェックしています..."

# Python バージョンチェック
if ! command -v python3 &> /dev/null; then
    print_error "Python3 がインストールされていません"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    print_error "Python 3.10以上が必要です。現在のバージョン: $python_version"
    exit 1
fi

print_success "Python バージョン: $python_version"

# Docker チェック
if ! command -v docker &> /dev/null; then
    print_error "Docker がインストールされていません"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose がインストールされていません"
    exit 1
fi

print_success "Docker と Docker Compose が利用可能です"

# 仮想環境の作成
print_info "仮想環境を作成しています..."
if [ ! -d "freamarket" ]; then
    python3 -m venv freamarket
    print_success "仮想環境 'freamarket' を作成しました"
else
    print_info "仮想環境 'freamarket' は既に存在します"
fi

# 仮想環境のアクティベート
print_info "仮想環境をアクティベートしています..."
source freamarket/bin/activate

# 依存関係のインストール
print_info "依存関係をインストールしています..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "依存関係のインストールが完了しました"
else
    print_error "依存関係のインストールに失敗しました"
    exit 1
fi

# データベースの起動
print_info "データベースを起動しています..."
docker-compose up -d

if [ $? -eq 0 ]; then
    print_success "データベースが起動しました"
else
    print_error "データベースの起動に失敗しました"
    exit 1
fi

# データベースの準備を待つ
print_info "データベースの準備を待っています..."
sleep 10

# マイグレーションの実行
print_info "データベースマイグレーションを実行しています..."
alembic upgrade head

if [ $? -eq 0 ]; then
    print_success "マイグレーションが完了しました"
else
    print_error "マイグレーションに失敗しました"
    exit 1
fi

# セットアップ完了
echo ""
print_success "セットアップが完了しました！"
echo ""
echo "📋 次のステップ:"
echo "1. 仮想環境をアクティベート: source freamarket/bin/activate"
echo "2. アプリケーションを起動: uvicorn main:app --reload"
echo "3. ブラウザでアクセス: http://localhost:8000"
echo "4. API ドキュメント: http://localhost:8000/docs"
echo "5. pgAdmin: http://localhost:81 (email: fastapi@example.com, password: password)"
echo ""
echo "🎉 フリーマーケットAPI の準備が整いました！"