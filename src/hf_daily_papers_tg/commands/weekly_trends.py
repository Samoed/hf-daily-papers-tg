import asyncio
import logging

from telegram import Bot
from telegram.constants import ParseMode

from hf_daily_papers_tg.commands.error_message import send_error_message
from hf_daily_papers_tg.parsers.trending import get_trending_datasets, get_trending_models, get_trending_spaces
from hf_daily_papers_tg.settings import Settings

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def send_weekly_tradings_update(bot: Bot, settings: Settings) -> None:
    """Send daily papers update to the channel."""
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Starting weekly tradings update...",
    )

    datasets = await get_trending_datasets(settings)
    models = await get_trending_models(settings)
    spaces = await get_trending_spaces(settings)

    message_lines = ["<b>Weekly trending models:</b>"]
    for idx, model in enumerate(models, start=1):
        message_lines.append(f"{idx}. {model.full_text()}")
    message_lines.append("\n<b>Weekly trending spaces:</b>")
    for idx, space in enumerate(spaces, start=1):
        message_lines.append(f"{idx}. {space.full_text()}")
    message_lines.append("\n<b>Weekly trending datasets:</b>")
    for idx, dataset in enumerate(datasets, start=1):
        message_lines.append(f"{idx}. {dataset.full_text()}")

    await bot.send_message(
        chat_id=settings.tg.channel_id,
        text="\n".join(message_lines),
        parse_mode=ParseMode.HTML,
    )

    logger.info("Finished weekly trends update")
    await bot.send_message(
        chat_id=settings.tg.admin_user_id,
        text="Finished weekly trends update.",
    )


async def main(settings: Settings) -> None:
    async with Bot(settings.tg.bot_token) as bot:
        try:
            await send_weekly_tradings_update(bot, settings)
        except Exception as e:
            logger.exception("Failed to send weekly trends update.")
            await send_error_message(bot, settings.tg.admin_user_id, e)


if __name__ == "__main__":
    asyncio.run(main(Settings()))
