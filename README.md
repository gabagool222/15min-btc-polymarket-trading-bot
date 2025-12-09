# Bitcoin 15min Arbitrage Bot - Polymarket

Simple arbitrage bot implementing **Jeremy Whittaker's strategy** for Bitcoin 15-minute markets on Polymarket.

## 🎯 Strategy

**Pure arbitrage**: Buy both sides (UP + DOWN) when total cost < $1.00 to guarantee profit regardless of outcome.

### Example:
```
BTC goes up (UP):     $0.48
BTC goes down (DOWN): $0.51
─────────────────────────
Total:                $0.99  ✅ < $1.00
Profit:               $0.01 per share (1.01%)
```

**Why does it work?**
- At close, ONE of the two sides pays $1.00 per share
- If you paid $0.99 total, you earn $0.01 no matter which side wins
- It's **guaranteed profit** (pure arbitrage)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Jonmaa/btc-polymarket-bot.git
cd btc-polymarket-bot
```

2. **Create virtual environment and install dependencies:**
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. **Configure environment variables:**

Copy `.env.example` to `.env` and configure:
```env
POLYMARKET_PRIVATE_KEY=0x...
POLYMARKET_API_KEY=...
POLYMARKET_API_SECRET=...
POLYMARKET_API_PASSPHRASE=...
TARGET_PAIR_COST=0.991
ORDER_SIZE=5
DRY_RUN=true
```

## 💻 Usage

**Simulation mode** (recommended first):
```bash
python -m src.simple_arb_bot
```

**Live mode** (change `DRY_RUN=false` in `.env`):
```bash
python -m src.simple_arb_bot
```

## ⚙️ Configuration

### Required variables:
- `POLYMARKET_PRIVATE_KEY` - Your Polymarket private key
- `POLYMARKET_API_KEY` - Polymarket API key
- `POLYMARKET_API_SECRET` - Polymarket API secret
- `POLYMARKET_API_PASSPHRASE` - Polymarket API passphrase

### Optional variables:
- `TARGET_PAIR_COST` (default: 0.99) - Threshold to detect arbitrage
- `ORDER_SIZE` (default: 5) - Number of shares per trade
- `DRY_RUN` (default: true) - Simulation mode vs live trading

## 📊 Features

✅ **Auto-discovers** active BTC 15min market  
✅ **Detects opportunities** when price_up + price_down < threshold  
✅ **Continuous scanning** with no delays (maximum speed)  
✅ **Auto-switches** to next market when current one closes  
✅ **Final summary** with total investment, profit and market result  
✅ **Simulation mode** for risk-free testing  

## 📈 Example Output

```
🚀 BITCOIN 15MIN ARBITRAGE BOT STARTED
======================================================================
Market: btc-updown-15m-1765301400
Time remaining: 12m 34s
Mode: 🔸 SIMULATION
Cost threshold: $0.99
Order size: 5.0 shares
======================================================================

🎯 ARBITRAGE OPPORTUNITY DETECTED
======================================================================
Price UP (rises):     $0.4800
Price DOWN (falls):   $0.5100
Total cost:           $0.9900
Profit per share:     $0.0100
Profit %:             1.01%
----------------------------------------------------------------------
Total investment:     $4.95
Expected payout:      $5.00
EXPECTED PROFIT:      $0.05
======================================================================

🏁 MARKET CLOSED - FINAL SUMMARY
======================================================================
Market: btc-updown-15m-1765301400
Result: UP (rises) 📈
Mode: 🔸 SIMULATION
----------------------------------------------------------------------
Total opportunities detected:  842
Total trades executed:         842
Total shares bought:           8420
----------------------------------------------------------------------
Total invested:                $4175.50
Expected payout at close:      $4210.00
Expected profit:               $34.50 (0.83%)
======================================================================
```

## ⚠️ Warnings

- ⚠️ **DO NOT use `DRY_RUN=false` without funds** in your Polymarket wallet
- ⚠️ **Spreads** can eliminate profit (verify liquidity)
- ⚠️ Markets close every **15 minutes** (don't accumulate positions)
- ⚠️ Start with **small orders** (ORDER_SIZE=5)
- ⚠️ This software is **educational only** - use at your own risk

## 📚 Resources

- [Jeremy Whittaker's original article](https://jeremywhittaker.com/index.php/2024/09/24/arbitrage-in-polymarket-com/)
- [Polymarket](https://polymarket.com/)
- [BTC 15min Markets](https://polymarket.com/crypto/15M)

## 📁 Project Structure

```
Bot/
├── src/
│   ├── simple_arb_bot.py  # Main arbitrage bot
│   ├── config.py          # Configuration
│   ├── lookup.py          # Market ID fetcher
│   └── trading.py         # Order execution
├── .env                   # Environment variables
├── .env.example          # Environment template
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## ⚖️ Disclaimer

This software is for educational purposes only. Trading involves risk. I am not responsible for financial losses. Always do your own research and never invest more than you can afford to lose.
