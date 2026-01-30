# BTC 15-Minute Arbitrage Strategy

This document explains **how** the bot makes money and **why** the strategy works, in plain language.

---

## What Are These Markets?

On Polymarket, **Bitcoin 15-minute markets** are binary prediction markets that ask:

> **"Will Bitcoin go UP or DOWN in the next 15 minutes?"**

- **UP (Yes)** — You win if Bitcoin’s price is higher at the end of the 15-minute window.
- **DOWN (No)** — You win if Bitcoin’s price is lower (or the same) at the end.

Each market lasts exactly 15 minutes. At settlement, **exactly one** of UP or DOWN pays **$1.00 per share**; the other pays **$0.00**.

---

## The Core Idea: Locked-In Profit

The bot does **not** try to guess whether Bitcoin will go up or down. Instead, it:

1. **Buys both sides** — It buys UP shares and DOWN shares.
2. **Only when the total cost is less than $1.00** — For example, UP at $0.48 and DOWN at $0.51 = $0.99 total.

**Why this works:**

- At the end of the 15 minutes, **one** of UP or DOWN pays $1.00 per share.
- You own one share of each.
- So you **always** receive $1.00 per pair, no matter which side wins.
- If you paid $0.99 for the pair, you keep **$0.01 profit per pair**.

That’s **pure arbitrage**: you lock in a profit by buying both outcomes when the combined price is below the guaranteed payout.

---

## Example (Numbers)

| Item              | Value   |
|-------------------|--------|
| UP price          | $0.48  |
| DOWN price        | $0.51  |
| **Total cost**    | **$0.99** |
| Payout (one side) | $1.00  |
| **Profit per share** | **$0.01** |

If you buy **5 shares** of each (5 UP + 5 DOWN):

- You spend: 5 × $0.99 = **$4.95**
- You receive at settlement: 5 × $1.00 = **$5.00**
- **Profit: $0.05** (about 1.01%)

The bot only places this trade when the **actual fillable cost** (walking the order book for your size) is at or below your configured threshold (e.g. $0.99).

---

## Why Does the Opportunity Exist?

In theory, UP + DOWN should always equal $1.00 (one of them must happen). In practice:

- **Liquidity** — Different people place orders on each side at different times.
- **Volatility** — Prices move; sometimes one side is cheap and the other expensive.
- **Spreads** — Bid/ask spreads can create a window where buying both sides is still below $1.00.

The bot **scans the order book** (real buy/sell orders) and computes the price needed to fill your order size. It only trades when that total cost is **below your threshold** (e.g. `TARGET_PAIR_COST=0.99`).

---

## Risk and Caveats

1. **Execution risk** — By the time your orders hit the exchange, prices can move. The bot uses **fill-or-kill (FOK)** style behavior where possible so you don’t end up with only one leg filled.
2. **Slippage** — For larger sizes, the “walk the book” cost might be higher than the best ask; the bot uses a worst-case fill estimate.
3. **Market closure** — Each market lasts 15 minutes; the bot automatically switches to the next market when the current one closes.
4. **Fees and spread** — Real profit is after any fees; the threshold you set should account for that.

---

## Summary

| Concept              | Explanation |
|----------------------|-------------|
| **Strategy**         | Buy UP + DOWN when total cost &lt; $1.00 per pair. |
| **Why it works**     | One of UP or DOWN always pays $1.00; you always get $1.00 per pair. |
| **When the bot trades** | When order-book cost for your size ≤ your cost threshold. |
| **No prediction**     | The bot does not bet on direction; it only enters when the numbers guarantee a profit. |

For step-by-step setup and usage (no coding required), see [USER_GUIDE.md](USER_GUIDE.md).
