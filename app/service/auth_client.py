import uuid
import asyncio

from app.kafka.correlation import create_future
from app.kafka.producer import get_kafka_producer
from app.schema.events import AuthResponse
from app.utils.error import InvalidTokenError, UserNotFoundError, InternalServiceError, AuthTimeoutError

ERROR_MAP = {
    "invalid_token": InvalidTokenError,
    "user_not_found": UserNotFoundError,
    "internal_error": InternalServiceError,
    "auth_timeout": AuthTimeoutError,
}

async def get_user_id_by_token(token: str, timeout: float = 10.0) -> str:
    request_id = str(uuid.uuid4())
    future = create_future(request_id)

    producer = await get_kafka_producer()
    await producer.send(
        "user.auth.request",
        {
            "request_id": request_id,
            "token": token,
        }
    )

    try:
        response_payload = await asyncio.wait_for(future, timeout)
        response = AuthResponse(**response_payload)

        if response.error:
            exc_class = ERROR_MAP.get(response.error, InternalServiceError)
            raise exc_class()

        if not response.user_id:
            raise InternalServiceError("Внутренняя ошибка сервиса")

        return response.user_id

    except asyncio.TimeoutError:
        raise AuthTimeoutError()
