import datetime as dt

from jose import JWTError, jwt
from jose.constants import ALGORITHMS

from app.core import exps


class JWTManager:
    def __init__(self, secret_key: str):
        self.secret_key: str = secret_key

    def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHMS.HS256])
        except JWTError:
            raise exps.TOKEN_INVALID

        exp = payload.get("exp")
        if exp and dt.datetime.now(dt.UTC).timestamp() > exp:
            raise exps.TOKEN_EXPIRED
        return payload.get("payload")

    def encode_token(self, payload: dict, minutes: int) -> str:
        claims = {
            "payload": payload,
            "exp": dt.datetime.now(dt.UTC) + dt.timedelta(minutes=minutes),
        }
        return jwt.encode(claims, self.secret_key, algorithm=ALGORITHMS.HS256)
