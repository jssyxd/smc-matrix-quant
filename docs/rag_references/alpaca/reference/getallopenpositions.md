# All Open Positions

Source: https://docs.alpaca.markets/us/reference/getallopenpositions.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# All Open Positions

The positions API provides information about an account's current open positions. The response will include information such as cost basis, shares traded, and market value, which will be updated live as price information is updated. Once a position is closed, it will no longer be queryable through this API

Retrieves a list of the account's open positions

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AssetClass": {
        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, \"crypto\" for cryptocurrencies, and \"ipo\" for IPO indications of interest/orders. This `asset_class: ipo` value is distinct from the assets API `attributes: [\"ipo\"]` flag.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto",
          "crypto_perp",
          "treasury",
          "corporate",
          "global_equity",
          "us_index",
          "us_equity_chain",
          "ipo"
        ],
        "example": "us_equity",
        "examples": [
          "us_equity"
        ],
        "title": "AssetClass",
        "type": "string"
      },
      "ExchangeForPosition": {
        "description": "Represents the current exchanges Alpaca supports. List is currently:\n\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC\n- CRYPTO\n\nCan be empty if not applicable (e.g., for options contracts)",
        "enum": [
          "AMEX",
          "ARCA",
          "BATS",
          "NYSE",
          "NASDAQ",
          "NYSEARCA",
          "OTC",
          "CRYPTO",
          ""
        ],
        "example": "NYSE",
        "title": "Exchange",
        "type": "string"
      },
      "Position": {
        "description": "The positions API provides information about an account's current open positions. The response will include information such as cost basis, shares traded, and market value, which will be updated live as price information is updated. Once a position is closed, it will no longer be queryable through this API.",
        "examples": [
          {
            "asset_class": "us_equity",
            "asset_id": "904837e3-3b76-47ec-b432-046db621571b",
            "asset_marginable": true,
            "avg_entry_price": "100.0",
            "change_today": "0.0084",
            "cost_basis": "500.0",
            "current_price": "120.0",
            "exchange": "NASDAQ",
            "lastday_price": "119.0",
            "market_value": "600.0",
            "qty": "5",
            "qty_available": "4",
            "side": "long",
            "symbol": "AAPL",
            "unrealized_intraday_pl": "10.0",
            "unrealized_intraday_plpc": "0.0084",
            "unrealized_pl": "100.0",
            "unrealized_plpc": "0.20"
          },
          {
            "asset_class": "us_equity",
            "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "asset_marginable": false,
            "avg_entry_price": "174.78",
            "change_today": "-0.0018326556325525",
            "cost_basis": "349.56",
            "current_price": "174.29",
            "exchange": "NASDAQ",
            "lastday_price": "174.61",
            "market_value": "348.58",
            "qty": "2",
            "qty_available": "2",
            "side": "long",
            "symbol": "AAPL",
            "unrealized_intraday_pl": "-0.98",
            "unrealized_intraday_plpc": "-0.0028035244307129",
            "unrealized_pl": "-0.98",
            "unrealized_plpc": "-0.0028035244307129"
          }
        ],
        "properties": {
          "asset_class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "asset_id": {
            "description": "Asset ID (For options this represents the option contract ID)",
            "format": "uuid",
            "type": "string"
          },
          "asset_marginable": {
            "type": "boolean"
          },
          "avg_entry_price": {
            "description": "Average entry price of the position",
            "minLength": 1,
            "type": "string"
          },
          "avg_entry_swap_rate": {
            "description": "The weighted-average exchange rate at the time the position was entered.",
            "format": "decimal",
            "type": "string"
          },
          "change_today": {
            "description": "Percent change from last day price (by a factor of 1)",
            "minLength": 1,
            "type": "string"
          },
          "cost_basis": {
            "description": "Total cost basis in dollar",
            "minLength": 1,
            "type": "string"
          },
          "current_price": {
            "description": "Current asset price per share",
            "minLength": 1,
            "type": "string"
          },
          "exchange": {
            "$ref": "#/components/schemas/ExchangeForPosition"
          },
          "lastday_price": {
            "description": "Last day's asset price per share based on the closing value of the last trading day",
            "minLength": 1,
            "type": "string"
          },
          "market_value": {
            "description": "Total dollar amount of the position",
            "minLength": 1,
            "type": "string"
          },
          "prev_swap_rate": {
            "description": "The exchange rate as of the previous close (i.e. yesterday's rate)",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "The number of shares",
            "minLength": 1,
            "type": "string"
          },
          "qty_available": {
            "description": "Total number of shares available minus open orders / locked for options covered call",
            "minLength": 1,
            "type": "string"
          },
          "side": {
            "description": "long",
            "enum": [
              "long",
              "short"
            ],
            "type": "string"
          },
          "swap_rate": {
            "description": "The current exchange rate (without mark-up) used to convert local-currency position values into USD. Present only for LCT (Local Currency Trading) accounts",
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol name of the asset",
            "example": "AAPL",
            "type": "string"
          },
          "unrealized_intraday_pl": {
            "description": "Unrealized profit/loss in dollars for the day",
            "minLength": 1,
            "type": "string"
          },
          "unrealized_intraday_plpc": {
            "description": "Unrealized profit/loss percent (by a factor of 1)",
            "minLength": 1,
            "type": "string"
          },
          "unrealized_pl": {
            "description": "Unrealized profit/loss in dollars",
            "minLength": 1,
            "type": "string"
          },
          "unrealized_plpc": {
            "description": "Unrealized profit/loss percent (by a factor of 1)",
            "minLength": 1,
            "type": "string"
          },
          "usd": {
            "$ref": "#/components/schemas/USDPositionValues"
          }
        },
        "required": [
          "asset_id",
          "symbol",
          "exchange",
          "asset_class",
          "avg_entry_price",
          "qty",
          "side",
          "market_value",
          "cost_basis",
          "unrealized_pl",
          "unrealized_plpc",
          "unrealized_intraday_pl",
          "unrealized_intraday_plpc",
          "current_price",
          "lastday_price",
          "change_today",
          "asset_marginable"
        ],
        "title": "Position",
        "type": "object"
      },
      "USDPositionValues": {
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
            "description": "Unrealized intraday profit/loss percent (by a factor of 1)",
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
        "required": [
          "avg_entry_price",
          "cost_basis"
        ],
        "title": "USDPositionValues",
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
    "/v2/positions": {
      "get": {
        "description": "The positions API provides information about an account's current open positions. The response will include information such as cost basis, shares traded, and market value, which will be updated live as price information is updated. Once a position is closed, it will no longer be queryable through this API\n\nRetrieves a list of the account's open positions",
        "operationId": "getAllOpenPositions",
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
            "description": "Successful response"
          }
        },
        "summary": "All Open Positions",
        "tags": [
          "Positions"
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
      "name": "Positions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```