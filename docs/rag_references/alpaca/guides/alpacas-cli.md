# Trading CLI

Source: https://docs.alpaca.markets/us/docs/alpacas-cli.md

---
updatedAt: 2026-06-08T14:37:01.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Trading CLI

Alpaca's CLI is a command-line interface that provides direct access to Alpaca's Trading and Market Data APIs from the terminal. Trade stocks, options, and crypto, query market data, manage your account, and automate workflows; all without writing HTTP requests.

> **Alpha Preview** — This CLI is under active development. Commands, flags, and output formats may change without notice between releases.

**GitHub:** [alpacahq/cli](https://github.com/alpacahq/cli) | **License:** Apache 2.0

## What You Can Do

* **Trade**: Submit, replace, and cancel orders for stocks, options, and crypto with explicit flags and structured output
* **Market data**: Pull bars, quotes, trades, snapshots, screeners, news, option chains, and crypto orderbooks
* **Account management**: Check balances, positions, portfolio history, activity logs, and account configuration
* **Watchlists**: Create, update, and manage watchlists by name or ID
* **Automate**: Pipe JSON output into scripts, cron jobs, CI pipelines, or AI agent sessions

## Installation

### Go

```bash
go install github.com/alpacahq/cli/cmd/alpaca@latest
```

Make sure `$GOPATH/bin` (typically `~/go/bin`) is on your `PATH`.

### Homebrew (macOS / Linux)

```bash
brew install alpacahq/tap/cli
```

### Verify

```bash
alpaca version
alpaca doctor
```

## Authentication

Paper trading is the default. You can authenticate in two ways:

### OAuth (Paper Trading)

Opens a browser for authentication. No API keys, config files, or environment variables needed:

```bash
alpaca profile login
```

### API Keys (Paper or Live)

```bash
# Paper trading with API keys
alpaca profile login --api-key

# Live trading with API keys
alpaca profile login --api-key --live
```

### Multiple Profiles

You can manage multiple profiles and switch between them:

```bash
alpaca profile list
alpaca profile switch <name>
alpaca profile logout <name>
```

### Environment Variables (CI / Agents)

For scripts and automation, set API keys as environment variables:

```bash
export ALPACA_API_KEY=PK...
export ALPACA_SECRET_KEY=...
alpaca account get
```

## Configuration

| Variable            | Description                                |
| :------------------ | :----------------------------------------- |
| `ALPACA_API_KEY`    | API key ID (used with `ALPACA_SECRET_KEY`) |
| `ALPACA_SECRET_KEY` | Secret key                                 |
| `ALPACA_LIVE_TRADE` | Set `true` for live trading                |
| `ALPACA_PROFILE`    | Active profile name                        |
| `ALPACA_OUTPUT`     | Default format (`json` or `csv`)           |
| `ALPACA_CONFIG_DIR` | Config directory override                  |

Credentials are stored in `~/.config/alpaca/profiles/` with 0600 permissions.

## Output Formats

Every command returns structured JSON by default. Use flags to reshape output:

```bash
# JSON (default)
alpaca position list

# CSV
alpaca position list --csv

# Filtered JSON with built-in jq (no external jq needed)
alpaca position list --jq '[.[] | {symbol, qty, unrealized_pl}]'

# Quiet mode (suppress non-essential output)
alpaca account get --quiet
```

## Commands

### Account & Portfolio

```bash
alpaca account get                  # Account details (equity, buying power)
alpaca account config get           # Account configuration
alpaca account config set           # Update account configuration
alpaca account activity list        # Activity log (fills, dividends, transfers)
alpaca account portfolio            # Portfolio equity and P&L history
```

### Orders

```bash
alpaca order submit --symbol AAPL --side buy --qty 10 --type market
alpaca order submit --symbol AAPL --side buy --qty 10 --type limit --limit-price 185
alpaca order list                   # List orders (default: open)
alpaca order list --status all      # All orders
alpaca order get --order-id <id>    # Single order
alpaca order replace --order-id <id> --qty 20
alpaca order cancel --order-id <id>
alpaca order cancel-all

# Preview an order without submitting
alpaca order submit --symbol AAPL --side buy --qty 10 --type market --dry-run
```

### Positions

```bash
alpaca position list                # All open positions
alpaca position get --symbol AAPL   # Single position
alpaca position close --symbol AAPL # Close a position
alpaca position close-all           # Liquidate entire portfolio
```

### Options

```bash
alpaca option contracts --underlying-symbol AAPL
alpaca option get --symbol-or-id AAPL250620C00200000
alpaca option exercise --symbol-or-id <contract>
alpaca option do-not-exercise --symbol-or-id <contract>
```

### Market Data — Stocks

```bash
alpaca data bars --symbol AAPL --start 2025-01-01 --timeframe 1Day
alpaca data quotes --symbol AAPL --start 2025-06-01
alpaca data trades --symbol AAPL --start 2025-06-01
alpaca data latest-bar --symbol AAPL
alpaca data latest-quote --symbol AAPL
alpaca data latest-trade --symbol AAPL
alpaca data snapshot --symbol AAPL
alpaca data screener most-actives
alpaca data screener movers
```

### Market Data — Crypto

```bash
alpaca data crypto bars --symbol BTC/USD --start 2025-01-01 --timeframe 1Day
alpaca data crypto latest-quotes --symbol BTC/USD,ETH/USD
alpaca data crypto snapshots --symbol BTC/USD
alpaca data crypto-orderbook --symbol BTC/USD
```

### Market Data — Options

```bash
alpaca data option chain --underlying-symbol AAPL
alpaca data option snapshot --symbol AAPL250620C00200000
alpaca data option latest-quotes --symbol AAPL250620C00200000
```

### Market Data — Other

```bash
alpaca data news --symbol AAPL
alpaca data corporate-actions --symbols AAPL --types dividend
alpaca data forex rates --currency-pairs USD/EUR
alpaca clock                        # Market status and next open/close
alpaca calendar                     # Trading calendar
```

### Watchlists

```bash
alpaca watchlist list
alpaca watchlist create --name "Tech Stocks" --symbols AAPL,MSFT,NVDA
alpaca watchlist get --watchlist-id <id>
alpaca watchlist add --watchlist-id <id> --symbol GOOGL
alpaca watchlist remove --watchlist-id <id> --symbol GOOGL
alpaca watchlist delete --watchlist-id <id>
```

### Assets

```bash
alpaca asset list                   # All tradable assets
alpaca asset get --symbol AAPL      # Asset details
```

### Raw API Access

For endpoints not yet covered by named commands:

```bash
alpaca api GET /v2/account
echo '{"symbol":"AAPL","qty":"1","side":"buy","type":"market","time_in_force":"day"}' \
  | alpaca api POST /v2/orders
```

## Discoverability

```bash
alpaca --help              # Top-level command groups
alpaca --help-all          # Full command tree with all flags
alpaca order submit --help # Per-command flags and descriptions
alpaca order list --schema # Response schema without calling the API
```

## Using with AI Agents

The CLI is designed for AI agent integration. Key features for agents:

* **No confirmation prompts**: Commands execute immediately. No interactive "are you sure?" dialogs.
* **Structured JSON errors** on stderr with exit codes (`0` success, `1` error, `2` auth failure)
* **Automatic retry** on 429/5xx (max 3 retries, respects `Retry-After`)
* **`--dry-run`** for order preview without execution
* **`--schema`** to inspect response shapes without making API calls
* **`--quiet`** to suppress non-essential output

### Idempotent Orders

The optional `--client-order-id` flag lets you assign a unique identifier to an order (up to 128 characters). If omitted, Alpaca generates one automatically.

When provided, the API rejects duplicate submissions with the same `client_order_id`, preventing accidental double-orders in retry logic.

```bash
# Generate a client-assigned UUID that you'll use for this order
CLIENT_ORDER_ID="$(uuidgen)"

# Submit with a client-assigned UUID
alpaca order submit --symbol AAPL --side buy --qty 10 --type market \
  --client-order-id "$CLIENT_ORDER_ID"

# Retrieve the order later by that ID
alpaca order get-by-client-id --client-order-id "$CLIENT_ORDER_ID"
```

### Whitelisting in MCP Clients

When using the CLI from an AI agent in Cursor or Claude, you can whitelist CLI commands to skip confirmation prompts. Note that this removes a safety layer: an agent with whitelisted order commands can trade without human confirmation.

## How the CLI Differs from the MCP Server

Both tools access the same Alpaca APIs, but they serve different use cases:

| Aspect         | CLI                                      | MCP Server                                       |
| :------------- | :--------------------------------------- | :----------------------------------------------- |
| Invocation     | One command per call, then exits         | Background process for an entire session         |
| Context cost   | Minimal, just the command string         | Full tool schemas in the context window          |
| Output         | Pipes into scripts, files, other tools   | Returns through MCP to the AI model              |
| AI host needed | No, works in any terminal                | Yes, requires an MCP client                      |
| Best for       | Scripts, cron, CI, focused agent actions | Long-lived AI sessions, multi-tool orchestration |

## Self-Update

```bash
alpaca update              # Check for updates and prompt to upgrade
alpaca update --yes        # Non-interactive upgrade
alpaca update --check      # Check without upgrading
```

## Shell Completions

```bash
alpaca completion bash     # Bash completions
alpaca completion zsh      # Zsh completions
alpaca completion fish     # Fish completions
alpaca completion powershell # PowerShell completions
```

Follow the output instructions to install completions for your shell.

## Important Considerations

* **Paper trading is the default**: Live trading requires explicit opt-in via `--live` flag or `ALPACA_LIVE_TRADE=true`. Scripts that forget to opt in will hit paper, not live.
* **No confirmation prompts**: Commands like `alpaca order cancel-all` and `alpaca position close-all` execute immediately without asking for confirmation.
* **API key security**: Keep your API keys secure and never share them. Treat them like passwords.
* **Order execution risk**: Orders execute directly against Alpaca's Trading API. Review orders before submitting, as unintended orders can result in real financial loss.
* **Rate limits**: Alpaca's API has rate limits per account. High-frequency querying may trigger rate limiting.

## Resources

* [GitHub Repository](https://github.com/alpacahq/cli)
* [CLI Launch Blog Post](https://alpaca.markets/blog/alpaca-introduces-cli-for-trading-api/)
* [Alpaca MCP Server](/us/docs/alpaca-mcp-server)
* [Alpaca Support](mailto:support@alpaca.markets)

## Disclosure

*Insights generated by our CLI, MCP server, and connected AI agents are for educational and informational purposes only and should not be taken as investment advice. Alpaca does not recommend any specific securities or investment strategies. Past performance from models does not guarantee future results. Please conduct your own due diligence before making any decisions.*