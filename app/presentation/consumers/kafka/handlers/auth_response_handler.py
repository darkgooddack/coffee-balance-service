from app.core.logging import logger
from app.infrastructure.messaging.base_handler import MessageHandler
from app.infrastructure.messaging.kafka.correlation import resolve_future


class AuthResponseHandler(MessageHandler):
    topic = "user.auth.response"

    async def handle(self, payload: dict) -> None:
        request_id = payload.get("request_id")
        if not request_id:
            logger.error(f"Missing request_id: {payload}")
            return
        resolve_future(request_id, payload)
