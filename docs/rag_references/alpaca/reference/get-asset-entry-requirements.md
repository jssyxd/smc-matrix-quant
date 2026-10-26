# Retrieve Entry Requirements for requested assets

Source: https://docs.alpaca.markets/us/reference/get-asset-entry-requirements.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Entry Requirements for requested assets

Returns all entry-requirements

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AssetEntryRequirements": {
        "description": "Defines the necessary conditions that must be met to initiate a position for a specific asset",
        "properties": {
          "regt_long": {
            "description": "The percentage of the asset's market value required as Reg T (2x) buying power to open a long position",
            "example": "0.5",
            "format": "decimal",
            "type": "string"
          },
          "regt_short": {
            "description": "The percentage of the asset's market value required as Reg T (2x) buying power to open a short position",
            "example": "0.5",
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol (or asset id) of the requested asset",
            "example": "AAPL",
            "type": "string"
          }
        },
        "required": [
          "symbol"
        ],
        "title": "AssetEntryRequirements",
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
    "/v1/assets/entry-requirements": {
      "get": {
        "description": "Returns all entry-requirements",
        "operationId": "get-asset-entry-requirements",
        "parameters": [
          {
            "description": "Comma-separated symbols or asset ids. The symbols (or asset ids) for which asset entry requirements are to be requested. Maximum number of symbols allowed is 500.",
            "example": "AAPL,SPY",
            "in": "query",
            "name": "symbols",
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
                  "items": {
                    "$ref": "#/components/schemas/AssetEntryRequirements"
                  },
                  "type": "array"
                }
              }
            },
            "description": "An array of asset entry requirement objects."
          }
        },
        "summary": "Retrieve Entry Requirements for requested assets",
        "tags": [
          "Assets"
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
      "name": "Assets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```