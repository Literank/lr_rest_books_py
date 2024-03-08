from abc import ABC, abstractmethod
from typing import Optional

from ..model import User, UserPermission


class UserManager(ABC):
    @abstractmethod
    def create_user(self, u: User) -> int:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass


class PermissionManager(ABC):
    @abstractmethod
    def generate_token(self, user_id: int, email: str, perm: UserPermission) -> str:
        pass

    @abstractmethod
    def has_permission(self, token: str, perm: UserPermission) -> bool:
        pass
