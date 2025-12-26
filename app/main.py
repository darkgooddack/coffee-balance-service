from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.config import settings
from app.core.logger import logger
from app.kafka.consumer import KafkaConsumerManager
from app.kafka.handlers.auth_response_handler import AuthResponseHandler
from app.kafka.handlers.user_registered_handler import UserRegisteredHandler
from app.kafka.router import KafkaRouter
from app.utils.error import AppBaseError
from app.api.balance import router as balance_router


handlers = [AuthResponseHandler(), UserRegisteredHandler()]
kafka_router = KafkaRouter(handlers)
kafka_consumer = KafkaConsumerManager(kafka_router, group_id="coffee-balance-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kafka consumers...")
    await kafka_consumer.start()
    try:
        yield
    finally:
        logger.info("Stopping Kafka consumers...")
        await kafka_consumer.stop()

app = FastAPI(
    name="coffee-balance-service",
    description="Сервис баланса",
    lifespan=lifespan,
)


@app.exception_handler(AppBaseError)
async def app_base_error_handler(
    request: Request,
    exc: AppBaseError,
):
    raise exc.http()


app.include_router(balance_router, prefix=settings.api.prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
