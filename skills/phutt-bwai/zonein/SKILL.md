---
name: zonein
version: 2.0.0
description: |
  Fetch live smart money signals from Polymarket and HyperLiquid via Zonein API.
  Create, configure, and manage AI trading agents that follow smart money.
  Use PROACTIVELY when user asks about:
  (1) Prediction market signals, whales, smart bettors
  (2) Crypto perp trading signals, long/short sentiment
  (3) Leaderboard, top traders, wallet tracking
  (4) Create/manage trading agents (agent creation flow)
  (5) Market overview, crypto sentiment, smart money flow
  (6) Agent performance, stats, trades, vault balance
  Always use the bundled script — never call the API with inline code.
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz/pm\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---

# Zonein — Smart Money Intelligence

Fetch live trading intelligence from Polymarket and HyperLiquid smart money wallets using the bundled script.

## Setup (credentials)

### Get Your API Key

1. Go to **https://app.zonein.xyz/pm**
2. Log in with your account (you need a referral code to register)
3. Click the **"Get API Key"** button
4. Copy your API key (starts with `zn_`)

### Set API Key in OpenClaw

**Option A — Gateway Dashboard (recommended):**
1. Open your **OpenClaw Gateway Dashboard**
2. Go to **`/skills`** in the sidebar
3. Find **"zonein"** in Workspace Skills → click **Enable**
4. Enter your `ZONEIN_API_KEY` and save

**Option B — Environment variable:**
```bash
export ZONEIN_API_KEY="zn_your_key_here"
```

**Option C — The script also reads from `~/.openclaw/openclaw.json`** automatically (skills.entries.zonein.apiKey).

## Quick Reference

| User asks... | Command |
|-------------|---------|
| "What's happening in the market?" | `signals --limit 5` + `perp-signals --limit 5` |
| "Show me PM signals for politics" | `signals --categories POLITICS --limit 10` |
| "What are whales doing on crypto?" | `perp-signals --limit 10` |
| "Top Polymarket traders this week" | `leaderboard --period WEEK --limit 10` |
| "Which coins are smart money long?" | `perp-coins` |
| "Best perp traders this month" | `perp-top --period month --limit 10` |
| "Track wallet 0x..." | `trader 0x...` or `perp-trader 0x...` |
| "Where is smart money flowing?" | `signals --limit 10` + `perp-signals --limit 10` + `perp-coins` |
| "Create a trading agent" | Follow Agent Creation Flow (Step 1–6) |
| "List my agents" | `agents` |
| "How is my agent doing?" | `agent-stats <id>` + `agent-trades <id>` |
| "Stop my agent" | `agent-disable <id>` |
| "What agent types are available?" | `agent-templates` |
| "Check my agent's balance" | `agent-balance <id>` |
| "What positions does my agent have?" | `agent-positions <id>` |
| "How do I fund my agent?" | `agent-deposit <id>` then send USDC, then `agent-fund <id>` to bridge to Hyperliquid |
| "Open a BTC long for $100" | `agent-open <id> --coin BTC --direction LONG --size 100` |
| "Close my ETH position" | `agent-close <id> --coin ETH` |
| "Withdraw my funds" | `agent-disable <id>` then `agent-withdraw <id> --to 0x...` |

## Commands

**Presentation Rules:**
- Present results in natural, readable language. Format numbers, tables, and summaries nicely.
- If the user asks to see raw JSON or the actual command, you may show it.

**Read-only commands (safe to run without asking):**
`signals`, `leaderboard`, `consensus`, `trader`, `perp-signals`, `perp-traders`, `perp-top`, `perp-categories`, `perp-coins`, `perp-trader`, `agents`, `agent-get`, `agent-stats`, `agent-trades`, `agent-vault`, `agent-templates`, `agent-assets`, `agent-categories`, `agent-balance`, `agent-positions`, `agent-deposit`, `agent-orders`, `status`

**Financial commands (ALWAYS ask user for confirmation before executing):**
`agent-fund`, `agent-open`, `agent-close`, `agent-withdraw`, `agent-enable`, `agent-deploy`

**Example — user deposits USDC and asks to check balance:**
- You run: `agent-balance <id>` (read-only, safe)
- You see: `arbitrum_usdc: 200, needs_funding: true`
- You tell the user: "Your vault has 200 USDC on Arbitrum but it hasn't been bridged to Hyperliquid yet. Would you like me to bridge it now so your agent can start trading?"
- Only run `agent-fund <id>` after user confirms

