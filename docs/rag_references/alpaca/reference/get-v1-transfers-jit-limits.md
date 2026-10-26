# Retrieve Daily Trading Limits

Source: https://docs.alpaca.markets/us/reference/get-v1-transfers-jit-limits.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Daily Trading Limits

The JIT Securities daily trading limit is set at the correspondent level and is used as the limit for the total amount due to Alpaca on the date of settlement. The limit in use returns the real time usage of this limit and is calculated by taking the net of trade and non-trade activity inflows and outflows. If the limit in use reaches the daily net limit, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change. The limit is reset at the start of every trading day at 8.00 PM ET

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "DailyTradingLimit": {
        "description": "Correspondent-level daily net buying limit and the real-time amount currently consuming it.",
        "properties": {
          "cash_held": {
            "description": "Cash reserved for open cash-secured put positions. Only present in the response when the correspondent has at least one open cash-secured put; the field is omitted from the response otherwise (including for options-enabled correspondents with no open cash-secured puts).",
            "example": "20000",
            "format": "decimal",
            "type": "string"
          },
          "correspondent": {
            "description": "The correspondent code the limits apply to.",
            "example": "EXMP",
            "type": "string"
          },
          "daily_net_limit": {
            "description": "The daily net buying limit for the correspondent; further buying is halted once the in_use_limit limit reaches this value.",
            "example": "1000000",
            "format": "decimal",
            "type": "string"
          },
          "executed_buys": {
            "description": "Cumulative cash value of executed buy activity contributing to the in-use limit since the last reset.",
            "example": "55",
            "format": "decimal",
            "type": "string"
          },
          "executed_sells": {
            "description": "Cumulative cash value of executed sell activity offsetting the in-use limit since the last reset.",
            "example": "0",
            "format": "decimal",
            "type": "string"
          },
          "in_use_limit": {
            "description": "Real-time net amount currently consuming the daily limit. Equal to `executed_buys` − `executed_sells` + `open_buys` − `open_sells` (+ `cash_held` when a cash-secured put is open). Resets at the start of the next trading day at 8.00 PM ET.",
            "example": "55",
            "format": "decimal",
            "type": "string"
          },
          "open_buys": {
            "description": "Reserved cash value of currently open buy orders (limit price for limit orders, notional or estimated mid for market orders) contributing to the in-use limit.",
            "example": "0",
            "format": "decimal",
            "type": "string"
          },
          "open_sells": {
            "description": "Reserved cash value of currently open sell orders offsetting the in-use limit.",
            "example": "0",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "DailyTradingLimit",
        "type": "object"
      }
    },
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
    "/v1/transfers/jit/limits": {
      "get": {
        "description": "The JIT Securities daily trading limit is set at the correspondent level and is used as the limit for the total amount due to Alpaca on the date of settlement. The limit in use returns the real time usage of this limit and is calculated by taking the net of trade and non-trade activity inflows and outflows. If the limit in use reaches the daily net limit, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change. The limit is reset at the start of every trading day at 8.00 PM ET",
        "operationId": "get-v1-transfers-jit-limits",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "open_cash_secured_put": {
                    "summary": "Correspondent with an open cash-secured put (cash_held present)",
                    "value": {
                      "cash_held": "20000",
                      "correspondent": "EXMP",
                      "daily_net_limit": "1000000",
                      "executed_buys": "43140",
                      "executed_sells": "0",
                      "in_use_limit": "103140",
                      "open_buys": "40000",
                      "open_sells": "0"
                    }
                  },
                  "us_equity": {
                    "summary": "US equity correspondent with open and executed activity",
                    "value": {
                      "correspondent": "EXMP",
                      "daily_net_limit": "1000000",
                      "executed_buys": "55",
                      "executed_sells": "0",
                      "in_use_limit": "55",
                      "open_buys": "0",
                      "open_sells": "0"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/DailyTradingLimit"
                }
              }
            },
            "description": "Returns the JIT Securities Daily Trading Limit Object based off of real time calculations."
          }
        },
        "summary": "Retrieve Daily Trading Limits",
        "tags": [
          "Funding"
        ]
      }
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```