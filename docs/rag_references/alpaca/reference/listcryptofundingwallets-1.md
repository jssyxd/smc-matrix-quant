# Retrieve Crypto Funding Wallets

Source: https://docs.alpaca.markets/us/reference/listcryptofundingwallets-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Crypto Funding Wallets

Lists wallets for the account given in the path parameter. If an asset is specified and no wallet for the account and asset pair exists one will be created. If no asset is specified only existing wallets will be listed for the account. An account may have at most one wallet per asset.

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
    "/v1/accounts/{account_id}/wallets": {
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
        "summary": "Retrieve Crypto Funding Wallets",
        "tags": [
          "Crypto Funding"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        },
        {
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
            "enum": [
              "SOL",
              "ETH",
              "BTC",
              "XRP",
              "ARB"
            ],
            "type": "string"
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