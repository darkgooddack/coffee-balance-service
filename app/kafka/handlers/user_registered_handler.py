from app.kafka.handlers.base import KafkaMessageHandler
from app.database.db import new_session
from app.repository.balance import BalanceRepository
from app.service.balance import BalanceService
from app.core.logger import logger


class UserRegisteredHandler(KafkaMessageHandler):
    topic = "user.registered"

    async def handle(self, payload: dict) -> None:
        user_id = payload.get("user_id")
        if not user_id:
            logger.error(f"Invalid user.registered payload: {payload}")
            return

        async with new_session() as session:
            repo = BalanceRepository(session)
            service = BalanceService(repo)
            success, error = await service.create_balance_for_user(user_id)

            if not success:
                logger.error(f"Failed to create balance for user {user_id}, error: {error}")
