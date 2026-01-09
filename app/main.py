from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from core.config import settings
from core.exceptions import map_exception
from core.logging import logger

from infrastructure.messaging.kafka.consumer import KafkaConsumerManager
from infrastructure.messaging.kafka.router import KafkaRouter
from presentation.consumers.kafka.handlers.auth_response_handler import (
    AuthResponseHandler,
)
from presentation.consumers.kafka.handlers.user_registered_handler import (
    UserRegisteredHandler,
)
from presentation.api.balance_router import router


handlers = [
    AuthResponseHandler(),
    UserRegisteredHandler(),
]

kafka_router = KafkaRouter(handlers)
kafka_consumer = KafkaConsumerManager(
    kafka_router,
    group_id="coffee-balance-service",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kafka consumers...")

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
    raise map_exception(exc)


app.include_router(router, prefix=settings.api.prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
