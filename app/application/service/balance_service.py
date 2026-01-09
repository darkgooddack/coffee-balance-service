from app.application.interfaces.balance_repository import BalanceRepository
from app.core.logging import logger
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
        logger.info("Top-up requested: user_id=%s, amount=%s", user_id, amount)

        if amount <= 0:
            logger.warning("Invalid amount for top-up: %s", amount)
            raise InvalidAmountError()

        try:
            new_balance = await self.repo.update_balance(user_id, amount)
            logger.info("New balance after top-up: %s for user_id=%s", new_balance, user_id)
            return int(new_balance)  # точно int для response_model
        except Exception as e:
            logger.exception("Error during top-up for user_id=%s: %s", user_id, e)
            raise InternalServiceError() from e

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
