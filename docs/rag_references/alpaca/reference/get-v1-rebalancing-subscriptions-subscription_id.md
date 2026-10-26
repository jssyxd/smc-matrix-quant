# Get Subscription by ID

Source: https://docs.alpaca.markets/us/reference/get-v1-rebalancing-subscriptions-subscription_id.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Subscription by ID

Get a subscription by its ID.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
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
    "/v1/rebalancing/subscriptions/{subscription_id}": {
      "get": {
        "description": "Get a subscription by its ID.",
        "operationId": "get-v1-rebalancing-subscriptions-subscription_id",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/PortfolioSubscription"
                }
              }
            },
            "description": "The portfolio subscription"
          }
        },
        "summary": "Get Subscription by ID",
        "tags": [
          "Rebalancing"
        ]
      },
      "parameters": [
        {
          "in": "path",
          "name": "subscription_id",
          "required": true,
          "schema": {
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
      "name": "Rebalancing"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```