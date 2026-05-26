from sqlalchemy.orm import Session
from models import User
from users.schemas import UserCreate, UserUpdate


# CREATE - Add a new user to the database            (POST)
def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ - Get a user by ID                                     (GET /user_id)
def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get a user by their ID"""
    return db.query(User).filter(User.id == user_id).first()




# READ - Get all users                                         (GET /users)
def get_all_users(db: Session) -> list[User]:
    """Get all users from the database"""
    return db.query(User).all()


# UPDATE - Update a user                                         (PUT /user_id)
def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    """Update a user's information"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        db_user.email = user_update.email
    
    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE - Delete a user                                  (DELETE /user_id)
def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user by their ID. Returns True if deleted, False if user not found"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
