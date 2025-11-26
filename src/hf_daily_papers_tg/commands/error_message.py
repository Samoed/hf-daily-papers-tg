import html
import logging
import traceback

from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)


async def send_error_message(bot: Bot, admin_user_id: int, exception: Exception, message: str | None = None) -> None:
    """Send an error message to the admin user."""
    traceback.print_exception(type(exception), exception, exception.__traceback__)
    msg_str = ""
    if message:
        msg_str += f"\n<pre>{html.escape(message)}</pre>\n\n"

    message = f"An exception was raised while handling an update{msg_str}"

    await bot.send_message(chat_id=admin_user_id, text=message, parse_mode=ParseMode.HTML)
