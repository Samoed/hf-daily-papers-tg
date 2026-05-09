import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from telegram.error import TimedOut

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def send_with_retries(
    fn: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    backoff: float = 2.0,
) -> T:
    """Call an async Telegram request, retrying on TimedOut with exponential backoff."""
    for attempt in range(1, attempts + 1):
        try:
            return await fn()
        except TimedOut:  # noqa: PERF203
            if attempt == attempts:
                raise
            wait = backoff**attempt
            logger.warning("Timed out, retrying in %.0fs (attempt %d/%d)", wait, attempt, attempts)
            await asyncio.sleep(wait)
    return None  # type: ignore[return-value]
