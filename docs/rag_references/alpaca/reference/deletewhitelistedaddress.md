# Delete a whitelisted address

Source: https://docs.alpaca.markets/us/reference/deletewhitelistedaddress.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Delete a whitelisted address

Deletes a whitelisted withdrawal address by ID. Subsequent withdrawals targeting the deleted address will be rejected.

# OpenAPI definition

```json
{
  "components": {
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
    "/v2/wallets/whitelists/{whitelisted_address_id}": {
      "delete": {
        "description": "Deletes a whitelisted withdrawal address by ID. Subsequent withdrawals targeting the deleted address will be rejected.",
        "operationId": "deleteWhitelistedAddress",
        "responses": {
          "200": {
            "description": "Successfully deleted a whitelisted address"
          }
        },
        "summary": "Delete a whitelisted address",
        "tags": [
          "Crypto Funding"
        ]
      },
      "parameters": [
        {
          "description": "The whitelisted address to delete",
          "in": "path",
          "name": "whitelisted_address_id",
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
      "name": "Crypto Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```