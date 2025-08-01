# 商品（アイテム）関連のビジネスロジックファイル
# このファイルは、商品のデータベース操作（CRUD: Create, Read, Update, Delete）を担当します
# データベースとの直接的なやり取りを行い、商品データの管理を行います

# 必要なライブラリをインポート
from sqlalchemy.orm import Session  # データベースセッション
from schemas import ItemCreate, ItemUpdate  # データスキーマ（入力データの形式）
from models import Item  # データベースモデル（商品テーブル）


def find_all(db: Session):
    """
    全ての商品を取得する関数
    データベース内の全ての商品情報を返します
    """
    return db.query(Item).all()


def find_by_id(db: Session, id: int, user_id: int):
    """
    指定されたIDの商品を取得する関数
    特定の商品IDとユーザーIDに一致する商品を検索します
    自分の商品のみ取得可能です
    """
    return db.query(Item).filter(Item.id == id).filter(Item.user_id == user_id).first()


def find_by_name(db: Session, name: str):
    """
    商品名で検索する関数
    商品名に指定された文字列が含まれる商品を全て取得します
    部分一致検索が可能です（例：「PC」で検索すると「PC1」「PC2」などがヒット）
    """
    return db.query(Item).filter(Item.name.like(f'%{name}%')).all()


def create(db: Session, item_create: ItemCreate, user_id: int):
    """
    新しい商品を作成する関数
    受け取った商品情報とユーザーIDを使って、新しい商品をデータベースに保存します
    """
    # 受け取った商品情報をデータベースモデルに変換
    new_item = Item(
        **item_create.model_dump(),  # 商品情報を展開
        user_id=user_id  # 出品者のユーザーIDを設定
    )
    # データベースに新しい商品を追加
    db.add(new_item)
    # 変更を保存
    db.commit()
    return new_item


def update(db: Session, id: int, item_update: ItemUpdate, user_id: int):
    """
    商品情報を更新する関数
    指定されたIDの商品情報を更新します（自分の商品のみ更新可能）
    """
    # 更新対象の商品を取得（自分の商品のみ）
    item = find_by_id(db, id, user_id=user_id)
    if item is None:
        # 商品が見つからない場合はNoneを返す
        return None

    # 各項目を更新（Noneの場合は元の値を保持）
    item.name = item.name if item_update.name is None else item_update.name
    item.price = item.price if item_update.price is None else item_update.price
    item.description = (
        item.description
        if item_update.description is None
        else item_update.description
    )
    item.status = (
        item.status if item_update.status is None else item_update.status
    )
    # 更新された商品をデータベースに保存
    db.add(item)
    # 変更を保存
    db.commit()
    return item


def delete(db: Session, id: int, user_id: int):
    """
    商品を削除する関数
    指定されたIDの商品を削除します（自分の商品のみ削除可能）
    """
    # 削除対象の商品を取得（自分の商品のみ）
    item = find_by_id(db, id, user_id)
    if item is None:
        # 商品が見つからない場合はNoneを返す
        return None
    # 商品を削除
    db.delete(item)
    # 変更を保存
    db.commit()
    return item
