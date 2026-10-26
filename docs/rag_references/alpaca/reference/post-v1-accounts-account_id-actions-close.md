# Close an Account

Source: https://docs.alpaca.markets/us/reference/post-v1-accounts-account_id-actions-close.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Close an Account

This operation closes an active account. The underlying records and information of the account are not deleted by this operation.

**Before closing an account, you are responsible for closing all the positions and withdrawing all the money associated with that account. Learn more in the Positions Documentation.**

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
    "/v1/accounts/{account_id}/actions/close": {
      "parameters": [
        {
          "description": "The id of the account to be closed",
          "in": "path",
          "name": "account_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ],
      "post": {
        "description": "This operation closes an active account. The underlying records and information of the account are not deleted by this operation.\n\n**Before closing an account, you are responsible for closing all the positions and withdrawing all the money associated with that account. Learn more in the Positions Documentation.**",
        "operationId": "post-v1-accounts-account_id-actions-close",
        "responses": {
          "204": {
            "description": "Success"
          },
          "404": {
            "description": "Account Not Found"
          }
        },
        "summary": "Close an Account",
        "tags": [
          "Accounts"
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
      "name": "Accounts"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```