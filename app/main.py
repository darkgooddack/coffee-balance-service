from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import map_exception
from app.core.logging import logger

from app.infrastructure.messaging.kafka.consumer import KafkaConsumerManager
from app.infrastructure.messaging.router import MessageRouter
from app.presentation.consumers.kafka.handlers.auth_response_handler import (
    AuthResponseHandler,
)
from app.presentation.consumers.kafka.handlers.user_registered_handler import (
    UserRegisteredHandler,
)
from app.presentation.api.balance_router import router


handlers = [
    AuthResponseHandler(),
    UserRegisteredHandler(),
]

kafka_router = MessageRouter(handlers)
kafka_consumer = KafkaConsumerManager(
    kafka_router,
    group_id="coffee-balance-service",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kafka consumers.2..")

    try:
        await kafka_consumer.start()
        logger.info("Kafka consumer started successfully")
    except Exception as e:
        logger.error(f"Kafka unavailable, consumer not started: {e}")
        kafka_consumer._consumer = None
        kafka_consumer._task = None

    try:
        yield
    finally:
        logger.info("Stopping Kafka consumers...")
        try:
            await kafka_consumer.stop()
        except Exception as e:
            logger.warning(f"Error stopping Kafka consumer: {e}")



app = FastAPI(
    name="coffee-balance-service",
    description="Сервис баланса",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Handled exception: %s", exc)
    http_exc = map_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content={"detail": http_exc.detail},
    )



app.include_router(router, prefix=settings.api.prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
