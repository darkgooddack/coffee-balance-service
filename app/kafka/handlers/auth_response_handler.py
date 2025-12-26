from app.kafka.handlers.base import KafkaMessageHandler
from app.core.logger import logger
from app.kafka.correlation import resolve_future


class AuthResponseHandler(KafkaMessageHandler):
    topic = "user.auth.response"

    async def handle(self, payload: dict) -> None:
        request_id = payload.get("request_id")
        user_id = payload.get("user_id")

        if request_id and user_id:
            resolve_future(request_id, user_id)
        else:
            logger.error(f"Invalid auth response: {payload}")
