from pydantic import BaseModel, EmailStr


# Common fields shared by all user schemas
class UserBase(BaseModel):

    # User name must be string
    name: str

    # Validates email format automatically
    email: EmailStr


# Used when creating a new user
class UserCreate(UserBase):

    # Inherits:
    # name
    # email
    pass


# Used when updating a user
class UserUpdate(BaseModel):

    # Optional fields
    name: str | None = None
    email: EmailStr | None = None


# Used when sending user response
class UserResponse(UserBase):

    # Include database ID
    id: int

    # Convert SQLAlchemy object -> JSON
    class Config:
        from_attributes = True