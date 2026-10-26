# Get instant funding account limits

Source: https://docs.alpaca.markets/us/reference/get-v1-instant-funding-account-limits.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get instant funding account limits

Returns the limits for individual partner accounts.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AccountLimit": {
        "properties": {
          "account_no": {
            "type": "string"
          },
          "amount_available": {
            "format": "decimal",
            "type": "string"
          },
          "amount_in_use": {
            "format": "decimal",
            "type": "string"
          },
          "amount_limit": {
            "format": "decimal",
            "type": "string"
          }
        },
        "required": [
          "account_no",
          "amount_in_use",
          "amount_available",
          "amount_limit"
        ],
        "type": "object"
      },
      "Error": {
        "properties": {
          "code": {
            "type": "number"
          },
          "message": {
            "type": "string"
          }
        },
        "required": [
          "code",
          "message"
        ],
        "title": "Error",
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
    "/v1/instant_funding/limits/accounts": {
      "get": {
        "description": "Returns the limits for individual partner accounts.",
        "operationId": "get-v1-instant-funding-account-limits",
        "parameters": [
          {
            "description": "Filter limits based on comma-separated account numbers",
            "explode": false,
            "in": "query",
            "name": "account_numbers",
            "required": true,
            "schema": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "style": "form"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/AccountLimit"
                  },
                  "type": "array"
                }
              }
            },
            "description": "invidual broker account limits"
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "error"
          }
        },
        "summary": "Get instant funding account limits",
        "tags": [
          "Instant Funding"
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
      "name": "Instant Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```