import asyncio
import logging
from collections.abc import Mapping
from typing import Any

from httpx import AsyncClient, HTTPStatusError

logger = logging.getLogger(__name__)


async def fetch_json_with_retries(
    client: AsyncClient,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    attempts: int = 3,
    backoff: float = 1.0,
) -> list[Any] | dict[Any, Any]:
    """GET JSON payload with basic retry logic."""
    last_error: HTTPStatusError | None = None

    for attempt in range(1, attempts + 1):
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as exc:
            last_error = exc
            logger.warning("Request failed for %s (attempt %s/%s): %s", url, attempt, attempts, exc)
            if attempt == attempts:
                break
        await asyncio.sleep(backoff * attempt)

    raise last_error or RuntimeError(f"Failed to fetch {url}")
