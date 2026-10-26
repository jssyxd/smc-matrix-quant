# Retrieve real-time Trading Limits for an Account

Source: https://docs.alpaca.markets/us/reference/get-v1-account-trading-limits.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve real-time Trading Limits for an Account

This endpoint is only available to accounts with the trading limits feature enabled, and not on JIT.
The daily trading limit is set at the correspondent level (or the account level) and is used as the limit for the total amount due to Alpaca on the date of settlement.
The limit in use returns the real time usage of this limit, based on the setup it uses the usage is calculated differently.
If the limit in use reaches the `daily_net_limit` or `available` is zero, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AccountTradingLimit": {
        "properties": {
          "available": {
            "description": "The remaining net buying limit that can be used for trading.",
            "format": "decimal",
            "type": "string"
          },
          "daily_net_limit": {
            "description": "The net buying limit that can be reached before further trading activity is restricted. Please reach out to learn more about how this limit is determined.",
            "format": "decimal",
            "type": "string"
          },
          "held": {
            "description": "The limit that is currently being held for open orders",
            "format": "decimal",
            "type": "string"
          },
          "swap_rate": {
            "description": "The swap rate is applicable for Local Currency Trading (LCT) accounts",
            "format": "decimal",
            "type": "string"
          },
          "usd": {
            "$ref": "#/components/schemas/USDAccountTradingLimit"
          },
          "used": {
            "description": "The real time net value of cash inflows (buy trades, etc.) with cash outflows (sell trades, etc). This will be dynamic throughout the day based on user activity, with executed orders being reset at the start of the next trading day.",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "AccountTradingLimit",
        "type": "object"
      },
      "USDAccountTradingLimit": {
        "properties": {
          "available": {
            "description": "The remaining net buying limit that can be used for trading.",
            "format": "decimal",
            "type": "string"
          },
          "daily_net_limit": {
            "description": "The net buying limit that can be reached before further trading activity is restricted. Please reach out to learn more about how this limit is determined.",
            "format": "decimal",
            "type": "string"
          },
          "held": {
            "description": "The limit that is currently being held for open orders",
            "format": "decimal",
            "type": "string"
          },
          "used": {
            "description": "The real time net value of cash inflows (buy trades, etc.) with cash outflows (sell trades, etc). This will be dynamic throughout the day based on user activity, with executed orders being reset at the start of the next trading day.",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "USDAccountTradingLimit",
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
    "/v1/trading/accounts/{account_id}/limits": {
      "get": {
        "description": "This endpoint is only available to accounts with the trading limits feature enabled, and not on JIT.\nThe daily trading limit is set at the correspondent level (or the account level) and is used as the limit for the total amount due to Alpaca on the date of settlement.\nThe limit in use returns the real time usage of this limit, based on the setup it uses the usage is calculated differently.\nIf the limit in use reaches the `daily_net_limit` or `available` is zero, further purchasing activity will be halted, however, the limit can be adjusted by reaching out to Alpaca with the proposed new limit and the reason for the change.",
        "operationId": "get-v1-account-trading-limits",
        "parameters": [
          {
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AccountTradingLimit"
                }
              }
            },
            "description": "Returns the trading limit set for the account and the real-time usage of the limit"
          },
          "404": {
            "description": "Returned when the account is not configured for trading limits"
          }
        },
        "summary": "Retrieve real-time Trading Limits for an Account",
        "tags": [
          "Trading"
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
      "name": "Trading"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```