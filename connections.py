# # connections.py: Create SQLAlchemy engine and SessionLocal
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from db import Base
# import models

# from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# # Validate credentials before creating engine
# def validate_db_credentials():
#     missing = [var for var, val in {
#         'DB_NAME': DB_NAME,
#         'DB_USER': DB_USER,
#         'DB_PASSWORD': DB_PASSWORD,
#         'DB_HOST': DB_HOST,
#         'DB_PORT': DB_PORT
#     }.items() if not val]
#     if missing:
#         raise ValueError(f"Missing required DB credentials: {', '.join(missing)}")

# validate_db_credentials()

# # Construct the database URL
# # DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = "postgresql://postgres.znttvqorufuzrkhdjjtc:postgres@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true"



# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Create a configured "SessionLocal" class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # ----------------------------------------------------------------------------------------------------------------------------------


#                                   # Dependency function to get a database session. This will be used in FastAPI routes to interact with the database.
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


#                                     # Creat all tables in the database (Run this function once to create tables based on your models)
# def create_tables():                             #this fun is used for creating tables if not exsists
#     Base.metadata.create_all(bind=engine)


# # ---------------------------------------------------------------------------------------------------------------------------------------


# # Function to test database connected or not , if connected then it will print "Database connection successful!" otherwise it will print the error message.  (Run this file)
# def test_connection():
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text("SELECT 1"))
#             print("Database connection successful!", result.scalar())
#     except Exception as e:
#         print("Database connection failed:", e)

# if __name__ == "__main__":
#     test_connection()
#     create_tables()
#     print("Tables created!")




from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db import Base
import models
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres.znttvqorufuzrkhdjjtc:postgres@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true"



# # Create the SQLAlchemy engine

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    test_connection()
    create_tables()
    print("Tables created!")