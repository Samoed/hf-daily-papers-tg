import datetime
import logging

from httpx import AsyncClient

from hf_daily_papers_tg.models.papers import PaperModel
from hf_daily_papers_tg.parsers.http_utils import fetch_json_with_retries
from hf_daily_papers_tg.settings import Settings

logger = logging.getLogger(__name__)


async def get_papers(date: datetime.date, settings: Settings) -> list[PaperModel]:
    """Fetch papers from Hugging Face API for a given date."""
    url = f"{settings.hf_api_base_url}/daily_papers"
    async with AsyncClient() as client:
        papers_data = await fetch_json_with_retries(
            client,
            url,
            params={"date": date.isoformat()},
        )
    return [PaperModel.model_validate(paper) for paper in papers_data]
