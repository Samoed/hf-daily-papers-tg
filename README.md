# HF Daily Papers Telegram Bot

Telegram bot that posts the latest Hugging Face papers and blog updates to a channel. You can see it live here: https://t.me/hf_dailypapers

## Features
- Daily digest of yesterday's Hugging Face papers with titles, abstracts, AI summaries, and GitHub/project links when available.
- Daily digest of Hugging Face blog and community posts, ordered by upvotes.
- Weekly leaderboard of top papers.
- Admin notifications about start/end of runs and error traces.

## Quickstart
1) Requirements: Python 3.10+ and `uv` or `pip` for dependencies.
2) Install deps (example with `uv`):
   ```bash
   uv sync
   ```
3) Create a `.env` in the repo root:
   ```env
   TG__BOT_TOKEN=123456:bot-token
   TG__ADMIN_USER_ID=123456789          # Telegram user ID to receive status/errors
   TG__CHANNEL_ID=-1001234567890        # Target channel ID (use a negative ID for channels)
   HF_API_BASE_URL=https://huggingface.co/api
   TIMEZONE=Europe/Moscow               # Any IANA timezone name
   WEEKLY_FETCH_DAYS=7
   WEEKLY_TOP=20
   ```
4) Run a job:
   - Daily papers: `uv run python -m hf_daily_papers_tg.commands.daily_papers`
   - Daily posts: `uv run python -m hf_daily_papers_tg.commands.daily_posts`
   - Weekly top papers: `uv run python -m hf_daily_papers_tg.commands.weekly_papers`

Each command sends a start message to the admin, publishes to the channel, and reports errors to the admin chat.

## Scheduling
Use a scheduler (cron/systemd/GitHub Actions) to run the commands. The bot uses `TIMEZONE` to determine "yesterday" for daily jobs and the start date for the weekly leaderboard.

## Development
- Format/lint: `make format`
- Type-check: `make typecheck`

HuggingFace API reference https://huggingface.co/spaces/huggingface/openapi or https://huggingface-openapi.hf.space/
