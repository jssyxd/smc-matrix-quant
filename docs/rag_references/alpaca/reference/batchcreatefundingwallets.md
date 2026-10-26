# Batch create funding wallets

Source: https://docs.alpaca.markets/us/reference/batchcreatefundingwallets.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Batch create funding wallets

Creates funding wallets for a list of accounts in a single request. Every `account_id` in the request must belong to your firm, and the request is rejected if a funding wallet already exists for any of the supplied accounts.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "BatchCreateFundingWalletRequest": {
        "properties": {
          "account_ids": {
            "description": "list of UUID account ids which will have funding wallets created",
            "items": {
              "type": "string"
            },
            "type": "array"
          }
        },
        "type": "object"
      },
      "BatchCreateFundingWalletResponse": {
        "properties": {
          "funding_wallets": {
            "items": {
              "$ref": "#/components/schemas/FundingWallet"
            },
            "type": "array"
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
    "/v1beta/accounts/funding_wallet": {
      "post": {
        "description": "Creates funding wallets for a list of accounts in a single request. Every `account_id` in the request must belong to your firm, and the request is rejected if a funding wallet already exists for any of the supplied accounts.",
        "operationId": "batchCreateFundingWallets",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/BatchCreateFundingWalletRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/BatchCreateFundingWalletResponse"
                }
              }
            },
            "description": "Funding wallets"
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Error response."
          }
        },
        "summary": "Batch create funding wallets",
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