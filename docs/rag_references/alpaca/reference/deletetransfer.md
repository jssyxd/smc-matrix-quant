# Request to Close a Transfer

Source: https://docs.alpaca.markets/us/reference/deletetransfer.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Request to Close a Transfer

Request to close a transfer

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
    "/v1/accounts/{account_id}/transfers/{transfer_id}": {
      "delete": {
        "description": "Request to close a transfer",
        "operationId": "deleteTransfer",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          },
          {
            "description": "Transfer identifier",
            "in": "path",
            "name": "transfer_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Success"
          },
          "404": {
            "description": "Transfer Not Found"
          }
        },
        "summary": "Request to Close a Transfer",
        "tags": [
          "Funding"
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```