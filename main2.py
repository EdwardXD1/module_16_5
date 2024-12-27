from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users: List['User'] = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/users", response_model=List[User])
async def all_inf() -> List[User]:
    return users

@app.post("/user/{username}/{age}", response_model=User)
async def post_user(
    username: str = Path(min_length=5, max_length=20, description="Enter username", examples="UrbanUser"),
    age: int = Path(ge=18, le=120, description="Enter age", examples=24)
):
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def refresh_user(
    user_id: int = Path(ge=1, description="Enter User ID", examples=1),
    username: str = Path(min_length=5, max_length=20, description="Enter username", examples="UrbanUser"),
    age: int = Path(ge=18, le=120, description="Enter age", examples=24)
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int = Path(ge=1, description="Enter User ID", examples=1)):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
