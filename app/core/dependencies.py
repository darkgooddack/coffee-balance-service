from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.event_publisher import EventPublisher
from app.application.service.balance_service import BalanceService
from app.infrastructure.messaging.kafka.event_publisher import KafkaEventPublisher
from app.infrastructure.messaging.kafka.producer import get_kafka_producer
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


async def get_event_publisher(
    producer=Depends(get_kafka_producer),
) -> EventPublisher:
    return KafkaEventPublisher(producer)


async def get_auth_client(
    publisher: EventPublisher = Depends(get_event_publisher),
):
    return AuthClient(publisher)
