# Retrieve Crypto Funding Transfers

Source: https://docs.alpaca.markets/us/reference/listcryptofundingtransfers.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Crypto Funding Transfers

Returns an array of all transfers associated with the given account across all wallets.

# OpenAPI definition

```json
{
  "components": {
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
      "TransferDirection": {
        "enum": [
          "INCOMING",
          "OUTGOING"
        ],
        "example": "INCOMING",
        "type": "string"
      }
    },
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
    "/v2/wallets/transfers": {
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
          }
        },
        "summary": "Retrieve Crypto Funding Transfers",
        "tags": [
          "Crypto Funding"
        ]
      }
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