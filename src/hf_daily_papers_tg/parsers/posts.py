import datetime

from httpx import AsyncClient

from hf_daily_papers_tg.models.posts import Article, Blog, Blogs, CommunityArticlesModel
from hf_daily_papers_tg.parsers.http_utils import fetch_json_with_retries
from hf_daily_papers_tg.settings import Settings


async def get_blog_posts(date: datetime.date, settings: Settings) -> list[Blog]:
    """Placeholder for get_blogs function."""
    url = f"{settings.hf_api_base_url}/blog"
    async with AsyncClient() as client:
        blogs_data = await fetch_json_with_retries(client, url)
    blogs = Blogs.model_validate(blogs_data)
    return [blog for blog in blogs.blogs if blog.published_at.date() == date]


async def get_community_posts(date: datetime.date, settings: Settings) -> list[Article]:
    """Fetch community articles from Hugging Face API for a given date."""
    url = f"{settings.hf_api_base_url}/blog/community"
    async with AsyncClient() as client:
        articles_data = await fetch_json_with_retries(
            client,
            url,
            params={"sort": "recent"},
        )
    articles = CommunityArticlesModel.model_validate(articles_data)
    return [article for article in articles.posts if article.published_at.date() == date]
