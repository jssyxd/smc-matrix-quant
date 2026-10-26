# Retrieve Crypto Funding Wallets

Source: https://docs.alpaca.markets/us/reference/listcryptofundingwallets.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Crypto Funding Wallets

Lists wallets for the account given in the path parameter. If an asset is specified and no wallet for the account and asset pair exists one will be created. If no asset is specified only existing wallets will be listed for the account. An account may have at most one wallet per asset.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CryptoChain": {
        "description": "Chain identifier for multi-chain crypto assets.",
        "enum": [
          "SOL",
          "ETH",
          "BTC",
          "XRP",
          "ARB"
        ],
        "example": "ETH",
        "type": "string"
      },
      "CryptoWallet": {
        "properties": {
          "address": {
            "type": "string"
          },
          "chain": {
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp (RFC3339) of account creation.",
            "format": "date-time",
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
    "/v2/wallets": {
      "get": {
        "description": "Lists wallets for the account given in the path parameter. If an asset is specified and no wallet for the account and asset pair exists one will be created. If no asset is specified only existing wallets will be listed for the account. An account may have at most one wallet per asset.",
        "operationId": "listCryptoFundingWallets",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CryptoWallet"
                }
              }
            },
            "description": "A single wallet object if an asset is specified or an array of wallet objects if no asset is specified"
          }
        },
        "summary": "Retrieve Crypto Funding Wallets",
        "tags": [
          "Crypto Funding"
        ]
      },
      "parameters": [
        {
          "description": "Filter by crypto asset symbol, e.g. BTC, ETH, USDT. If specified and no wallet exists, one will be created.",
          "in": "query",
          "name": "asset",
          "schema": {
            "type": "string"
          }
        },
        {
          "description": "Optional chain identifier. Use to request wallets for a specific chain when asset is a multi-chain crypto asset. If not specified, network is considered.",
          "in": "query",
          "name": "chain",
          "schema": {
            "$ref": "#/components/schemas/CryptoChain"
          }
        },
        {
          "description": "Deprecated. Use chain instead. Optional network identifier which is used to request wallets for a specific network when asset is a multi-chain crypto asset. When both 'chain' and 'network' are specified, 'chain' will take precedence and 'network' will be ignored. If 'chain' and 'network' are not specified, the default 'network' (ethereum) will be used.",
          "in": "query",
          "name": "network",
          "schema": {
            "deprecated": true,
            "enum": [
              "ethereum",
              "solana"
            ],
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