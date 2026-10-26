# List Open Positions for an Account

Source: https://docs.alpaca.markets/us/reference/getpositionsforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List Open Positions for an Account

List open positions for an account

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
    "schemas": {
      "AssetClass": {
        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, \"crypto\" for cryptocurrencies, and \"ipo\" for IPO indications of interest. This `asset_class: ipo` value is distinct from the assets API `attributes: [\"ipo\"]` flag.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto",
          "ipo"
        ],
        "type": "string"
      },
      "Position": {
        "examples": [
          {
            "asset_class": "us_equity",
            "asset_id": "93f58d0b-6c53-432d-b8ce-2bad264dbd94",
            "asset_marginable": false,
            "avg_entry_price": "172.08",
            "change_today": "0.0189483657034581",
            "cost_basis": "688.32",
            "current_price": "172.08",
            "exchange": "NASDAQ",
            "lastday_price": "168.88",
            "market_value": "688.32",
            "qty": "4",
            "qty_available": "4",
            "side": "long",
            "symbol": "AAPL",
            "unrealized_intraday_pl": "0",
            "unrealized_intraday_plpc": "0",
            "unrealized_pl": "0",
            "unrealized_plpc": "0"
          }
        ],
        "properties": {
          "asset_class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "asset_id": {
            "description": "Asset ID (For options this represents the option contract ID)",
            "example": "904837e3-3b76-47ec-b432-046db621571b",
            "format": "uuid",
            "type": "string"
          },
          "asset_marginable": {
            "description": "Indicates if this asset is marginable",
            "type": "boolean"
          },
          "avg_entry_price": {
            "description": "Average entry price of the position",
            "example": "100.0",
            "type": "string"
          },
          "avg_entry_swap_rate": {
            "description": "The average swap rate of the position. This is only returned for LCT accounts.",
            "example": "1.40",
            "format": "decimal",
            "type": "string"
          },
          "change_today": {
            "description": "Percent change from last day price (by a factor of 1)",
            "example": "0.0084",
            "format": "decimal",
            "type": "string"
          },
          "cost_basis": {
            "description": "Total cost basis",
            "example": "500.0",
            "format": "decimal",
            "type": "string"
          },
          "current_price": {
            "description": "Current asset price per share",
            "example": "120.0",
            "format": "decimal",
            "type": "string"
          },
          "exchange": {
            "description": "Exchange name of the asset",
            "example": "NASDAQ",
            "type": "string"
          },
          "lastday_price": {
            "description": "Last day's asset price per share based on the closing value of the last trading day",
            "example": "119.0",
            "format": "decimal",
            "type": "string"
          },
          "market_value": {
            "description": "Total market value of the position",
            "example": "600.0",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "The number of shares",
            "example": "5",
            "type": "string"
          },
          "qty_available": {
            "description": "Total number of shares available minus open orders / locked for options covered call",
            "example": "5",
            "type": "string"
          },
          "side": {
            "enum": [
              "long",
              "short"
            ],
            "example": "long",
            "type": "string"
          },
          "swap_rate": {
            "description": "The latest swap rate. This is only returned for LCT accounts.",
            "example": "1.50",
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "Asset symbol",
            "example": "AAPL",
            "type": "string"
          },
          "unrealized_intraday_pl": {
            "description": "Unrealized profit/loss for the day",
            "example": "10.0",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_intraday_plpc": {
            "description": "Unrealized interday profit/loss percent (by a factor of 1)",
            "example": "0.0084",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_pl": {
            "description": "Unrealized profit/loss",
            "example": "100.0",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_plpc": {
            "description": "Unrealized profit/loss percent (by a factor of 1)",
            "example": "0.20",
            "format": "decimal",
            "type": "string"
          },
          "usd": {
            "$ref": "#/components/schemas/USDPosition"
          }
        },
        "required": [
          "asset_id",
          "symbol",
          "exchange",
          "asset_class",
          "avg_entry_price",
          "qty",
          "qty_available",
          "side",
          "market_value",
          "cost_basis",
          "unrealized_pl",
          "unrealized_plpc",
          "unrealized_intraday_pl",
          "unrealized_intraday_plpc",
          "current_price",
          "lastday_price",
          "change_today"
        ],
        "type": "object"
      },
      "USDPosition": {
        "description": "Position values in USD. This is returned for LCT (non-USD) accounts only.",
        "properties": {
          "avg_entry_price": {
            "description": "Average entry price of the position in USD",
            "example": "71.43",
            "format": "decimal",
            "type": "string"
          },
          "change_today": {
            "description": "Percent change from last day price (by a factor of 1)",
            "example": "0.67",
            "format": "decimal",
            "type": "string"
          },
          "cost_basis": {
            "description": "Total cost basis in USD",
            "example": "333.33",
            "format": "decimal",
            "type": "string"
          },
          "current_price": {
            "description": "Current asset price per share in USD",
            "example": "80.0",
            "format": "decimal",
            "type": "string"
          },
          "lastday_price": {
            "description": "Last day's asset price per share based on the closing value of the last trading day in USD",
            "example": "79.33",
            "format": "decimal",
            "type": "string"
          },
          "market_value": {
            "description": "Total market value of the position in USD",
            "example": "400.00",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_intraday_pl": {
            "description": "Unrealized profit/loss in USD for the day",
            "example": "6.67",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_intraday_plpc": {
            "description": "Unrealized interday profit/loss percent (by a factor of 1)",
            "example": "0.0084",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_pl": {
            "description": "Unrealized profit/loss in USD",
            "example": "66.67",
            "format": "decimal",
            "type": "string"
          },
          "unrealized_plpc": {
            "description": "Unrealized profit/loss percent (by a factor of 1)",
            "example": "0.2",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "USDPosition",
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
    "/v1/trading/accounts/{account_id}/positions": {
      "get": {
        "description": "List open positions for an account",
        "operationId": "getPositionsForAccount",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Position"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Success"
          }
        },
        "summary": "List Open Positions for an Account",
        "tags": [
          "Trading"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
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
      "name": "Trading"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```