from app.core.logging import logger
from app.infrastructure.messaging.base_handler import MessageHandler


class MessageRouter:
    def __init__(self, handlers: list[MessageHandler]):
        self._handlers = {h.event: h for h in handlers}

    @property
    def events(self) -> list[str]:
        return list(self._handlers.keys())

    async def dispatch(self, event: str, payload: dict):
        handler = self._handlers.get(event)
        if not handler:
            logger.warning(f"No handler for event {event}")
            return
        await handler.handle(payload)
