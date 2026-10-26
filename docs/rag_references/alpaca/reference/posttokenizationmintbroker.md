# Mint a Tokenized Asset

Source: https://docs.alpaca.markets/us/reference/posttokenizationmintbroker.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Mint a Tokenized Asset

This endpoint is used by an Authorized Participant to request the minting of a tokenized asset. Alpaca will initiate a journal of the underlying asset from the Authorized Participant's account to the issuer's account.

**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is
idempotent. Multiple requests with the same key and identical request body will
create only one mint request. A subsequent request returns the previously created
request with the same response (no duplicate is created). If the same key is used
with a different request body, the API returns `422 Unprocessable Entity`.

**Recommended for production**: Always supply `Idempotency-Key` when requesting a
mint. This allows safe retries on timeouts, network errors, or 5xx responses
without risking duplicate requests. Use a client-generated unique value (e.g. UUID).

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
      },
      "LegacyIdempotencyKey": {
        "description": "Optional client-generated key for safe retries and duplicate request detection.\nThis endpoint currently accepts keys up to 128 characters. Alpaca is moving toward\na 36-character maximum; new implementations should generate a unique UUIDv7 or\nUUIDv4 value (36 characters including hyphens) for each logical operation. Do not\nreuse a key across operations.\n",
        "in": "header",
        "name": "Idempotency-Key",
        "required": false,
        "schema": {
          "maxLength": 128,
          "type": "string"
        }
      }
    },
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
      "TokenizationIssuer": {
        "description": "The tokenized asset's issuer",
        "enum": [
          "binance",
          "coinbase",
          "ondo",
          "st0x",
          "xstocks"
        ],
        "example": "xstocks",
        "title": "TokenizationIssuer",
        "type": "string"
      },
      "TokenizationMintRequest": {
        "properties": {
          "issuer": {
            "$ref": "#/components/schemas/TokenizationIssuer"
          },
          "network": {
            "$ref": "#/components/schemas/TokenizationNetwork"
          },
          "qty": {
            "description": "The underlying quantity to convert into the tokenized asset. It can be fractional.",
            "type": "string"
          },
          "underlying_symbol": {
            "description": "The underlying asset symbol",
            "type": "string"
          },
          "wallet_address": {
            "description": "The wallet address to receive the tokenized asset",
            "type": "string"
          }
        },
        "required": [
          "underlying_symbol",
          "qty",
          "issuer",
          "network",
          "wallet_address"
        ],
        "title": "TokenizationMintRequest",
        "type": "object"
      },
      "TokenizationMintResponse": {
        "properties": {
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "issuer": {
            "$ref": "#/components/schemas/TokenizationIssuer"
          },
          "network": {
            "$ref": "#/components/schemas/TokenizationNetwork"
          },
          "qty": {
            "description": "The quantity to convert for this tokenization request. It can be fractional.",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/TokenizationRequestStatus"
          },
          "token_symbol": {
            "description": "The tokenized asset symbol",
            "type": "string"
          },
          "tokenization_request_id": {
            "description": "Unique identifier of the tokenization request set by Alpaca",
            "type": "string"
          },
          "underlying_symbol": {
            "description": "The underlying asset symbol",
            "type": "string"
          }
        },
        "required": [
          "tokenization_request_id",
          "status",
          "underlying_symbol",
          "token_symbol",
          "qty",
          "created_at",
          "issuer",
          "network"
        ],
        "title": "TokenizationMintResponse",
        "type": "object"
      },
      "TokenizationNetwork": {
        "description": "The token's blockchain network",
        "enum": [
          "arbitrum",
          "base",
          "binance",
          "cronos",
          "ethereum",
          "hypercore",
          "hyperevm",
          "mantle",
          "robinhood",
          "solana",
          "ton",
          "tron"
        ],
        "example": "solana",
        "title": "TokenizationNetwork",
        "type": "string"
      },
      "TokenizationRequestStatus": {
        "description": "Status of the tokenization request",
        "enum": [
          "pending",
          "rejected",
          "completed"
        ],
        "example": "completed",
        "title": "TokenizationRequestStatus",
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
    "/v1/accounts/{account_id}/tokenization/mint": {
      "post": {
        "description": "This endpoint is used by an Authorized Participant to request the minting of a tokenized asset. Alpaca will initiate a journal of the underlying asset from the Authorized Participant's account to the issuer's account.\n\n**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is\nidempotent. Multiple requests with the same key and identical request body will\ncreate only one mint request. A subsequent request returns the previously created\nrequest with the same response (no duplicate is created). If the same key is used\nwith a different request body, the API returns `422 Unprocessable Entity`.\n\n**Recommended for production**: Always supply `Idempotency-Key` when requesting a\nmint. This allows safe retries on timeouts, network errors, or 5xx responses\nwithout risking duplicate requests. Use a client-generated unique value (e.g. UUID).",
        "operationId": "postTokenizationMintBroker",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          },
          {
            "$ref": "#/components/parameters/LegacyIdempotencyKey"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/TokenizationMintRequest"
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
                  "$ref": "#/components/schemas/TokenizationMintResponse"
                }
              }
            },
            "description": "Successfully requested minting of a tokenized asset."
          },
          "400": {
            "content": {
              "application/json": {
                "example": {
                  "code": 40010000,
                  "message": "failed to decode request body"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Bad request (e.g. malformed input, insufficient position, or account not authorized to mint). Also returned when the `Idempotency-Key` header is malformed, or when replaying a request that was originally rejected."
          },
          "401": {
            "content": {
              "application/json": {
                "example": {
                  "code": 40110000,
                  "message": "unauthorized"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Authentication credentials are missing or invalid."
          },
          "403": {
            "content": {
              "application/json": {
                "example": {
                  "code": 40310000,
                  "message": "forbidden"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Caller is not authorized to perform this operation."
          },
          "422": {
            "content": {
              "application/json": {
                "example": {
                  "code": 42210001,
                  "message": "issuer is required, network is required"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "One or more request parameters are missing or invalid, or the same `Idempotency-Key` was reused with a different request body."
          }
        },
        "summary": "Mint a Tokenized Asset",
        "tags": [
          "Tokenization"
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
      "name": "Tokenization"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```