All commands use the bundled Python script. **Always use these commands — never write inline API calls.**

Prefix: `python3 skills/zonein/scripts/zonein.py`

### `signals` — PM smart money trading signals

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--limit` | int | 20 | 1–100 | Max signals to return |
| `--categories` | str | all | `POLITICS,CRYPTO,SPORTS,CULTURE,ECONOMICS,TECH,FINANCE` | Comma-separated filter |
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | Lookback period |
| `--min-wallets` | int | 3 | ≥1 | Minimum smart wallets for consensus |

### `leaderboard` — PM top traders by PnL

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | Ranking period |
| `--category` | str | OVERALL | `OVERALL`, `POLITICS`, `SPORTS`, `CRYPTO`, `CULTURE`, `ECONOMICS`, `TECH`, `FINANCE` | Category filter |
| `--limit` | int | 20 | 1–500 | Max traders to return |

### `consensus` — PM positions where smart bettors agree

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--min-bettors` | int | 3 | Minimum bettors agreeing on a position |

### `trader` — PM trader profile by wallet

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `wallet` | str | yes | Polymarket wallet address (0x...) |

### `perp-signals` — Perp trading signals (HyperLiquid)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 20 | Max signals to return |
| `--min-wallets` | int | 3 | Minimum wallets for consensus |
| `--min-score` | float | 0 | Minimum trader credibility score (0–100) |

### `perp-traders` — Perp smart money traders

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--limit` | int | 20 | Max traders to return |
| `--min-score` | float | 0 | Minimum trader score (0–100) |
| `--categories` | str | all | Comma-separated: `swing_trading`, `large_cap_trader`, `high_win_rate`, `scalper`, etc. |

### `perp-top` — Perp top performers by PnL

| Param | Type | Default | Values | Description |
|-------|------|---------|--------|-------------|
| `--limit` | int | 10 | 1–100 | Max traders |
| `--period` | str | month | `day`, `week`, `month` | PnL ranking period |

### `perp-coins` — Coin distribution (long vs short sentiment)

No parameters. Returns all coins with smart money positions.

### `perp-categories` — Perp trader category list

No parameters.

### `perp-trader` — Perp trader details by address

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `address` | str | yes | HyperLiquid wallet address (0x...) |

### Agent Management

### `agents` — List your trading agents

No parameters.

### `agent-get` — Get full agent config and state

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID (e.g. `agent_abc12345`) |

### `agent-create` — Create a new trading agent

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `--name` | str | required | Agent display name |
| `--type` | str | composite | `composite`, `momentum_hunter`, `stable_grower`, `precision_master`, `whale_follower`, `scalping_pro`, `swing_trader` |
| `--assets` | str | BTC,ETH | Comma-separated: `BTC,ETH,SOL,HYPE` |
| `--categories` | str | auto from type | Comma-separated smart money categories |
| `--leverage` | int | 5 | Max leverage (1–20) |
| `--description` | str | auto | Agent description |
| `--risk-per-trade` | float | 1 | Risk per trade % |
| `--max-daily-loss` | float | 3 | Max daily loss % |
| `--risk-reward` | str | 1:2 | Risk:reward ratio |
| `--max-trades-per-day` | int | 3 | Max trades per day |
| `--min-confidence` | float | 0.8 | Min LLM confidence (0–1) |
| `--min-consensus` | float | 0.7 | Min smart money consensus (0–1) |

### `agent-update` — Update agent configuration

| Param | Type | Description |
|-------|------|-------------|
| `agent_id` | str | Agent ID (positional) |
| `--name` | str | New name |
| `--assets` | str | Comma-separated assets |
| `--categories` | str | Comma-separated categories |
| `--leverage` | int | Max leverage |
| `--methodology` | str | Trading methodology text |
| `--entry-strategy` | str | Entry strategy text |
| `--exit-framework` | str | Exit framework text |

### `agent-deploy` — Validate config and enable trading

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent to deploy |

### `agent-enable` / `agent-disable` / `agent-pause` — Lifecycle control

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-delete` — Delete agent (soft delete)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-stats` — Performance statistics (PnL, win rate)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-trades` — Trade history

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 50 | Max trades to return |

### `agent-vault` — Vault (trading wallet) info

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

