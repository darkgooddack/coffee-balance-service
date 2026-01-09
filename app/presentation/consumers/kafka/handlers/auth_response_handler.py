from app.infrastructure.messaging.kafka.base_handler import KafkaMessageHandler
from app.core.logging import logger
from app.infrastructure.messaging.kafka.correlation import resolve_future


class AuthResponseHandler(KafkaMessageHandler):
    topic = "user.auth.response"

    async def handle(self, payload: dict) -> None:
        request_id = payload.get("request_id")
        if not request_id:
            logger.error(f"Missing request_id: {payload}")
            return
        resolve_future(request_id, payload)
