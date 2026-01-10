
from app.core.logging import logger
from app.core.dependencies import get_balance_service
from app.infrastructure.messaging.base_handler import MessageHandler


class UserRegisteredHandler(MessageHandler):
    topic = "user.registered"

    async def handle(self, payload: dict) -> None:
        user_id = payload.get("user_id")
        if not user_id:
            logger.error(f"Invalid payload: {payload}")
            return

        service = await get_balance_service()
        await service.top_up(user_id, 0)
