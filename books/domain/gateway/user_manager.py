from abc import ABC, abstractmethod
from typing import Optional

from ..model import User


class UserManager(ABC):
    @abstractmethod
    def create_user(self, u: User) -> int:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
