import asyncio
import datetime
import logging
from typing import Any

from telegram.constants import FloodLimit, ParseMode
from telegram.ext import AIORateLimiter, ExtBot

from hf_daily_papers_tg.commands.error_message import send_error_message
from hf_daily_papers_tg.parsers.papers import get_papers
from hf_daily_papers_tg.settings import Settings

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def send_daily_papers_update(bot: ExtBot[Any], settings: Settings) -> None:
    """Send daily papers update to the channel."""
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Starting daily papers update...",
    )
    yesterday = datetime.datetime.now(settings.timezone).date() - datetime.timedelta(days=1)
    papers = await get_papers(yesterday, settings)
    logger.info(f"Fetched {len(papers)} papers for date {yesterday.isoformat()}")

    for paper in papers:
        logger.info(f"Paper: {paper.paper.id}")
        try:
            await bot.send_message(
                chat_id=settings.tg.channel_id,
                text=paper.format(),
                parse_mode=ParseMode.HTML,
            )
            await asyncio.sleep(0.05)  # additional delay to avoid hitting rate limits
        except Exception as e:
            msg = f"Failed to send papers update. On paper {paper.paper.id} {e}"
            logger.exception(msg)
            await send_error_message(bot, settings.tg.admin_user_id, e, msg)

    logger.info("Finished daily papers update")
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Finished daily papers update.",
    )


async def main(settings: Settings) -> None:
    async with ExtBot(
        settings.tg.bot_token,
        rate_limiter=AIORateLimiter(
            # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits
            overall_max_rate=FloodLimit.MESSAGES_PER_MINUTE_PER_GROUP - 3,
            max_retries=2,
        ),
    ) as bot:
        try:
            await send_daily_papers_update(bot, settings)
        except Exception as e:
            msg = f"Failed to send papers update. {e}"
            logger.exception(msg)
            await send_error_message(bot, settings.tg.admin_user_id, e, msg)


if __name__ == "__main__":
    asyncio.run(main(Settings()))
