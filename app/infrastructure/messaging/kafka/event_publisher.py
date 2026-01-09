from app.application.interfaces.event_publisher import EventPublisher
from app.infrastructure.messaging.kafka.producer import KafkaProducerWrapper


class KafkaEventPublisher(EventPublisher):
    def __init__(self, producer: KafkaProducerWrapper):
        self._producer = producer

    async def publish(self, event_name: str, payload: dict) -> None:
        await self._producer.send(event_name, payload)
