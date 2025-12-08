# Polymarket Hedged Bot (Skeleton)

This repo sketches a 15-minute Polymarket hedging bot inspired by the "pair cost < 1" strategy (avg YES + avg NO below 1). It connects to the Polymarket CLOB websocket, watches order book mispricings, and asymmetrically adds YES/NO until profit is locked.

## Quick start
1) Create a virtualenv and install deps:
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2) Set env vars (see `.env.example`). Define `POLYMARKET_MARKET_SLUG` (e.g. `btc-updown-15m-1765176300`). Default WS endpoint: `wss://ws-subscriptions-clob.polymarket.com`.
3) Run el bot (rota automáticamente cada 15m usando el slug base):
```
python -m src.main
```

### Obtener IDs vía slug (herramienta interna)
```
python -m src.lookup btc-updown-15m-1765176300
```
Devuelve `market_id`, `yes_token_id`, `no_token_id` y outcomes. El `main` ya lo hace automáticamente antes de cada ventana.

## Configuration
Environment variables (see defaults in `src/config.py`):
- `POLYMARKET_API_KEY` / `POLYMARKET_API_SECRET`: trading credentials.
- `POLYMARKET_MARKET_ID`: 15m BTC market id for order book subscription.
- `POLYMARKET_YES_TOKEN_ID` / `POLYMARKET_NO_TOKEN_ID`: outcome token ids for orders.
- `POLYMARKET_WS_URL`: websocket endpoint (default `wss://clob.polymarket.com/ws`).
- `TARGET_PAIR_COST`: max combined average cost (default 0.99).
- `BALANCE_SLACK`: allowed qty imbalance fraction (default 0.15).
- `ORDER_SIZE`: per-order size (default 50).
- `YES_BUY_THRESHOLD` / `NO_BUY_THRESHOLD`: price thresholds to consider a buy (defaults 0.45 / 0.45).
- `VERBOSE`: set `true` for console messages.

## How the strategy is encoded
- State tracks `qty_yes`, `qty_no`, `cost_yes`, `cost_no`.
- A buy sim is accepted only if new pair cost stays below `TARGET_PAIR_COST` and quantities remain balanced.
- Lock condition: `pair_cost < 1.0` and `min(qty_yes, qty_no) > (cost_yes + cost_no)`.
- One run handles a single market window; reset state between windows or restart the process.

## Notes
- `place_order_stub` currently logs and sends an unauthenticated payload; replace with signed trading messages when API keys are available.
- Add persistence/logging for production use and guard against disconnections.
