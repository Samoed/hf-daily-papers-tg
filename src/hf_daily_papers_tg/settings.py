from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseModel):
    bot_token: str
    admin_user_id: int
    channel_id: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env")

    tg: TelegramSettings
    hf_api_base_url: str = "https://huggingface.co/api"
    timezone: ZoneInfo = ZoneInfo("Europe/Moscow")
    weekly_fetch_days: int = 7
    weekly_top: int = 20
