from app.kafka.handlers.base import KafkaMessageHandler
from app.core.logger import logger
from app.kafka.correlation import resolve_future


class AuthResponseHandler(KafkaMessageHandler):
    topic = "user.auth.response"

    async def handle(self, payload: dict) -> None:
        request_id = payload.get("request_id")

        if not request_id:
            logger.error(f"Missing request_id in auth response: {payload}")
            return

        resolve_future(request_id, payload)
