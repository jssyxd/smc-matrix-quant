# Retrieve Crypto Funding Transfers

Source: https://docs.alpaca.markets/us/reference/listcryptofundingtransfers-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Crypto Funding Transfers

Returns an array of all transfers associated with the given account across all wallets.

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
    "schemas": {
      "CryptoTransfer": {
        "description": "Transfers allow you to transfer assets into your end customer's account (deposits) or out (withdrawal).",
        "properties": {
          "amount": {
            "description": "Amount of transfer denominated in the underlying crypto asset",
            "type": "string"
          },
          "asset": {
            "description": "Symbol of crypto asset for given transfer (e.g. BTC)",
            "type": "string"
          },
          "chain": {
            "description": "Underlying network for given transfer",
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp when transfer was created",
            "format": "date-time",
            "type": "string"
          },
          "direction": {
            "$ref": "#/components/schemas/TransferDirection"
          },
          "fees": {
            "type": "string"
          },
          "from_address": {
            "description": "Originating address of the transfer",
            "type": "string"
          },
          "id": {
            "description": "The crypto transfer ID",
            "format": "uuid",
            "type": "string"
          },
          "network_fee": {
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/CryptoTransferStatus"
          },
          "to_address": {
            "description": "Destination address of the transfer",
            "type": "string"
          },
          "tx_hash": {
            "description": "On-chain transaction hash (e.g. 0xabc...xyz)",
            "type": "string"
          },
          "usd_value": {
            "description": "Equivalent USD value at time of transfer",
            "type": "string"
          }
        },
        "type": "object"
      },
      "CryptoTransferStatus": {
        "enum": [
          "PROCESSING",
          "FAILED",
          "COMPLETE"
        ],
        "example": "PROCESSING",
        "type": "string"
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
      "TransferDirection": {
        "description": "- **INCOMING**\nFunds incoming to user's account (deposit).\n- **OUTGOING**\nFunds outgoing from user's account (withdrawal).\n",
        "enum": [
          "INCOMING",
          "OUTGOING"
        ],
        "example": "INCOMING",
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
    "/v1/accounts/{account_id}/wallets/transfers": {
      "get": {
        "description": "Returns an array of all transfers associated with the given account across all wallets.",
        "operationId": "listCryptoFundingTransfers",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CryptoTransfer"
                }
              }
            },
            "description": "An array of transfer objects"
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
        "summary": "Retrieve Crypto Funding Transfers",
        "tags": [
          "Crypto Funding"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
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
      "name": "Crypto Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```