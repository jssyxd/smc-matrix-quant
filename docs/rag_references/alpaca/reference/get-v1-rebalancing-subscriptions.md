# List All Subscriptions

Source: https://docs.alpaca.markets/us/reference/get-v1-rebalancing-subscriptions.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List All Subscriptions

Lists subscriptions

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "NextPageToken": {
        "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
        "example": "MTAwMA==",
        "type": [
          "string",
          "null"
        ]
      },
      "PortfolioSubscription": {
        "properties": {
          "account_id": {
            "description": "Account ID subscribing to portfolio",
            "type": "string"
          },
          "created_at": {
            "description": "Subscription creation timestamp",
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "Subscription ID",
            "type": "string"
          },
          "last_rebalanced_at": {
            "description": "Last rebalancing event for this subscription. Can be null.",
            "type": "string"
          },
          "portfolio_id": {
            "description": "Portfolio ID for subscription",
            "type": "string"
          }
        },
        "title": "PortfolioSubscription",
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
    "/v1/rebalancing/subscriptions": {
      "get": {
        "description": "Lists subscriptions",
        "operationId": "get-v1-rebalancing-subscriptions",
        "parameters": [
          {
            "description": "Any subscriptions for this account_id will be returned",
            "in": "query",
            "name": "account_id",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Portfolio ID",
            "in": "query",
            "name": "portfolio_id",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Pagination token",
            "in": "query",
            "name": "page_token",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Max number of subscriptions to return per page",
            "in": "query",
            "name": "limit",
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
                  "properties": {
                    "next_page_token": {
                      "$ref": "#/components/schemas/NextPageToken"
                    },
                    "subscriptions": {
                      "items": {
                        "$ref": "#/components/schemas/PortfolioSubscription"
                      },
                      "type": "array"
                    }
                  },
                  "required": [
                    "subscriptions",
                    "next_page_token"
                  ],
                  "type": "object"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "List All Subscriptions",
        "tags": [
          "Rebalancing"
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
      "name": "Rebalancing"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```