# Creates a funding wallet

Source: https://docs.alpaca.markets/us/reference/createfundingwallet.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Creates a funding wallet

Creates a funding wallet for the specified account. The request is rejected if the account already has a funding wallet.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
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
      },
      "FundingWallet": {
        "properties": {
          "account_id": {
            "format": "uuid",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/FundingWalletStatus"
          }
        },
        "required": [
          "account_id",
          "status",
          "created_at"
        ],
        "type": "object"
      },
      "FundingWalletStatus": {
        "description": "Status:\n * `active`: The funding wallet is ready\n * `pending`: The funding wallet is being processed\n * `disabled`: The funding wallet is disabled\n",
        "enum": [
          "active",
          "pending",
          "disabled"
        ],
        "type": "string"
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
    "/v1beta/accounts/{account_id}/funding_wallet": {
      "post": {
        "description": "Creates a funding wallet for the specified account. The request is rejected if the account already has a funding wallet.",
        "operationId": "createFundingWallet",
        "parameters": [
          {
            "description": "UUID alpaca account ID",
            "in": "path",
            "name": "account_id",
            "required": true,
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
                  "$ref": "#/components/schemas/FundingWallet"
                }
              }
            },
            "description": "funding wallet"
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
        "summary": "Creates a funding wallet",
        "tags": [
          "Funding Wallets"
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
      "name": "Funding Wallets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```