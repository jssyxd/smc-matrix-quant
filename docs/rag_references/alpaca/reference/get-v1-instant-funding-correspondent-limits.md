# Get instant funding limits

Source: https://docs.alpaca.markets/us/reference/get-v1-instant-funding-correspondent-limits.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get instant funding limits

Returns globally configured limits for the correspondent. These limits are used to determine
the maximum amount that can be extended to all accounts, and reaching this limit will result
in further requests to create instant funding requests being rejected.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CorrespondentLimit": {
        "properties": {
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
    "/v1/instant_funding/limits": {
      "get": {
        "description": "Returns globally configured limits for the correspondent. These limits are used to determine\nthe maximum amount that can be extended to all accounts, and reaching this limit will result\nin further requests to create instant funding requests being rejected.",
        "operationId": "get-v1-instant-funding-correspondent-limits",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CorrespondentLimit"
                }
              }
            },
            "description": "correspondent instant funding limits"
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
        "summary": "Get instant funding limits",
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