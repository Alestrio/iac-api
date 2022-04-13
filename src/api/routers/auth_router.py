#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import auth_utils
from auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from data.database.UserDb import UserDb
from models.User import Token, User, UserIn

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        200: {"description": "Successful operation"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/users")
async def get_users():
    users = auth_utils.get_users()
    json_users = []
    for user in users:
        json_users.append(User.from_db_item(user))
    return json_users


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_utils.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth_utils.get_current_active_user)):
    return current_user


@router.post("/users/register/")
async def create_user(form_data: UserIn):
    user = auth_utils.create_user(form_data)
    return user


@router.put("/users/{username}/admin/{admin}")
async def change_admin_status(username: str, admin: bool, current_user: User = Depends(
    auth_utils.get_current_admin_user)):
    user = auth_utils.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user['is_admin'] != admin:
        user['is_admin'] = admin
        auth_utils.update_user(user)
    return True


@router.delete('/users/{username}')
async def delete_user(username: str, current_user: User = Depends(auth_utils.get_current_admin_user)):
    user = auth_utils.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    auth_utils.delete_user(user)
    return True
