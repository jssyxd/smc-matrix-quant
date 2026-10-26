# Update Watchlist By Name

Source: https://docs.alpaca.markets/us/reference/updatewatchlistbyname-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Update Watchlist By Name

Update the name and/or content of watchlist

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AssetAttribute": {
        "description": "Unique characteristic of an asset. Supported values:\n- `ptp_no_exception`: Asset is a Publicly Traded Partnership (PTP) without a qualified notice; non-U.S. customers may incur 10% withholding on gross proceeds as per IRS guidance, and are blocked from being purchased by default.\n- `ptp_with_exception`: Users can open positions in these PTPs without general restrictions.\n- `ipo`: Accepting limit orders only before the stock begins trading on the secondary market.\n- `has_options`: The underlying equity has listed options available on the platform. Note: if the equity had inactive/expired contracts in the past, this will still show up.\n- `options_late_close`: Indicates the underlying asset's options contracts close at 4:15pm ET instead of the standard 4:00pm ET.\n- `fractional_eh_enabled`: Indicates the asset accepts fractional orders during extended hours sessions (pre-market, post-market, and overnight if enabled).\n- `overnight_tradable`: Asset is eligible for overnight (24x5) trading in supported venues on the platform.\n- `overnight_halted`: Asset is eligible for overnight trading but is currently halted/blocked for overnight sessions due to risk, corporate action, compliance, or venue constraints.",
        "enum": [
          "ptp_no_exception",
          "ptp_with_exception",
          "ipo",
          "has_options",
          "options_late_close",
          "fractional_eh_enabled",
          "overnight_tradable",
          "overnight_halted"
        ],
        "example": "ptp_no_exception",
        "type": "string"
      },
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
      "Assets": {
        "description": "The assets API serves as the master list of assets available for trade and data consumption from Alpaca. Assets are sorted by asset class, exchange and symbol. Some assets are only available for data consumption via Polygon, and are not tradable with Alpaca. These assets will be marked with the flag tradable=false.\n",
        "examples": [
          {
            "borrow_status": "easy_to_borrow",
            "class": "us_equity",
            "easy_to_borrow": true,
            "exchange": "NASDAQ",
            "fractionable": true,
            "id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "marginable": true,
            "name": "Apple Inc. Common Stock",
            "shortable": true,
            "status": "active",
            "symbol": "AAPL",
            "tradable": true
          }
        ],
        "properties": {
          "attributes": {
            "example": [
              "ptp_no_exception",
              "ipo"
            ],
            "items": {
              "$ref": "#/components/schemas/AssetAttribute"
            },
            "type": "array"
          },
          "borrow_status": {
            "description": "Borrow status for US equity assets. This field is omitted for non-US-equity assets.",
            "enum": [
              "easy_to_borrow",
              "hard_to_borrow"
            ],
            "example": "easy_to_borrow",
            "type": "string"
          },
          "class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "cusip": {
            "description": "The CUSIP identifier for the asset (US Equities only).\nTo request a specific CUSIP, please reach out to Alpaca support.\n",
            "example": "987654321",
            "type": [
              "string",
              "null"
            ]
          },
          "exchange": {
            "$ref": "#/components/schemas/Exchange"
          },
          "fractionable": {
            "description": "Asset is fractionable or not",
            "type": "boolean"
          },
          "id": {
            "description": "Asset ID",
            "format": "uuid",
            "type": "string"
          },
          "maintenance_margin_requirement": {
            "deprecated": true,
            "description": "**deprecated**: Please use margin_requirement_long or margin_requirement_short instead. Note that these fields are of type string.\nShows the margin requirement percentage for the asset (equities only).\n",
            "type": "number"
          },
          "margin_requirement_long": {
            "description": "The margin requirement percentage for the asset's long positions (equities only), encoded as a decimal string.",
            "example": "100",
            "format": "decimal",
            "type": "string"
          },
          "margin_requirement_short": {
            "description": "The margin requirement percentage for the asset's short positions (equities only), encoded as a decimal string.",
            "example": "30",
            "format": "decimal",
            "type": "string"
          },
          "marginable": {
            "description": "Asset is marginable or not",
            "type": "boolean"
          },
          "min_order_size": {
            "description": "Minimum order size. Field available for crypto only.",
            "format": "decimal",
            "type": "string"
          },
          "min_trade_increment": {
            "description": "Amount a trade quantity can be incremented by. Field available for crypto only.",
            "format": "decimal",
            "type": "string"
          },
          "name": {
            "description": "The official name of the asset",
            "minLength": 1,
            "type": "string"
          },
          "price_increment": {
            "description": "Amount the price can be incremented by. Field available for crypto only.",
            "format": "decimal",
            "type": "string"
          },
          "shortable": {
            "description": "Asset is shortable or not",
            "type": "boolean"
          },
          "status": {
            "description": "active or inactive",
            "enum": [
              "active",
              "inactive"
            ],
            "example": "active",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the asset",
            "example": "AAPL",
            "type": "string"
          },
          "tradable": {
            "description": "Asset is tradable on Alpaca or not",
            "type": "boolean"
          }
        },
        "required": [
          "id",
          "class",
          "exchange",
          "symbol",
          "name",
          "status",
          "tradable",
          "marginable",
          "shortable",
          "fractionable"
        ],
        "title": "Assets",
        "type": "object"
      },
      "Exchange": {
        "description": "Represents the current exchanges Alpaca supports. List is currently:\n\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC\n- CRYPTO",
        "enum": [
          "AMEX",
          "ARCA",
          "BATS",
          "NYSE",
          "NASDAQ",
          "NYSEARCA",
          "OTC",
          "CRYPTO"
        ],
        "example": "NYSE",
        "title": "Exchange",
        "type": "string"
      },
      "UpdateWatchlistRequest": {
        "anyOf": [
          {
            "required": [
              "name"
            ]
          },
          {
            "required": [
              "symbols"
            ]
          }
        ],
        "description": "Request format used for updating an existing watchlist with a set of assets and/or a name.",
        "properties": {
          "name": {
            "description": "The new watchlist name.",
            "type": "string"
          },
          "symbols": {
            "description": "List of asset symbols to include in the watchlist. The existing assets will be replaced with the new list.",
            "items": {
              "type": [
                "string",
                "null"
              ]
            },
            "type": "array"
          }
        },
        "title": "PutWatchlistRequest",
        "type": "object"
      },
      "Watchlist": {
        "description": "The watchlist API provides CRUD operation for the account's watchlist. An account can have multiple watchlists and each is uniquely identified by id but can also be addressed by user-defined name. Each watchlist is an ordered list of assets.\n",
        "examples": [
          {
            "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
            "assets": [
              {
                "class": "us_equity",
                "easy_to_borrow": true,
                "exchange": "NASDAQ",
                "fractionable": true,
                "id": "8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
                "marginable": true,
                "name": "Tesla, Inc. Common Stock",
                "shortable": true,
                "status": "active",
                "symbol": "TSLA",
                "tradable": true
              }
            ],
            "created_at": "2022-01-31T21:49:05.14628Z",
            "id": "3174d6df-7726-44b4-a5bd-7fda5ae6e009",
            "name": "Primary Watchlist",
            "updated_at": "2022-01-31T21:49:05.14628Z"
          }
        ],
        "properties": {
          "account_id": {
            "description": "account ID",
            "format": "uuid",
            "type": "string"
          },
          "assets": {
            "description": "the content of this watchlist, in the order as registered by the client",
            "items": {
              "$ref": "#/components/schemas/Assets"
            },
            "type": "array"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "watchlist id",
            "format": "uuid",
            "type": "string"
          },
          "name": {
            "description": "user-defined watchlist name (up to 64 characters)",
            "minLength": 1,
            "type": "string"
          },
          "updated_at": {
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "id",
          "account_id",
          "created_at",
          "updated_at",
          "name"
        ],
        "title": "Watchlist",
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
    "/v2/watchlists:by_name": {
      "put": {
        "description": "Update the name and/or content of watchlist",
        "operationId": "updateWatchlistByName",
        "parameters": [
          {
            "description": "name of the watchlist",
            "in": "query",
            "name": "name",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UpdateWatchlistRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Watchlist"
                }
              }
            },
            "description": "Successful response"
          }
        },
        "summary": "Update Watchlist By Name",
        "tags": [
          "Watchlists"
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
      "name": "Watchlists"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```