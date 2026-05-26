from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):      #get
    title: str
    description: Optional[str] = None
    owner_id: int

class ItemCreate(ItemBase):          #post
    pass  # Files and images will be handled via form data, not in schema

class ItemUpdate(BaseModel):           #put      All fields are optional, so you can update just one or more fields.If you inherit from ItemBase, all fields would be required (not optional).
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    # Files and images will be handled via form data

class ItemResponse(ItemBase):
    id: int
    files: Optional[str] = None
    images: Optional[str] = None

    class Config:
        from_attributes = True
