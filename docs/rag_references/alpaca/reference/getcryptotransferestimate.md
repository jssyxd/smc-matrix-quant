# Returns the estimated gas fee for a proposed transaction.

Source: https://docs.alpaca.markets/us/reference/getcryptotransferestimate.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Returns the estimated gas fee for a proposed transaction.

Returns the estimated on-chain network (gas) fee for a proposed crypto withdrawal at current chain conditions. Pass the `asset`, `from_address`, `to_address`, and `amount` you intend to send; the response reports the network fee that would be charged for the corresponding transaction.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "WalletFeeEstimateResponse": {
        "description": "Estimated on-chain fee breakdown for a proposed crypto withdrawal, including the total fee and the underlying network (gas) fee.",
        "properties": {
          "fee": {
            "example": "0.0505",
            "format": "decimal",
            "type": "string"
          },
          "network_fee": {
            "example": "0.0825",
            "format": "decimal",
            "type": "string"
          }
        },
        "type": "object"
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
    "/v2/wallets/fees/estimate": {
      "get": {
        "description": "Returns the estimated on-chain network (gas) fee for a proposed crypto withdrawal at current chain conditions. Pass the `asset`, `from_address`, `to_address`, and `amount` you intend to send; the response reports the network fee that would be charged for the corresponding transaction.",
        "operationId": "getCryptoTransferEstimate",
        "parameters": [
          {
            "description": "The asset for the proposed transaction",
            "in": "query",
            "name": "asset",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The originating address of the proposed transaction",
            "in": "query",
            "name": "from_address",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The destination address of the proposed transaction",
            "in": "query",
            "name": "to_address",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The amount, denoted in the specified asset, of the proposed transaction",
            "in": "query",
            "name": "amount",
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
                  "$ref": "#/components/schemas/WalletFeeEstimateResponse"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Returns the estimated gas fee for a proposed transaction.",
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