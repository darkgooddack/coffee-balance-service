from abc import ABC, abstractmethod


class MessageHandler(ABC):
    event: str

    @abstractmethod
    async def handle(self, payload: dict) -> None:
        ...
