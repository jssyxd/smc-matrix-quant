# Retrieve Aggregate Positions

Source: https://docs.alpaca.markets/us/reference/get-v1-reporting-eod-aggregate_positions.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Aggregate Positions

This API endpoint provides reporting data to partners for aggregate common stock and crypto positions across their account base. Partners can view historical snapshots of their holding across their entire account base. Please note that this API utilizes an 8:00 pm (EST) cutoff which aligns with the end of the Securities extended hours trading session as well as Alpaca's 24 hour Crypto trading window. Additionally, the endpoint supports indexing to help the partner efficiently filter by key information including date and symbol while being able to include or remove firm accounts.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AggregatePositionResponse": {
        "examples": [
          {
            "asset_type": "us_equity",
            "closing_price": "148.4700",
            "cusip": "037833100",
            "long_market_value": "148.4700",
            "long_qty": "1",
            "num_accounts": 1,
            "short_market_value": "0",
            "short_qty": "0",
            "symbol": "AAPL"
          }
        ],
        "properties": {
          "asset_type": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "closing_price": {
            "description": "EOD asset price per share at session close",
            "format": "decimal",
            "type": "string"
          },
          "cusip": {
            "description": "Cusip (9 digits, can start with 0's)",
            "format": "decimal",
            "type": "string"
          },
          "long_market_value": {
            "description": "Aggregate notional dollar amount of the partner's long positions",
            "format": "decimal",
            "type": "string"
          },
          "long_qty": {
            "description": "Aggregate number of shares that the partner is long",
            "format": "decimal",
            "type": "string"
          },
          "num_accounts": {
            "description": "Number of accounts that have a position in this asset (either long or short)",
            "format": "decimal",
            "type": "integer"
          },
          "short_market_value": {
            "description": "Aggregate notional dollar amount of the partner's short positions",
            "format": "decimal",
            "type": "string"
          },
          "short_qty": {
            "description": "Aggregate number of shares that the partner is short",
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol of asset",
            "type": "string"
          }
        },
        "title": "",
        "type": "object"
      },
      "AssetClass": {
        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, \"crypto\" for cryptocurrencies, and \"ipo\" for IPO indications of interest. This `asset_class: ipo` value is distinct from the assets API `attributes: [\"ipo\"]` flag.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto",
          "ipo"
        ],
        "type": "string"
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
    "/v1/reporting/eod/aggregate_positions": {
      "get": {
        "description": "This API endpoint provides reporting data to partners for aggregate common stock and crypto positions across their account base. Partners can view historical snapshots of their holding across their entire account base. Please note that this API utilizes an 8:00 pm (EST) cutoff which aligns with the end of the Securities extended hours trading session as well as Alpaca's 24 hour Crypto trading window. Additionally, the endpoint supports indexing to help the partner efficiently filter by key information including date and symbol while being able to include or remove firm accounts.",
        "operationId": "get-v1-reporting-eod-aggregate_positions",
        "parameters": [
          {
            "description": "\"YYYY-MM-DD\" format",
            "in": "query",
            "name": "date",
            "required": true,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Comma-separated symbols. If populated, then only the specified symbols will be returned. If null, then all symbols will be included in the response.",
            "in": "query",
            "name": "symbols",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Defaults to True which includes firm accounts. Passing False will exclude all firm accounts.",
            "in": "query",
            "name": "firm_accounts",
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
                  "items": {
                    "$ref": "#/components/schemas/AggregatePositionResponse"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Array of objects, each object pertains to the date specified in the request and a unique asset. See parameters below. Notes: Returns an empty array for non-trading days, assets with no positions are omitted."
          }
        },
        "summary": "Retrieve Aggregate Positions",
        "tags": [
          "Reporting"
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
      "name": "Reporting"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```