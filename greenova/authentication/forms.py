# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Authentication forms and FastAPI utilities for the authentication app.

This module provides Pydantic models and FastAPI endpoints for user
authentication, token management, and session handling, with strict type
annotations and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - FastAPI endpoints for user info and token management
    - Pydantic models for user and token data

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from beartype import beartype

from .types import UserInfoDict, SessionDataDict, MfaPayloadDict

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """Pydantic model for user information."""

    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class Token(BaseModel):
    """Pydantic model for access token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Pydantic model for token data."""

    username: Optional[str] = None


@beartype
def fake_decode_token(token: str) -> UserInfoDict:
    """Fake decode a token and return user info.

    Args:
        token: The token string.

    Returns:
        UserInfoDict: The decoded user info dictionary.
    """
    # This doesn't provide any security at all
    # Check the next version
    user_info: UserInfoDict = {
        "username": "john",
        "email": "john@example.com",
        "full_name": "John Doe",
        "disabled": False,
    }
    return user_info


@beartype
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the token.

    Args:
        token: The OAuth2 token.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the user is inactive.
    """
    user_info = fake_decode_token(token)
    if user_info["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(**user_info)


@app.get("/users/me", response_model=User)
@beartype
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """Get the current authenticated user.

    Args:
        current_user: The current user dependency.

    Returns:
        User: The current user.
    """
    return current_user
