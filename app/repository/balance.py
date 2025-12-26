from sqlalchemy.ext.asyncio import AsyncSession
from app.models.balance import Balance


class BalanceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: str) -> Balance | None:
        return await self.session.get(Balance, user_id)

    async def create_balance(self, user_id: str) -> Balance:
        balance = Balance(user_id=user_id, balance=0)
        self.session.add(balance)
        await self.session.commit()
        return balance

    async def update_balance(self, user_id: str, amount: int) -> Balance:
        balance = await self.get_balance(user_id)
        if balance is None:
            balance = await self.create_balance(user_id)
        balance.balance += amount
        await self.session.commit()
        return balance
