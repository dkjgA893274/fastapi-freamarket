# FastAPIアプリケーションのメインファイル
# このファイルは、Webアプリケーションのエントリーポイント（開始点）です
# アプリケーション全体の設定と、各機能（ルーター）を統合します

import time
# FastAPIフレームワークをインポート（Webアプリケーションを作成するためのライブラリ）
from fastapi import FastAPI, Request
# 各機能のルーター（URLの処理を担当するファイル）をインポート
from routers import item, auth
from fastapi.middleware.cors import CORSMiddleware
# 静的ファイルを提供するための機能をインポート
from fastapi.staticfiles import StaticFiles

# FastAPIアプリケーションのインスタンスを作成
# これがWebアプリケーションの本体になります
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 静的ファイル（HTML、CSS、JavaScript）を提供するための設定
# /static というURLパスで、staticフォルダ内のファイルにアクセスできるようになります
app.mount("/static", StaticFiles(directory="static"), name="static")

# アイテム関連の機能（商品の登録・更新・削除など）をアプリケーションに追加
app.include_router(item.router)
# 認証関連の機能（ユーザー登録・ログインなど）をアプリケーションに追加
app.include_router(auth.router)
