from fastapi import FastAPI, status
from typing import List
import src.users as users
import src.models as models


app = FastAPI()


@app.get("/users", response_model=List[models.User])
def get_users():
    return users.get_all_users()


@app.post("/users", response_model=models.User, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate):
    return users.create_user(user)

