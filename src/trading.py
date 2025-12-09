import functools
import logging
from typing import Optional

from py_clob_client.client import ClobClient

from .config import Settings

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def _client(settings_key: str, key: str, signature_type: int, funder: str) -> ClobClient:
    host = "https://clob.polymarket.com"
    return ClobClient(host, key=key, chain_id=137, signature_type=signature_type, funder=funder or None)


def get_client(settings: Settings) -> ClobClient:
    if not settings.private_key:
        raise RuntimeError("POLYMARKET_PRIVATE_KEY is required for trading")
    return _client("default", settings.private_key, settings.signature_type, settings.funder)


def get_balance(settings: Settings) -> float:
    """Get USDC balance from Polymarket account."""
    try:
        client = get_client(settings)
        # Get balances - returns dict with token addresses as keys
        balances = client.get_balance_allowance()
        # USDC on Polygon address
        usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        balance = float(balances.get(usdc_address, {}).get("balance", 0))
        return balance
    except Exception as e:
        logger.error(f"Error getting balance: {e}")
        return 0.0


def place_order(settings: Settings, *, side: str, token_id: str, price: float, size: float, tif: str = "GTC") -> dict:
    if price <= 0:
        raise ValueError("price must be > 0")
    if size <= 0:
        raise ValueError("size must be > 0")
    if not token_id:
        raise ValueError("token_id is required")

    side_up = side.upper()
    if side_up not in {"BUY", "SELL"}:
        raise ValueError("side must be BUY or SELL")

    client = get_client(settings)
    payload = {
        "price": price,
        "size": size,
        "side": side_up,
        "token_id": token_id,
        "time_in_force": tif,
    }
    try:
        return client.place_order(payload)
    except Exception as exc:  # pragma: no cover - passthrough from client
        raise RuntimeError(f"place_order failed: {exc}") from exc
