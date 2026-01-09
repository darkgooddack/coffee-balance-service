from app.application.interfaces.event_publisher import EventPublisher


class RabbitEventPublisher(EventPublisher):
    async def publish(self, event_name: str, payload: dict):
       ...
