from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users import routes as users
from iteams import routes as items
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
def home():
    return {"message": "FastAPI running"}