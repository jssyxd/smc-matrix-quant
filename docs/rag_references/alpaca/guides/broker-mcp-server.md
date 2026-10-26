# Broker MCP Server

Source: https://docs.alpaca.markets/us/docs/broker-mcp-server.md

---
updatedAt: 2026-07-16T09:00:40.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Broker MCP Server

Operate, inspect, and reason over the Alpaca Broker API with AI agents — no local setup, no repo cloning, no partner-run infrastructure.

<br />

<Callout icon="🚧" theme="warn">
  ### Beta

  The Broker API MCP Server is in **beta** and is rolling out to select broker partners. Behavior, available operations, and the consent experience may change as we incorporate partner feedback. During beta, **only Broker Dashboard super users can authorize and use the connection** — see [Who can use it (super users)](#who-can-use-it-super-users).
</Callout>

## What You Can Do

* **Ask questions against Broker API data.** In live, use read operations to look up accounts, inspect account status and profile details, review trading account state, check buying power and cash, list positions, pull portfolio history, review activities, and inspect transfers.
* **Discover the right endpoint and schema.** Built-in OpenAPI discovery lets an assistant search Broker API operations, inspect required parameters, and call endpoints with structured inputs.
* **Get documentation-aware answers.** Curated Alpaca docs and API-reference lookup tools answer integration questions about guides, endpoint behavior, request shapes, response fields, and sample usage.
* **Test full broker workflows in sandbox.** Sandbox exposes read and write operations for account opening, funding, transfers, trading, watchlists, documents, options, rebalancing, journals, instant funding, and IPOs.
* **Create synthetic sandbox accounts quickly.** The `create_sandbox_account` tool generates test accounts with valid defaults and optional KYC or account-status fixture outcomes for demos, QA, and integration testing.

## Who Can Use It (Super Users)

The Broker MCP connects to your firm's Broker API through an OAuth authorization in the Broker Dashboard. Approving that authorization requires the `manage_keys`**&#x20;entitlement**, which today is held only by the **Superuser** role.

Before inviting a teammate to test, confirm whether they can actually authorize the connection within your team.

## Environments

There are two hosted endpoints. Each maps to a distinct correspondent and uses its own OAuth client — sandbox and live credentials are **not** interchangeable. Use **sandbox** to test writes, account creation, orders, and funding.

| Environment | MCP endpoint                                    |
| ----------- | ----------------------------------------------- |
| Sandbox     | `https://broker-api.sandbox.alpaca.markets/mcp` |
| Live        | `https://broker-api.alpaca.markets/mcp`         |

## Setup

Connect from any MCP client that supports remote (OAuth) servers. Every client authorizes through the same OAuth flow: you start the connection, a super user approves the consent request in the Broker Dashboard, and the client is then authorized.

### Cursor

An Alpaca plugin is available for Cursor:

1. Open the command palette: `Cmd + Shift + P` (macOS) / `Ctrl + Shift + P` (Windows/Linux).
2. Type `Open Customize` and select the matching option.
3. Click `Browse Marketplace`.
4. Click `Add Marketplace`, then choose `Import from GitHub` from the dropdown on the right of the search bar.
5. Enter the plugins repository URL: <https://github.com/alpacahq/agentic>

### Claude Code (CLI)

A Claude Code plugin is also available. Add the marketplace:

```shell
claude plugin marketplace add alpacahq/agentic
```

To install the MCP server:

1. Start a new session with `claude`, then run `/plugin`.
2. Open the `Marketplaces` tab and select `alpaca-plugins`.
3. Choose `Browse plugins`, select `alpaca-broker`, and install it.
4. Run `/reload-plugins` to load it.
5. Run `/plugin` again, open the `Installed` tab, and confirm `alpaca-broker` is listed.

To enable the servers, run `/mcp` in the chat. You'll see `plugin:alpaca-broker:alpaca-broker` and `plugin:alpaca-broker:alpaca-broker-sandbox`; selecting either starts its OAuth flow.

### ChatGPT (Web)

1. Go to **Settings → Apps → Advanced Settings** and enable **developer mode**.
2. In the same panel, click **Create App** and fill in the form with the MCP URL (live or sandbox).
3. Click **Connect** and sign in through the OAuth flow.

### VS Code

Add either or both servers in `.vscode/mcp.json`:

```json
{
  "servers": {
    "alpaca-broker-mcp": {
      "type": "http",
      "url": "https://broker-api.alpaca.markets/mcp"
    },
    "alpaca-broker-mcp-sandbox": {
      "type": "http",
      "url": "https://broker-api.sandbox.alpaca.markets/mcp"
    }
  }
}
```

Then open the command palette (`Cmd + Shift + P` / `Ctrl + Shift + P`), run `MCP: List Servers`, select `alpaca-broker-mcp` or `alpaca-broker-mcp-sandbox`, and click `Start Server` to trigger the OAuth flow.

### Verify

After connecting, ask your assistant:

> "Find the account for `user@example.com` and summarize its status, buying power, positions, and recent activity."

If you get an API-backed summary, the server is connected.

## How It Works

Rather than loading thousands of endpoint tools into the model's context, the server uses a **CodeMode** discovery flow. The assistant:

1. `search` — finds the relevant Broker API operation(s) from intent.
2. `get_schema` — inspects required parameters, types, and response shape.
3. `execute` — calls the endpoint with structured inputs (subject to the environment's read/write policy).

This keeps tool selection accurate and reduces context bloat.

## Available Tools

| Group                          | Tools                                                                                                                        | Notes                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Endpoint discovery & execution | `search`, `get_schema`, `execute`                                                                                            | OpenAPI-backed             |
| Documentation & API reference  | `search_alpaca_docs`, `fetch_alpaca_doc`, `search_alpaca_api_specs`, `list_alpaca_api_endpoints`, `get_alpaca_endpoint_docs` | Read-only docs/spec lookup |
| Sandbox utilities              | `create_sandbox_account`                                                                                                     | Sandbox only               |

The server is synced to the public Broker OpenAPI spec from `docs.alpaca.markets`. Streaming and redirect/download operations are excluded because they don't function as request/response tools.

## Example Prompts

Control-plane (operate on accounts):

* "Find the account for `user@example.com` and summarize its status, buying power, positions, and recent activity."
* "Show this account's portfolio history for the last month."
* "Check recent transfers for this account and summarize anything pending or failed."
* "Create a sandbox account that lands in an action-required KYC state for a demo."
* "In sandbox, create a test account and then retrieve its status."

Data-plane (understand the API):

* "Which endpoint should I use to create an ACH relationship, and what fields are required?"
* "Show me the endpoint and required fields to create a Broker API account."
* "What is the minimal curl for creating a sandbox account, based on the docs?"
* "Search for the endpoint that retrieves account documents, inspect the schema, and explain the response."

## Safety & Environment Policy

* **Revoking access.** Authorizations can be reviewed and revoked from the Broker Dashboard (Team Management). Removing a user's role also revokes their access on the next token refresh.
* **API key security.** The connection uses OAuth — never paste API keys or secrets into chat.
* **Review AI-suggested actions.** Where writes are enabled in either environment, confirm any mutating operation before it runs.

## Known Limitations (Beta)

* **IP filters.** If your correspondent has IP filters configured, the hosted MCP connection will not work yet. This is a known limitation we plan to address.
* **Super-user-only authorization.** Broader role-based authorization (mapping consent to existing roles) is planned; today only super users can authorize.
* **Production is read-only**. Allowing write operations is planned in the near-future.

## Resources

* [Broker API documentation](https://docs.alpaca.markets/docs/about-broker-api)
* [Broker API reference](https://docs.alpaca.markets/reference)
* [Alpaca Broker Skills for partner workflows](https://github.com/alpacahq/alpaca-skills)
* [Alpaca Support](https://alpaca.markets/support)

## Disclosure

Insights generated by our MCP server and connected AI agents are for educational and informational purposes only and should not be taken as investment advice. Please conduct your own due diligence and review any AI-suggested actions before confirming them.