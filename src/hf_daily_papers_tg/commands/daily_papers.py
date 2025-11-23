import asyncio
import datetime
import logging

from telegram import Bot
from telegram.constants import ParseMode

from hf_daily_papers_tg.commands.error_message import send_error_message
from hf_daily_papers_tg.parsers.papers import get_papers
from hf_daily_papers_tg.settings import Settings

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def send_daily_papers_update(bot: Bot, settings: Settings) -> None:
    """Send daily papers update to the channel."""
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Starting daily papers update...",
    )
    today = datetime.datetime.now(settings.timezone).date()
    papers = await get_papers(today, settings)
    logger.info(f"Fetched {len(papers)} papers for date {today.isoformat()}")

    for paper in papers:
        logger.info(f"Paper: {paper.paper.id}")
        try:
            await bot.send_message(
                chat_id=settings.tg.channel_id,
                text=paper.format(),
                parse_mode=ParseMode.HTML,
            )
            await asyncio.sleep(0.05)
        except Exception:
            msg = f"Failed to send papers update. On paper {paper.paper.id}"
            logger.exception(msg)
            await send_error_message(bot, settings.tg.admin_user_id, Exception(msg))

    logger.info("Finished daily papers update")
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Finished daily papers update.",
    )


async def main(settings: Settings) -> None:
    async with Bot(settings.tg.bot_token) as bot:
        try:
            await send_daily_papers_update(bot, settings)
        except Exception as e:
            logger.exception("Failed to send papers update.")
            await send_error_message(bot, settings.tg.admin_user_id, e)


if __name__ == "__main__":
    asyncio.run(main(Settings()))
