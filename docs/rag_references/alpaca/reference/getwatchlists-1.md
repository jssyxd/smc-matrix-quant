# Get All Watchlists

Source: https://docs.alpaca.markets/us/reference/getwatchlists-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get All Watchlists

Returns the list of watchlists registered under the account.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "WatchlistWithoutAsset": {
        "description": "The watchlist API provides CRUD operation for the account's watchlist. An account can have multiple watchlists and each is uniquely identified by id but can also be addressed by user-defined name.\n",
        "examples": [
          {
            "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
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
    "/v2/watchlists": {
      "get": {
        "description": "Returns the list of watchlists registered under the account.",
        "operationId": "getWatchlists",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "example-1": {
                    "value": [
                      {
                        "account_id": "abe25343-a7ba-4255-bdeb-f7e013e9ee5d",
                        "created_at": "2022-01-31T21:49:05.14628Z",
                        "id": "3174d6df-7726-44b4-a5bd-7fda5ae6e009",
                        "name": "Primary Watchlist",
                        "updated_at": "2022-01-31T21:49:05.14628Z"
                      }
                    ]
                  }
                },
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/WatchlistWithoutAsset"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Successful response"
          }
        },
        "summary": "Get All Watchlists",
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