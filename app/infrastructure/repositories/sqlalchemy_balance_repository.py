from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces.balance_repository import BalanceRepository
from app.domain.entities.balance import Balance
from app.infrastructure.db.models.balance_model import BalanceModel


class SqlAlchemyBalanceRepository(BalanceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: str) -> Balance | None:
        model = await self.session.get(BalanceModel, user_id)
        if not model:
            return None
        return Balance(
            user_id=str(model.user_id),
            balance=model.balance,
        )

    async def update_balance(self, user_id: str, amount: int) -> int:
        model = await self.session.get(BalanceModel, user_id)
        if model is None:
            model = BalanceModel(user_id=user_id, balance=0)
            self.session.add(model)

        model.balance += amount
        await self.session.commit()
        return model.balance
