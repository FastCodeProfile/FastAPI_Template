"""
Dependencies
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from typing_extensions import Annotated

from app import models
from app.core import exps, settings
from app.core.db import Database, SessionLocal
from app.core.security import JWTManager, oauth


async def get_db() -> Database:
    async with SessionLocal() as session:
        yield Database(session)


async def get_jwt_manager() -> JWTManager:
    return JWTManager(settings.APP_SECRET_KEY)


async def get_oauth_telegram() -> oauth.Telegram:
    return oauth.Telegram(
        settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_BOT_USERNAME
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, oauth.oauth],
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)],
    db: Annotated[Database, Depends(get_db)],
) -> models.User:
    payload = jwt_manager.decode_token(credentials.credentials)
    if payload.get('type') != 'access':
        raise exps.TOKEN_INVALID
    if not (user := await db.user.read(payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user
