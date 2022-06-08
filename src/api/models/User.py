#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), Alexis LEBEL, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
from typing import Optional

from pydantic import BaseModel

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserIn(BaseModel):
    username: str
    password: str
    email: str


class User(BaseModel):
    username: str
    password: str
    email: str
    permissions: list[str] = []
    is_active: bool = True
    is_admin: bool = False

    def hash_password(self):
        """
        Hash the password using md5
        """
        import hashlib
        self.password = pwd_context.encrypt(self.password)

    @staticmethod
    def from_userin(user: UserIn):
        """
        Update the user from a userin object
        :return: None
        """
        user = User(
            username=user.username,
            password=user.password,
            email=user.email,
        )
        user.hash_password()
        return user

    @staticmethod
    def from_db_item(user: dict):
        """
        Update the user from a database item
        :return: None
        """
        user = User(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            permissions=user["permissions"],
            is_active=user["is_active"],
            is_admin=user["is_admin"],
        )
        return user


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None