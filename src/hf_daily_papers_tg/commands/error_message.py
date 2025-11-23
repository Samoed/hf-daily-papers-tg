import html
import logging
import traceback

from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)


async def send_error_message(bot: Bot, admin_user_id: int, exception: Exception) -> None:
    """Send an error message to the admin user."""
    tb_list = traceback.format_exception(type(exception), exception, exception.__traceback__)
    tb_string = "".join(tb_list)

    logger.error(tb_string)
    message = f"An exception was raised while handling an update\n<pre>{html.escape(tb_string)}</pre>"

    await bot.send_message(chat_id=admin_user_id, text=message, parse_mode=ParseMode.HTML)
