from fastapi import FastAPI, status
from typing import List
import src.users as users


app = FastAPI()


@app.get("/users", response_model=List[users.User])
def get_users():
    return users.get_all_users()


@app.post("/users", response_model=users.User, status_code=status.HTTP_201_CREATED)
def create_user(user: users.UserCreate):
    return users.create_user(user)

