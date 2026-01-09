import uuid
import asyncio
from app.infrastructure.messaging.kafka.correlation import create_future, resolve_future
from app.domain.errors import (
    InvalidTokenError,
    UserNotFoundError,
    InternalServiceError,
    AuthTimeoutError,
)
from app.infrastructure.messaging.kafka.producer import get_kafka_producer


ERROR_MAP = {
    "invalid_token": InvalidTokenError,
    "user_not_found": UserNotFoundError,
    "internal_error": InternalServiceError,
    "auth_timeout": AuthTimeoutError,
}


class AuthClient:

    def __init__(self):
        self._producer = None

    async def _get_producer(self):
        if self._producer is None:
            self._producer = await get_kafka_producer()
        return self._producer

    async def get_user_id_by_token(self, token: str, timeout: float = 10.0) -> str:
        request_id = str(uuid.uuid4())
        future = create_future(request_id)

        producer = await self._get_producer()
        await producer.send(
            "user.auth.request",
            {"request_id": request_id, "token": token},
        )

        try:
            payload = await asyncio.wait_for(future, timeout)
            if payload.get("error"):
                exc_class = ERROR_MAP.get(payload["error"], InternalServiceError)
                raise exc_class()

            user_id = payload.get("user_id")
            if not user_id:
                raise InternalServiceError("Внутренняя ошибка сервиса")

            return user_id

        except asyncio.TimeoutError:
            raise AuthTimeoutError()
