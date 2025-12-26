from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.repository.balance import BalanceRepository
from app.service.balance import BalanceService


def get_balance_service(
    session: AsyncSession = Depends(get_session),
) -> BalanceService:
    repo = BalanceRepository(session)
    return BalanceService(repo)