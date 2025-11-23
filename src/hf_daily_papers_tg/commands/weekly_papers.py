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


async def send_weekly_papers_update(bot: Bot, settings: Settings) -> None:
    """Send daily papers update to the channel."""
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Starting weekly papers update...",
    )
    # fetch papers from 6 days ago (run on Saturday for weekly update)
    today = datetime.datetime.now(settings.timezone).date()
    start_date = today - datetime.timedelta(days=settings.weekly_fetch_days)

    logger.info(f"Fetching papers from {start_date.isoformat()} to {today.isoformat()}")

    papers = []
    for day_offset in range(settings.weekly_fetch_days):
        date = start_date + datetime.timedelta(days=day_offset)
        daily_papers = await get_papers(date, settings)
        papers.extend(daily_papers)
        logger.info(f"Fetched {len(daily_papers)} papers for {date.isoformat()}")
    logger.info(f"Total papers fetched: {len(papers)}")

    papers = sorted(papers, key=lambda p: p.paper.upvotes, reverse=True)[: settings.weekly_top]

    message_lines = ["<b>Weekly Top Papers:</b>\n"]
    for idx, paper in enumerate(papers, start=1):
        message_lines.append(f"{idx}. {paper.paper_hyperlink} - {paper.paper.upvotes} 🔼")

    await bot.send_message(
        chat_id=settings.tg.channel_id,
        text="\n".join(message_lines),
        parse_mode=ParseMode.HTML,
    )

    logger.info("Finished weekly papers update")
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Finished weekly papers update.",
    )


async def main(settings: Settings) -> None:
    async with Bot(settings.tg.bot_token) as bot:
        try:
            await send_weekly_papers_update(bot, settings)
        except Exception as e:
            logger.exception("Failed to send weekly papers update.")
            await send_error_message(bot, settings.tg.admin_user_id, e)


if __name__ == "__main__":
    asyncio.run(main(Settings()))
