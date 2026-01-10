import uuid
import asyncio

from app.application.interfaces.event_publisher import EventPublisher
from app.domain.errors import (
    InvalidTokenError,
    UserNotFoundError,
    InternalServiceError,
    AuthTimeoutError,
    TokenExpiredError,
)
from app.infrastructure.messaging.kafka.correlation import (
    create_future,
)


ERROR_MAP = {
    "invalid_token": InvalidTokenError,
    "user_not_found": UserNotFoundError,
    "internal_error": InternalServiceError,
    "auth_timeout": AuthTimeoutError,
    "token_expired": TokenExpiredError,
}


class AuthClient:

    def __init__(self, publisher: EventPublisher):
        self._publisher = publisher

    async def get_user_id_by_token(
        self,
        token: str,
        timeout: float = 10.0,
    ) -> str:
        request_id = str(uuid.uuid4())
        future = create_future(request_id)

        await self._publisher.publish(
            "user.auth.request",
            {
                "request_id": request_id,
                "token": token,
            },
        )

        try:
            payload = await asyncio.wait_for(future, timeout)

            if payload.get("error"):
                exc = ERROR_MAP.get(payload["error"], InternalServiceError)
                raise exc()

            user_id = payload.get("user_id")
            if not user_id:
                raise InternalServiceError()

            return user_id

        except asyncio.TimeoutError:
            raise AuthTimeoutError()
