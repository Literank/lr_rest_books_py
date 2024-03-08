from datetime import datetime
import hashlib
import random
import time
from typing import Optional

from books.application.dto import UserCredential, User, UserToken
from books.domain.gateway import UserManager, PermissionManager
from books.domain.model import User as DomainUser, UserPermission

SALT_LEN = 4
ERR_EMPTY_EMAIL = "empty email"
ERR_EMPTY_PASSWORD = "empty password"


class UserOperator:
    def __init__(self, user_manager: UserManager, perm_manager: PermissionManager):
        self.user_manager = user_manager
        self.perm_manager = perm_manager

    def create_user(self, uc: UserCredential) -> Optional[User]:
        if not uc.email:
            raise ValueError(ERR_EMPTY_EMAIL)
        if not uc.password:
            raise ValueError(ERR_EMPTY_PASSWORD)

        salt = random_string(SALT_LEN)
        password_hash = sha1_hash(uc.password + salt)

        now = datetime.now()
        user = DomainUser(id=0, email=uc.email,
                          password=password_hash, salt=salt, is_admin=False,
                          created_at=now, updated_at=now)
        uid = self.user_manager.create_user(user)
        return User(id=uid, email=uc.email)

    def sign_in(self, email: str, password: str) -> Optional[UserToken]:
        if not email:
            raise ValueError(ERR_EMPTY_EMAIL)
        if not password:
            raise ValueError(ERR_EMPTY_PASSWORD)

        user = self.user_manager.get_user_by_email(email)
        if not user:
            return None
        password_hash = sha1_hash(password + user.salt)
        if user.password != password_hash:
            raise ValueError("wrong password")
        token = self.perm_manager.generate_token(
            user.id, user.email,
            UserPermission.PermAdmin if user.is_admin else UserPermission.PermUser)
        return UserToken(
            User(id=user.id, email=user.email),
            token)


def random_string(length: int) -> str:
    source = random.Random(time.time())
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ''.join(source.choice(charset) for _ in range(length))
    return result


def sha1_hash(input_str: str) -> str:
    hash_object = hashlib.sha1(input_str.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex
