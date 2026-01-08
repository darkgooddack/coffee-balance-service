from app.repository.balance import BalanceRepository


class BalanceService:
    def __init__(self, repo: BalanceRepository):
        self.repo = repo

    async def top_up(self, user_id: str, amount: int) -> int:
        return await self.repo.update_balance(user_id, amount)

    async def get_balance(self, user_id: str):
        balance = await self.repo.get_balance(user_id)
        if not balance:
            return 0
        return balance.balance

    async def create_balance_for_user(self, user_id: str) -> tuple[bool, str | None]:
        try:
            await self.repo.create_balance(user_id)
            return True, None
        except Exception:
            return False, "internal_error"


