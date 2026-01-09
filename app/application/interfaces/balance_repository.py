from abc import ABC, abstractmethod
from app.domain.entities.balance import Balance


class BalanceRepository(ABC):

    @abstractmethod
    async def get_balance(self, user_id: str) -> Balance | None:
        pass

    @abstractmethod
    async def update_balance(self, user_id: str, amount: int) -> int:
        pass
