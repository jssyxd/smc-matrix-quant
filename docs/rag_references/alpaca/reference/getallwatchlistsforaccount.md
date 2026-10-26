# Retrieve all Watchlists for an Account

Source: https://docs.alpaca.markets/us/reference/getallwatchlistsforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve all Watchlists for an Account

Fetch a list of all watchlists currently in an account.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "WatchlistWithoutAsset": {
        "description": "Represents a set of securities observed by a user.",
        "properties": {
          "account_id": {
            "description": "Unique identifier of the account that owns this watchlist.\n",
            "format": "uuid",
            "type": "string"
          },
          "created_at": {
            "description": "When watchlist was created",
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "Unique identifier of the watchlist itself.\n",
            "format": "uuid",
            "type": "string"
          },
          "name": {
            "description": "User friendly Name of watchlist",
            "pattern": "^[a-zA-Z0-9]+$",
            "type": "string"
          },
          "updated_at": {
            "description": "When watchlist was last updated",
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
    "/v1/trading/accounts/{account_id}/watchlists": {
      "get": {
        "description": "Fetch a list of all watchlists currently in an account.",
        "operationId": "getAllWatchlistsForAccount",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/WatchlistWithoutAsset"
                  },
                  "type": "array"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve all Watchlists for an Account",
        "tags": [
          "Watchlist"
        ]
      },
      "parameters": [
        {
          "description": "Unique identifier of an account.",
          "in": "path",
          "name": "account_id",
          "required": true,
          "schema": {
            "format": "uuid",
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