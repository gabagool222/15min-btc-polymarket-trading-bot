import asyncio
import json
from typing import AsyncIterator, Callable, Dict, Any, List

import websockets


class OrderBookStream:
    def __init__(self, ws_url: str, asset_ids: List[str], verbose: bool = False):
        self.ws_url = ws_url.rstrip("/")
        self.asset_ids = asset_ids
        self.verbose = verbose

    async def __aenter__(self):
        # Market channel per docs: wss://ws-subscriptions-clob.polymarket.com/ws/market
        target = f"{self.ws_url}/ws/market"
        if self.verbose:
            print(f"[ws] connecting to {target}")
        self._conn = await websockets.connect(target, ping_interval=20)
        payload = {"type": "market", "assets_ids": self.asset_ids}
        if self.verbose:
            print(f"[ws] subscribe payload: {payload}")
        await self._conn.send(json.dumps(payload))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._conn.close()

    async def messages(self) -> AsyncIterator[Dict[str, Any]]:
        while True:
            raw = await self._conn.recv()
            yield json.loads(raw)


async def place_order_stub(send: Callable[[str], Any], *, side: str, token_id: str, price: float, size: float) -> None:
    # Replace with authenticated WS trading message once keys are available.
    order = {
        "type": "place_order",
        "side": "buy",
        "token_id": token_id,
        "price": price,
        "size": size,
        "time_in_force": "GTC",
        "client_order_id": f"demo-{side.lower()}-{price}-{size}",
    }
    await send(json.dumps(order))


async def send_json(ws, payload: dict) -> None:
    await ws.send(json.dumps(payload))
