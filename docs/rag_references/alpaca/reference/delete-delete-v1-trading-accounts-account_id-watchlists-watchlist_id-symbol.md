# Remove a Symbol from a Watchlist

Source: https://docs.alpaca.markets/us/reference/delete-delete-v1-trading-accounts-account_id-watchlists-watchlist_id-symbol.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Remove a Symbol from a Watchlist

Delete one entry for an asset by symbol name

# OpenAPI definition

```json
{
  "components": {
    "securitySchemes": {
      "BasicAuth": {
        "scheme": "basic",
        "type": "http"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Open brokerage accounts, enable stock, options and crypto trading. Manage the ongoing user experience and brokerage customer lifecycle with the Alpaca Broker API",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Broker API",
    "version": "1.1.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v1/trading/accounts/{account_id}/watchlists/{watchlist_id}/{symbol}": {
      "delete": {
        "description": "Delete one entry for an asset by symbol name",
        "operationId": "delete-DELETE-v1-trading-accounts-account_id-watchlists-watchlist_id-symbol",
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "The requested watchlist is not found"
          }
        },
        "summary": "Remove a Symbol from a Watchlist",
        "tags": [
          "Watchlist"
        ]
      },
      "parameters": [
        {
          "description": "Account identifier.",
          "in": "path",
          "name": "account_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        },
        {
          "description": "The Watchlist ID",
          "in": "path",
          "name": "watchlist_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        },
        {
          "description": "The symbol ",
          "in": "path",
          "name": "symbol",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ]
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ],
  "servers": [
    {
      "description": "Sandbox endpoint",
      "url": "https://broker-api.sandbox.alpaca.markets"
    },
    {
      "description": "Production endpoint",
      "url": "https://broker-api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Watchlist"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```