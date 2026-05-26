from sqlalchemy import Column, Integer, String
from db import Base
class User(Base):
    __tablename__ = "satya_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, nullable=False)  # Foreign key to User.id (not enforced here for simplicity)
    files = Column(String, nullable=True)  # Store file path or name as string
    images = Column(String, nullable=True)  # Store image path or name as string