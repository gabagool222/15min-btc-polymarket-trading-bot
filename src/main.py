import asyncio
from dataclasses import replace

from .config import load_settings, Settings
from .lookup import fetch_market_from_slug, next_slug, parse_iso
from .bot import HedgedBot


async def run_sequence():
    base_settings: Settings = load_settings()
    if not base_settings.market_slug:
        raise SystemExit("POLYMARKET_MARKET_SLUG is required for automatic rotation")

    slug = base_settings.market_slug
    while True:
        info = fetch_market_from_slug(slug)
        end_dt = parse_iso(info.get("end_date"))
        if base_settings.verbose:
            print(f"[main] slug={slug} question={info.get('question')} end={end_dt}")
        market_settings = replace(
            base_settings,
            market_slug=slug,
            market_id=info["market_id"],
            yes_token_id=info["yes_token_id"],
            no_token_id=info["no_token_id"],
        )
        bot = HedgedBot(market_settings, end_time=end_dt)
        result = await bot.run_once()
        if market_settings.verbose:
            print(f"[{slug}] {result}")
        slug = next_slug(slug)


if __name__ == "__main__":
    asyncio.run(run_sequence())