### `agent-balance` — Live vault balance from Hyperliquid

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns: `account_value`, `withdrawable`, `has_positions`, `vault_address`.

### `agent-positions` — Open positions (live from Hyperliquid)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns each position: `coin`, `side` (LONG/SHORT), `size`, `entry_price`, `unrealized_pnl`, `leverage`, `notional`.

### `agent-deposit` — Get deposit address for funding agent

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

Returns: `deposit_address` (send USDC on Arbitrum One to this address).

### `agent-fund` — Bridge USDC from Arbitrum to Hyperliquid

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |

After sending USDC to the vault address on Arbitrum, call this to auto-bridge funds into Hyperliquid.
Privy sponsors gas — no ETH needed. Returns `tx_hash` and `amount` bridged.

### `agent-open` — Open a position (manual order via chat)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--coin` | str | yes | BTC, ETH, SOL, HYPE |
| `--direction` | str | no (default LONG) | LONG or SHORT |
| `--size` | float | yes | Position size in USD |
| `--leverage` | int | no | Leverage (1–20) |

### `agent-close` — Close a position

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--coin` | str | yes | Coin to close (BTC, ETH, SOL, HYPE) |

### `agent-orders` — Manual order history

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `agent_id` | str | required | Agent ID |
| `--limit` | int | 20 | Max orders to return |

### `agent-withdraw` — Withdraw funds to your wallet

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | str | yes | Agent ID |
| `--to` | str | yes | Destination 0x... wallet address on Arbitrum |

Agent must be **disabled** before withdrawing. Flow: Hyperliquid → Arbitrum → your wallet.

### `agent-templates` — Agent types & default config

No parameters. Returns available agent types with their category presets and default risk/trading config.

### `agent-assets` — Available trading assets

No parameters. Returns: BTC, ETH, SOL, HYPE.

### `agent-categories` — Smart money categories with live stats

No parameters. Returns all categories with description and live trader counts.

### `status` — Check API key status

No parameters.

## Operational Flows

### 🤖 Agent Creation Flow

When user wants to create a trading agent, follow this conversational flow:

**Step 1: Collect Preferences**
Ask the user about their trading goals:
- What coins do you want to trade? (BTC, ETH, SOL, HYPE)
- What's your risk tolerance? (conservative, moderate, aggressive)
- What trading style? (scalping, swing trading, momentum, balanced)
- How much leverage? (1x–20x)
- Max daily loss tolerance? (1%–10%)

**Step 2: Show Available Options**
Run these commands to give user context:
1. `agent-templates` — show available agent types
2. `agent-categories` — show smart money categories with stats
3. `agent-assets` — show available coins

**Step 3: Create Agent**
Based on collected preferences, create the agent:
```bash
python scripts/zonein/scripts/zonein.py agent-create --name "BTC Swing Trader" --type swing_trader --assets BTC,ETH --leverage 5 --risk-per-trade 1 --max-daily-loss 3 --risk-reward 1:2 --max-trades-per-day 3 --min-confidence 0.8 --min-consensus 0.7
```

**Step 4: Configure Strategy**
Update the agent with trading strategy prompts:
```bash
python scripts/zonein/scripts/zonein.py agent-update <agent_id> --methodology "Follow smart money signals..." --entry-strategy "Enter on SM consensus >70%..." --exit-framework "Take profit at +10%, stop loss at -5%..."
```

**Step 5: Review & Deploy**
1. `agent-get <agent_id>` — review full config
2. `agent-deploy <agent_id>` — validate and enable

**Step 6: Fund the Agent**
The vault (deposit address) is auto-created with the agent. The create response includes it.
1. Show user the deposit address from the create response (or use `agent-deposit <agent_id>`)
2. Tell user: "Send USDC to this address on Arbitrum One."
3. `agent-balance <agent_id>` — check `arbitrum_usdc` field to confirm deposit arrived
4. `agent-fund <agent_id>` — bridge USDC from Arbitrum into Hyperliquid (gasless, no ETH needed)
5. `agent-balance <agent_id>` — confirm Hyperliquid `account_value` shows the funds

**Step 7: Monitor**
- `agent-balance <agent_id>` — check vault balance
- `agent-positions <agent_id>` — view open positions
- `agent-stats <agent_id>` — check performance (PnL, win rate)
- `agent-trades <agent_id>` — view trade history
- `agent-disable <agent_id>` — stop trading if needed

### 💰 Deposit & Withdraw Flow

**Deposit:**
1. `agent-deposit <agent_id>` — get vault address
2. User sends USDC to vault address on **Arbitrum One**
3. `agent-balance <agent_id>` — check `arbitrum_usdc` to verify deposit arrived
4. `agent-fund <agent_id>` — bridge USDC from Arbitrum → Hyperliquid (gasless)
5. `agent-balance <agent_id>` — confirm `account_value` on Hyperliquid

**Withdraw:**
1. `agent-disable <agent_id>` — must disable agent first
2. `agent-withdraw <agent_id> --to 0xYourWallet...` — queue withdrawal
3. System processes: Hyperliquid → Arbitrum → your wallet

### 📊 Position Management via Chat

When user wants to check positions or trade manually:

**Check positions:**
```bash
python scripts/zonein/scripts/zonein.py agent-positions <agent_id>
```
Present each position: "BTC LONG — $500 at $95,432 entry — PnL: +$23.45 — 5x leverage"

**Open a position:**
```bash
python scripts/zonein/scripts/zonein.py agent-open <agent_id> --coin BTC --direction LONG --size 100 --leverage 5
```

**Close a position:**
```bash
python scripts/zonein/scripts/zonein.py agent-close <agent_id> --coin BTC
```

**Check order status:**
```bash
python scripts/zonein/scripts/zonein.py agent-orders <agent_id>
```

### Market Overview

When user asks about market conditions, run these in sequence:
1. `signals --limit 5` — top PM signals
2. `perp-signals --limit 5` — top perp signals
3. `perp-coins` — coin long/short sentiment
4. Summarize: which markets have strong agreement, which coins whales are bullish/bearish on

### Trading Signals

1. Ask: prediction markets, perp, or both?
2. Run the relevant command(s)
3. Present top signals sorted by consensus strength
4. Explain each signal, e.g.: "5 top-100 traders all say YES on 'Will BTC hit $100k?' — current price 42c"

### Track a Wallet

1. `trader <wallet>` — Polymarket profile
2. `perp-trader <address>` — HyperLiquid profile
3. Present: performance, open positions, win rate

## Output Fields

### PM Signal
- `direction` — YES or NO
- `consensus` — 0 to 1 (1 = everyone agrees)
- `total_wallets` — how many smart traders hold this
- `best_rank` — best leaderboard position
- `cur_yes_price` / `cur_no_price` — current prices

### Perp Signal
- `coin` — token (BTC, ETH, SOL, HYPE...)
- `direction` — LONG or SHORT
- `consensus` — agreement ratio (0-1)
- `long_wallets` / `short_wallets` — traders per side
- `long_value` / `short_value` — USD per side
- `best_trader_score` — credibility score

### Periods & Categories
- **PM Periods:** DAY, WEEK, MONTH, ALL
- **PM Categories:** OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, ECONOMICS, TECH, FINANCE
- **Perp Periods:** day, week, month

## How to Present Results

### PM Signal
```
🔮 [market_title]
Smart money says: [YES/NO] | Agreement: [X]%
[N] top traders holding | Best ranked: #[rank]
Current price: YES [price] / NO [price]
```

### Perp Signal
```
📊 $[COIN]
Smart money says: [LONG/SHORT] | Agreement: [X]%
[N] whale traders | Top score: [score]
Long: $[X] | Short: $[X]
```

## Important

- Signals show what smart money is doing — not guaranteed outcomes
- Past performance does not predict future results
- Never invest more than you can afford to lose
- Always use the bundled script. Never construct raw API calls with curl or inline Python.

## External Endpoints

| URL | Data Sent |
|-----|-----------|
| `https://mcp.zonein.xyz/api/v1/*` | API key (X-API-Key header) + query parameters |

## Security & Privacy

- Only your API key leaves the machine (sent to mcp.zonein.xyz)
- No personal data is sent beyond the key
- All data is read-only (the script only makes GET requests)

## Trust Statement

By using this skill, your API key and query parameters are sent to https://mcp.zonein.xyz. Only install if you trust Zonein.

## Links

- **Dashboard:** https://app.zonein.xyz/pm/
- **Perp Dashboard:** https://app.zonein.xyz/perp/
- **API Docs:** https://mcp.zonein.xyz/docs
