from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.service.balance_service import BalanceService
from app.infrastructure.repositories.sqlalchemy_balance_repository import (
    SqlAlchemyBalanceRepository,
)
from app.database.db import get_session
from app.infrastructure.auth.auth_client import AuthClient


async def get_balance_service(
    session: AsyncSession = Depends(get_session),
) -> BalanceService:
    repo = SqlAlchemyBalanceRepository(session)
    return BalanceService(repo)


async def get_auth_client() -> AuthClient:
    return AuthClient()
