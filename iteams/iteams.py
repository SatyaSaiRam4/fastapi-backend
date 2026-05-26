from sqlalchemy.orm import Session
from models import Item

# CREATE - Add a new item
def create_item(db: Session, item_data: dict) -> Item:
    item = Item(**item_data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# READ - Get item by ID
def get_item_by_id(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()

# READ - Get all items
def get_all_items(db: Session) -> list[Item]:
    return db.query(Item).all()

# UPDATE - Update an item
def update_item(db: Session, item_id: int, update_data: dict) -> Item | None:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None
    for key, value in update_data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

# DELETE - Delete an item
def delete_item(db: Session, item_id: int) -> bool:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
