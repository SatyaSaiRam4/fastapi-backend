# run_schema.py: Execute schema.sql to create tables in the database
from sqlalchemy import text
from connections import engine

SCHEMA_FILE = "schema.sql"

def run_schema():
    with open(SCHEMA_FILE, "r") as f:
        sql = f.read()
    # with engine.connect() as conn:                it wont auto commit , so u cant see chnages in database when we run the file .  
    with engine.begin() as conn:
        for statement in sql.split(';'):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
    print("Schema executed successfully.")

if __name__ == "__main__":
    run_schema()
