import jwt
import time
from typing import Optional

from books.domain.gateway import PermissionManager
from ...domain.model import UserPermission

ERR_INVALID_TOKEN = "invalid token"
ERR_FAIL_TO_DECODE = "failed to decode token"


class TokenKeeper(PermissionManager):
    def __init__(self, secret_key: str, expire_in_hours: int):
        self.secret_key = secret_key.encode()
        self.expire_hours = expire_in_hours

    def generate_token(self, user_id: int, email: str, perm: UserPermission) -> str:
        expiration_time = int(time.time()) + self.expire_hours * 3600
        claims = {
            "user_id": user_id,
            "user_name": email,
            "permission": perm,
            "exp": expiration_time
        }
        token_result = jwt.encode(claims, self.secret_key, algorithm='HS256')
        return token_result

    def extract_token(self, token_result: str) -> Optional[dict]:
        try:
            claims = jwt.decode(
                token_result, self.secret_key, algorithms=['HS256'])
            return claims
        except jwt.ExpiredSignatureError:
            raise ValueError(ERR_INVALID_TOKEN)
        except jwt.DecodeError:
            raise ValueError(ERR_FAIL_TO_DECODE)

    def has_permission(self, token_result: str, perm: UserPermission) -> bool:
        claims = self.extract_token(token_result)
        if not claims:
            return False
        return claims.get("permission", UserPermission.PermNone) >= perm
