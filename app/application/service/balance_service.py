from app.application.interfaces.balance_repository import BalanceRepository
from app.domain.errors import (
    BalanceNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InternalServiceError,
)


class BalanceService:
    def __init__(self, repo: BalanceRepository):
        self.repo = repo

    async def top_up(self, user_id: str, amount: int) -> int:
        if amount <= 0:
            raise InvalidAmountError()

        try:
            return await self.repo.update_balance(user_id, amount)
        except Exception:
            raise InternalServiceError()

    async def pay(self, user_id: str, amount: int) -> int:
        if amount <= 0:
            raise InvalidAmountError()

        balance = await self.repo.get_balance(user_id)
        if balance is None:
            raise BalanceNotFoundError()

        if balance.balance < amount:
            raise InsufficientFundsError()

        try:
            return await self.repo.update_balance(user_id, -amount)
        except Exception:
            raise InternalServiceError()

    async def get_balance(self, user_id: str) -> int:
        balance = await self.repo.get_balance(user_id)
        return balance.balance if balance else 0
