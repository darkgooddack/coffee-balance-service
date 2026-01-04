import asyncio
import json
from aiokafka import AIOKafkaConsumer
from app.core.config import settings
from app.core.logger import logger
from app.kafka.router import KafkaRouter

class KafkaConsumerManager:
    def __init__(self, router: KafkaRouter, group_id: str):
        self._consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None
        self.router = router
        self.group_id = group_id

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            *self.router.topics,
            bootstrap_servers=[settings.kafka.servers],
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await self._consumer.start()
        self._task = asyncio.create_task(self._consume())
        logger.info("Kafka consumer started")

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self._consumer:
            await self._consumer.stop()

    async def _consume(self):
        try:
            async for msg in self._consumer:
                await self.router.dispatch(msg.topic, msg.value)
        except asyncio.CancelledError:
            pass
