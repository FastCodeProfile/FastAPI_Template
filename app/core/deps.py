"""
Dependencies
"""

from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.core.db import Database
from app.core.security import Security
from app.logic import Logic
from app.models.user import User


async def get_db() -> AsyncGenerator[Database, Any]:
    async with Database() as db:
        yield db


async def get_security() -> Security:
    return Security()


async def get_logic(
    db: Annotated[Database, Depends(get_db)],
    security: Annotated[Security, Depends(get_security)],
) -> Logic:
    return Logic(db, security)


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name="access-token"))],
    logic: Annotated[Logic, Depends(get_logic)],
) -> User | None:
    return await logic.users.retrieve_by_token(token)
