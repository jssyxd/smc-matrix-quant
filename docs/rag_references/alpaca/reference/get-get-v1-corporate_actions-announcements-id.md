# Retrieve a Specific Announcement

Source: https://docs.alpaca.markets/us/reference/get-get-v1-corporate_actions-announcements-id.md

---
updatedAt: 2026-05-27T17:58:38.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve a Specific Announcement

This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.

# OpenAPI definition

```json
{
  "components": {
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
    "/v1/corporate_actions/announcements/{id}": {
      "get": {
        "deprecated": true,
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.",
        "operationId": "get-GET-v1-corporate_actions-announcements-id",
        "responses": {
          "200": {
            "description": "An Announcement object."
          },
          "400": {
            "description": "The body in the request is not valid"
          },
          "422": {
            "description": "Invalid input value."
          },
          "500": {
            "description": "A server error occurred. Please contact Alpaca."
          }
        },
        "summary": "Retrieve a Specific Announcement",
        "tags": [
          "Corporate Actions"
        ]
      },
      "parameters": [
        {
          "description": "The id of the corporate action announcement to be returned.",
          "in": "path",
          "name": "id",
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
      "name": "Corporate Actions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```