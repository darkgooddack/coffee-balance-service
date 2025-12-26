import asyncio
from typing import Dict

_pending: Dict[str, asyncio.Future] = {}

def create_future(request_id: str) -> asyncio.Future:
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    _pending[request_id] = future
    return future

def resolve_future(request_id: str, value):
    future = _pending.pop(request_id, None)
    if future and not future.done():
        future.set_result(value)

def reject_future(request_id: str, exc: Exception):
    future = _pending.pop(request_id, None)
    if future and not future.done():
        future.set_exception(exc)