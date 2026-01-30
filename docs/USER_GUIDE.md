# User Guide: BTC 15-Minute Arbitrage Bot

This guide is for **people who want to run the bot** without editing code. You only need to:

1. Install Python and dependencies  
2. Create a `.env` file with your Polymarket credentials  
3. Run a few commands to check setup, then start the bot  

---

## What You Need Before Starting

- A **Polymarket account** (you can sign up with email at [polymarket.com](https://polymarket.com)).
- **USDC** in your Polymarket wallet (the bot trades with USDC).
- Your **Polymarket private key** (or the key for the wallet linked to Polymarket).  
  - If you use **email login (Magic.link)**, you will also need your **proxy wallet address** (see below).
- A computer that can run Python 3 and stay online (or a server/VPS).

---

## Step 1: Install the Bot

1. **Open a terminal** (Command Prompt on Windows, Terminal on Mac/Linux).

2. **Go to the bot folder** (where you downloaded or cloned the project):
   ```text
   cd path\to\15min-btc-polymarket-trading-bot
   ```

3. **Create a virtual environment** (recommended):
   - **Windows:**
     ```text
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```text
     python3 -m venv .venv
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```text
   pip install -r requirements.txt
   ```

---

## Step 2: Configure Your Credentials (.env)

1. **Copy the example env file:**
   - Copy `.env.example` to a new file named `.env` in the same folder.

2. **Edit `.env`** with a text editor and fill in at least these:

   | Variable | What to put |
   |----------|-------------|
   | `POLYMARKET_PRIVATE_KEY` | Your wallet private key (starts with `0x`). **Keep this secret.** |
   | `POLYMARKET_SIGNATURE_TYPE` | `0` = normal wallet (e.g. MetaMask), `1` = Polymarket email login (Magic.link) |
   | `POLYMARKET_FUNDER` | **Only if you use email login:** your Polymarket *proxy* wallet address (see below). Leave empty for normal wallet. |

3. **If you use Polymarket email login (Magic.link):**
   - Go to your Polymarket profile (e.g. `https://polymarket.com/@YourUsername`).
   - Find “Copy address” or your wallet address — that is your **proxy** address.
   - Put that address in `POLYMARKET_FUNDER` in `.env`.
   - Set `POLYMARKET_SIGNATURE_TYPE=1`.

4. **Generate API keys** (required for trading):
   ```text
   python -m src.create_api_keys
   ```
   The script will print **API Key**, **Secret**, and **Passphrase**. Add them to `.env`:
   - `POLYMARKET_API_KEY=...`
   - `POLYMARKET_API_SECRET=...`
   - `POLYMARKET_API_PASSPHRASE=...`

5. **Optional but important for safety:**
   - `DRY_RUN=true` — Bot runs in **simulation mode** (no real money). Start with this.
   - `TARGET_PAIR_COST=0.99` — Only trade when UP+DOWN cost ≤ $0.99 (you can use 0.991 or 0.995).
   - `ORDER_SIZE=5` — Number of shares per side (start small).

---

## Step 3: Check Your Setup

Before trading real money, run these:

1. **Check configuration** (wallet, API, balance):
   ```text
   python -m src.check_config
   ```
   Fix any errors it reports (e.g. missing `POLYMARKET_FUNDER` for Magic.link).

2. **Check balance** (see your USDC on Polymarket):
   ```text
   python -m src.check_balance
   ```
   You should see your USDC balance. If it’s $0 but you have funds on the website, double-check `POLYMARKET_SIGNATURE_TYPE` and `POLYMARKET_FUNDER`.

---

## Step 4: Run the Bot

1. **Simulation (no real trades)**  
   Make sure `.env` has:
   ```text
   DRY_RUN=true
   ```
   Then run:
   ```text
   python -m src.btc_15m_arb_bot
   ```
   The bot will scan for opportunities and log what it *would* do, without placing real orders.

2. **Live trading**  
   Only after you’re comfortable with simulation:
   - Set `DRY_RUN=false` in `.env`.
   - Ensure you have USDC in your Polymarket wallet.
   - Run the same command:
     ```text
     python -m src.btc_15m_arb_bot
     ```

3. **Stopping the bot**  
   Press **Ctrl+C** in the terminal. The bot will stop and, if configured, you may see a short summary.

---

## What the Bot Does When Running

- **Finds the current BTC 15-minute market** (automatically).
- **Scans the order book** for UP and DOWN prices.
- **Checks** if buying your `ORDER_SIZE` of UP and DOWN would cost in total **≤ TARGET_PAIR_COST** (e.g. $0.99).
- **If yes:** places two orders (buy UP, buy DOWN). In live mode it will only count a trade as done when both legs fill (with optional unwind if one leg fails).
- **When the market closes** (after 15 minutes), it looks for the **next** 15-minute market and continues.

You don’t need to change markets by hand; the bot switches automatically.

---

## Quick Reference: Commands

| What you want to do | Command |
|---------------------|--------|
| Create API keys and add to .env | `python -m src.create_api_keys` |
| Check wallet/API/config | `python -m src.check_config` |
| Check USDC balance | `python -m src.check_balance` |
| Run bot (simulation or live) | `python -m src.btc_15m_arb_bot` |

---

## Troubleshooting

- **“Invalid signature”**  
  - Use `python -m src.check_config` and fix what it suggests.  
  - For email login: set `POLYMARKET_SIGNATURE_TYPE=1` and `POLYMARKET_FUNDER` to your Polymarket profile wallet address.  
  - Regenerate keys: `python -m src.create_api_keys` and update `.env`.

- **Balance shows $0**  
  - For Magic.link: your funds are in the *proxy* wallet. Set `POLYMARKET_FUNDER` to that address.  
  - Run `python -m src.check_balance` to see which address is used and what balance the API reports.

- **“No active BTC 15min market found”**  
  - Markets roll every 15 minutes. Wait a bit and try again.  
  - Check internet; you can also open https://polymarket.com/crypto/15M in a browser to see if markets load.

- **Bot doesn’t trade**  
  - In simulation, it only *simulates* trades when the cost is below your threshold.  
  - In live, opportunities can disappear quickly; you can try lowering `TARGET_PAIR_COST` slightly (e.g. 0.991) or increasing `ORDER_SIZE` only if you understand the risk.

---

## Need help?

If you need help with this bot or have questions, contact on Telegram: **[@jerrix1](https://t.me/jerrix1)**

---

## Next Steps

- **Strategy details:** see [STRATEGY.md](STRATEGY.md).  
- **Full project docs and options:** see the main [README.md](../README.md) in the project root.
