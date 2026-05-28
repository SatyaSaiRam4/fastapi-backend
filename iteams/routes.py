from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from connections import get_db
from iteams.schemas import ItemUpdate, ItemResponse
from iteams.iteams import (
    create_item,
    get_item_by_id,
    get_all_items,
    update_item,
    delete_item,
)
from typing import List, Optional
from supabase_client import supabase
import uuid

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

# CREATE - POST a new item
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_new_item(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    owner_id: int = Form(...),
    files: Optional[UploadFile] = File(None),
    images: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):

    file_url = None
    image_url = None

    # Upload file to Supabase Storage
    if files:
        file_bytes = await files.read()

        unique_file_name = f"{uuid.uuid4()}_{files.filename}"

        supabase.storage.from_("uploads").upload(
            unique_file_name,
            file_bytes
        )

        file_url = supabase.storage.from_("uploads").get_public_url(
            unique_file_name
        )

    # Upload image to Supabase Storage
    if images:
        image_bytes = await images.read()

        unique_image_name = f"{uuid.uuid4()}_{images.filename}"

        supabase.storage.from_("uploads").upload(
            unique_image_name,
            image_bytes
        )

        image_url = supabase.storage.from_("uploads").get_public_url(
            unique_image_name
        )

    item_data = {
        "title": title,
        "description": description,
        "owner_id": owner_id,
        "files": file_url,
        "images": image_url,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return item


# UPDATE - PUT an item
@router.put("/{item_id}", response_model=ItemResponse)
async def update_existing_item(
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

    # Upload updated file
    if files is not None:
        file_bytes = await files.read()

        unique_file_name = f"{uuid.uuid4()}_{files.filename}"

        supabase.storage.from_("uploads").upload(
            unique_file_name,
            file_bytes
        )

        file_url = supabase.storage.from_("uploads").get_public_url(
            unique_file_name
        )

        update_data["files"] = file_url

    # Upload updated image
    if images is not None:
        image_bytes = await images.read()

        unique_image_name = f"{uuid.uuid4()}_{images.filename}"

        supabase.storage.from_("uploads").upload(
            unique_image_name,
            image_bytes
        )

        image_url = supabase.storage.from_("uploads").get_public_url(
            unique_image_name
        )

        update_data["images"] = image_url

    item = update_item(db, item_id, update_data)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return item


# DELETE - DELETE an item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_item(db, item_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return None