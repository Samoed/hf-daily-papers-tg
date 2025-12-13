from httpx import AsyncClient

from hf_daily_papers_tg.models.trending import (
    DatasetTrendingModel,
    ModelsTrendingModel,
    RecentlyTrendingModel,
    RepoType,
    SpacesTrendingModel,
    TrendingModel,
)
from hf_daily_papers_tg.parsers.http_utils import fetch_json_with_retries
from hf_daily_papers_tg.settings import Settings


async def get_trending(settings: Settings, date_type: RepoType, limit: int = 10) -> list[TrendingModel]:
    url = f"{settings.hf_api_base_url}/trending"
    async with AsyncClient() as client:
        blogs_data = await fetch_json_with_retries(
            client,
            url,
            params={"type": date_type, "limit": limit},
        )
    recently_trending = RecentlyTrendingModel.model_validate(blogs_data)
    return recently_trending.recently_trending


async def get_trending_datasets(settings: Settings, limit: int = 10) -> list[DatasetTrendingModel]:
    recently_trending = await get_trending(settings, "dataset", limit)
    return [model.repo_data for model in recently_trending]


async def get_trending_models(settings: Settings, limit: int = 10) -> list[ModelsTrendingModel]:
    recently_trending = await get_trending(settings, "model", limit)
    return [model.repo_data for model in recently_trending]


async def get_trending_spaces(settings: Settings, limit: int = 10) -> list[SpacesTrendingModel]:
    recently_trending = await get_trending(settings, "space", limit)
    return [model.repo_data for model in recently_trending]
