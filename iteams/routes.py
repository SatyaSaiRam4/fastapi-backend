from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from connections import get_db
from iteams.schemas import ItemCreate, ItemUpdate, ItemResponse
from iteams.iteams import (
    create_item,
    get_item_by_id,
    get_all_items,
    update_item,
    delete_item,
)
from typing import List, Optional

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

# CREATE - POST a new item (multipart/form-data)
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_new_item(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    owner_id: int = Form(...),
    files: Optional[UploadFile] = File(None),
    images: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    item_data = {
        "title": title,
        "description": description,
        "owner_id": owner_id,
        "files": files.filename if files else None,
        "images": images.filename if images else None,
    }
    return create_item(db, item_data)

# READ - GET all items
@router.get("/", response_model=List[ItemResponse])
def list_all_items(db: Session = Depends(get_db)):
    return get_all_items(db)

# READ - GET an item by ID
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# UPDATE - PUT an item (multipart/form-data)
@router.put("/{item_id}", response_model=ItemResponse)
def update_existing_item(
    item_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    owner_id: Optional[int] = Form(None),
    files: Optional[UploadFile] = File(None),
    images: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if owner_id is not None:
        update_data["owner_id"] = owner_id
    if files is not None:
        update_data["files"] = files.filename
    if images is not None:
        update_data["images"] = images.filename
    item = update_item(db, item_id, update_data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# DELETE - DELETE an item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
