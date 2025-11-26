import asyncio
import datetime
import logging

from telegram import Bot
from telegram.constants import ParseMode

from hf_daily_papers_tg.commands.error_message import send_error_message
from hf_daily_papers_tg.parsers.posts import get_blog_posts, get_community_posts
from hf_daily_papers_tg.settings import Settings

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def send_posts_update(bot: Bot, settings: Settings) -> None:
    """Send daily papers update to the channel."""
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Starting daily posts update...",
    )
    yesterday = datetime.datetime.now(settings.timezone).date() - datetime.timedelta(days=1)
    logger.info("Starting daily posts update")
    blogs = await get_blog_posts(yesterday, settings)
    logger.info(f"Fetched {len(blogs)} posts for date {yesterday.isoformat()}")
    community_posts = await get_community_posts(yesterday, settings)
    logger.info(f"Fetched {len(community_posts)} community posts for date {yesterday.isoformat()}")

    message_lines = []
    if blogs:
        message_lines.append("<b>Blog Posts:</b>\n")
        blogs = sorted(blogs, key=lambda p: p.upvotes, reverse=True)
        for idx, post in enumerate(blogs, start=1):
            message_lines.append(f"{idx}. {post.hf_hyperlink} - {post.upvotes} 🔼")
        message_lines.append("")

    if community_posts:
        message_lines.append("<b>Community Posts:</b>\n")
        community_posts = sorted(community_posts, key=lambda p: p.upvotes, reverse=True)
        for idx, article in enumerate(community_posts, start=1):
            message_lines.append(f"{idx}. {article.hf_hyperlink} - {article.upvotes} 🔼")

    if not message_lines:
        await bot.send_message(
            chat_id=settings.tg.admin_user_id,
            text="No posts found for today.",
        )
        return

    await bot.send_message(
        chat_id=settings.tg.channel_id,
        text="\n".join(message_lines),
        parse_mode=ParseMode.HTML,
    )

    logger.info("Finished daily posts update")
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Finished daily posts update.",
    )


async def main(settings: Settings) -> None:
    async with Bot(settings.tg.bot_token) as bot:
        try:
            await send_posts_update(bot, settings)
        except Exception as e:
            msg = f"Failed to send daily posts update. {e}"
            logger.exception(msg)
            await send_error_message(bot, settings.tg.admin_user_id, e, msg)


if __name__ == "__main__":
    asyncio.run(main(Settings()))
