# Get Account Configurations

Source: https://docs.alpaca.markets/us/reference/getaccountconfig-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Account Configurations

gets the current account configuration values

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AccountConfigurations": {
        "description": "The account configuration API provides custom configurations about your trading account settings. These configurations control various allow you to modify settings to suit your trading needs.",
        "examples": [
          {
            "disable_overnight_trading": false,
            "fractional_trading": true,
            "max_margin_multiplier": "4",
            "no_shorting": false,
            "suspend_trade": false,
            "trade_confirm_email": "all"
          }
        ],
        "properties": {
          "disable_overnight_trading": {
            "description": "If true, overnight trading is disabled.",
            "type": "boolean"
          },
          "fractional_trading": {
            "description": "If true, account is able to participate in fractional trading",
            "type": "boolean"
          },
          "max_margin_multiplier": {
            "description": "Can be \"1\", \"2\", or \"4\"",
            "type": "string"
          },
          "max_options_trading_level": {
            "description": "The desired maximum options trading level. 0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "type": "integer"
          },
          "no_shorting": {
            "description": "If true, account becomes long-only mode.",
            "type": "boolean"
          },
          "ptp_no_exception_entry": {
            "description": "If set to true then Alpaca will accept orders for PTP symbols with no exception. Default is false.",
            "type": "boolean"
          },
          "suspend_trade": {
            "description": "If true, new orders are blocked.",
            "type": "boolean"
          },
          "trade_confirm_email": {
            "description": "all or none. If none, emails for order fills are not sent.",
            "type": "string"
          }
        },
        "title": "AccountConfigurations",
        "type": "object"
      }
    },
    "securitySchemes": {
      "API_Key": {
        "description": "",
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "API_Secret": {
        "description": "",
        "in": "header",
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Trading API",
    "version": "2.0.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v2/account/configurations": {
      "get": {
        "description": "gets the current account configuration values",
        "operationId": "getAccountConfig",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AccountConfigurations"
                }
              }
            },
            "description": "Successful response"
          }
        },
        "summary": "Get Account Configurations",
        "tags": [
          "Account Configurations"
        ]
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "servers": [
    {
      "description": "Paper",
      "url": "https://paper-api.alpaca.markets"
    },
    {
      "description": "Live",
      "url": "https://api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Account Configurations"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```