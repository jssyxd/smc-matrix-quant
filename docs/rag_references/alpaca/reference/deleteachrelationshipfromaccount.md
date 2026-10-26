# Delete an existing ACH relationship

Source: https://docs.alpaca.markets/us/reference/deleteachrelationshipfromaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Delete an existing ACH relationship

Delete an existing ACH relationship for an account

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
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
    "/v1/accounts/{account_id}/ach_relationships/{ach_relationship_id}": {
      "delete": {
        "description": "Delete an existing ACH relationship for an account",
        "operationId": "deleteACHRelationshipFromAccount",
        "responses": {
          "204": {
            "description": "Success (No Content)"
          },
          "400": {
            "description": "the passed in account_id or relationship_id were invalid"
          },
          "404": {
            "description": "Relationship Not Found"
          }
        },
        "summary": "Delete an existing ACH relationship",
        "tags": [
          "Funding"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        },
        {
          "description": "ACH relationship identifier",
          "in": "path",
          "name": "ach_relationship_id",
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```