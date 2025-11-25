import html
import logging
import traceback

from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)


async def send_error_message(bot: Bot, admin_user_id: int, exception: Exception, message: str | None = None) -> None:
    """Send an error message to the admin user."""
    tb_list = traceback.format_exception(type(exception), exception, exception.__traceback__)
    tb_string = "".join(tb_list)
    msg_str = ""
    if message:
        msg_str += f"\n<pre>{html.escape(message)}</pre>\n\n"

    logger.error(tb_string)
    message = f"An exception was raised while handling an update{msg_str}\n<pre>{html.escape(tb_string)}</pre>"

    await bot.send_message(chat_id=admin_user_id, text=message, parse_mode=ParseMode.HTML)
