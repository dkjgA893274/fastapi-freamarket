# サンプルテストファイル
# このファイルは、テストの書き方の例を示すためのファイルです
# 実際のテストではありませんが、テストの基本的な構造を理解するために使用できます

# 必要なライブラリをインポート
from fastapi.testclient import TestClient  # FastAPIのテストクライアント


def test_example():
    """
    サンプルテスト関数
    この関数は、テストの基本的な書き方を示すための例です
    実際のテストではありません
    """
    # テストの例：1 + 1 = 2 であることを確認
    assert 1 + 1 == 2


def test_example_with_client(client_fixture: TestClient):
    """
    テストクライアントを使用したサンプルテスト関数
    この関数は、HTTPクライアントを使用したテストの例を示します
    実際のテストではありません
    """
    # テストの例：アプリケーションが正常に起動していることを確認
    # 実際のアプリケーションでは、特定のエンドポイントをテストします
    response = client_fixture.get("/")
    # レスポンスのステータスコードが200（成功）であることを確認
    assert response.status_code == 200