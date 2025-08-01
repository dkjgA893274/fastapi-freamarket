# 商品（アイテム）関連のテストファイル
# このファイルは、フリーマーケットアプリの「商品API」が正しく動作するかを自動でチェックするテストコードです。
# 初心者向け解説：
# - テストを書くことで、アプリの機能が壊れていないか自動で確認できます。
# - 例えば「商品を追加したら、ちゃんと一覧に増えるか？」などを自動で検証します。
# - テストは「安心して開発を進めるためのお守り」です。
#
# このファイルの主な内容：
# 1. 商品一覧取得、商品詳細取得、商品検索、商品追加、商品更新、商品削除のテスト
# 2. 正常な場合（期待通り動く）と異常な場合（エラーになる）の両方を確認
# 3. テスト用のデータベース・クライアントはconftest.pyで用意されています

from fastapi.testclient import TestClient  # FastAPIのテスト用クライアント

# --- 商品一覧取得のテスト ---
def test_find_all(client_fixture: TestClient):
    """
    全ての商品を取得するAPIのテスト
    GET /items エンドポイントが正しく動作することを確認します
    初心者向け：
    - APIに「商品一覧を見せて」とリクエストし、2件返ってくるか確認します。
    """
    response = client_fixture.get("/items")
    assert response.status_code == 200  # 200は「成功」の意味
    items = response.json()
    assert len(items) == 2  # テスト用データが2件なので2件返るはず

# --- 商品詳細取得（正常系）のテスト ---
def test_find_byid_正常系(client_fixture: TestClient):
    """
    指定されたIDの商品を取得するAPIの正常系テスト
    初心者向け：
    - 「ID=1の商品を見せて」とリクエストし、ちゃんと返ってくるか確認します。
    """
    response = client_fixture.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1

# --- 商品詳細取得（異常系）のテスト ---
def test_find_byid_異常系(client_fixture: TestClient):
    """
    存在しないIDの商品を取得しようとしたときのテスト
    初心者向け：
    - 「ID=10の商品を見せて」とリクエストし、存在しないのでエラーになるか確認します。
    """
    response = client_fixture.get("/items/10")
    assert response.status_code == 404  # 404は「見つからない」の意味
    assert response.json()["detail"] == "Item not found"

# --- 商品名で検索するテスト ---
def test_find_by_name(client_fixture: TestClient):
    """
    商品名で検索するAPIのテスト
    初心者向け：
    - 「PC1」という名前の商品を検索し、1件だけ返ってくるか確認します。
    """
    response = client_fixture.get("/items/?name=PC1")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "PC1"

# --- 商品追加のテスト ---
def test_create(client_fixture: TestClient):
    """
    新しい商品を作成するAPIのテスト
    初心者向け：
    - 「スマホ」という商品を新しく追加し、ちゃんと登録されるか確認します。
    - 追加後、商品一覧が1件増えているかもチェックします。
    """
    response = client_fixture.post(
        "/items", json={"name": "スマホ", "price": 30000, "user_id": 1}
    )
    assert response.status_code == 201  # 201は「新規作成成功」の意味
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "スマホ"
    assert item["price"] == 30000

    # 商品一覧を再取得して、新しい商品が追加されていることを確認
    response = client_fixture.get("/items")
    assert len(response.json()) == 3

# --- 商品更新（正常系）のテスト ---
def test_update_正常系(client_fixture: TestClient):
    """
    商品情報を更新するAPIの正常系テスト
    初心者向け：
    - 「ID=1の商品名と価格を変更したい」とリクエストし、ちゃんと反映されるか確認します。
    """
    response = client_fixture.put("/items/1", json={"name": "スマホ", "price": 5000})
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "スマホ"
    assert item["price"] == 5000

# --- 商品更新（異常系）のテスト ---
def test_update_異常系(client_fixture: TestClient):
    """
    存在しないIDの商品を更新しようとしたときのテスト
    初心者向け：
    - 「ID=10の商品を更新したい」とリクエストし、存在しないのでエラーになるか確認します。
    """
    response = client_fixture.put("/items/10", json={"name": "スマホ", "price": 5000})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not updated"

# --- 商品削除（正常系）のテスト ---
def test_delete_正常系(client_fixture: TestClient):
    """
    商品を削除するAPIの正常系テスト
    初心者向け：
    - 「ID=1の商品を削除したい」とリクエストし、ちゃんと消えるか確認します。
    - 削除後、商品一覧が1件減っているかもチェックします。
    """
    response = client_fixture.delete("/items/1")
    assert response.status_code == 200
    # 商品一覧を再取得して、商品が削除されていることを確認
    response = client_fixture.get("/items")
    assert len(response.json()) == 1

# --- 商品削除（異常系）のテスト ---
def test_delete_異常系(client_fixture: TestClient):
    """
    存在しないIDの商品を削除しようとしたときのテスト
    初心者向け：
    - 「ID=10の商品を削除したい」とリクエストし、存在しないのでエラーになるか確認します。
    """
    response = client_fixture.delete("/items/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not deleted"

# --- 補足：テストの実行方法 ---
# - ターミナルで「pytest」と入力すると、全てのテストが自動で実行されます。
# - 1つのテストだけ実行したい場合は「pytest tests/test_item.py::test_find_all」のように指定できます。
# - テストが全て緑色（成功）なら、アプリの基本機能は壊れていません！
