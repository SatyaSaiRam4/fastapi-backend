from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from connections import get_db

from users.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from users.users import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)

from services.email_service import send_invitation_email


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# CREATE - POST a new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return create_user(db, user)


# READ - GET all users
@router.get("/", response_model=list[UserResponse])
def list_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    return get_all_users(db)


# READ - GET a user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# UPDATE - PUT a user
@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user"""

    user = update_user(db, user_id, user_update)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# DELETE - DELETE a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""

    deleted = delete_user(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return None


# SEND INVITATION EMAIL
@router.post("/invite")
def invite_user(data: dict):

    email = data.get("email")
    name = data.get("name")

    if not email or not name:
        raise HTTPException(
            status_code=400,
            detail="Name and email are required"
        )

    invite_link = "https://fastapi-frontend-98lpj0f27-satyas-projects-b7ea4d5b.vercel.app"

    response = send_invitation_email(
        to_email=email,
        name=name,
        invite_link=invite_link
    )

    return {
        "message": "Invitation sent successfully",
        "response": response
    }