# Redeem a Tokenized Asset

Source: https://docs.alpaca.markets/us/reference/posttokenizationredeem.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Redeem a Tokenized Asset

This endpoint is used by the tokenized asset issuer to confirm the redemption of tokens previously held in the Authorized Participant's wallet. When the issuer invokes this endpoint, Alpaca will  initiate a journal of the underlying asset into the Authorized Participant's account.

**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is
idempotent. Multiple requests with the same key and identical request body will
create only one redeem request. A subsequent request returns the previously created
request with the same response (no duplicate is created). If the same key is used
with a different request body, the API returns `422 Unprocessable Entity`.

**Recommended for production**: Always supply `Idempotency-Key` when requesting a
redemption. This allows safe retries on timeouts, network errors, or 5xx responses
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
      "TokenizationRedeemRequest": {
        "properties": {
          "client_account_id": {
            "description": "Alpaca account ID (UUID) of the Authorized Participant. Exactly one of `client_external_account_id` or `client_account_id` must be provided to identify the Authorized Participant whose account will receive the underlying asset. The deprecated `client_id` field is still accepted as an alias for `client_external_account_id` during the deprecation window.",
            "format": "uuid",
            "type": "string"
          },
          "client_external_account_id": {
            "description": "Customer's client identifier on the issuer's platform. Exactly one of `client_external_account_id` or `client_account_id` must be provided to identify the Authorized Participant whose account will receive the underlying asset. The deprecated `client_id` field is still accepted as an alias for `client_external_account_id` during the deprecation window.",
            "type": "string"
          },
          "client_id": {
            "deprecated": true,
            "description": "Customer's client identifier on the issuer's platform. Use `client_external_account_id` instead.",
            "type": "string",
            "x-deprecation": {
              "reason": "Use client_external_account_id instead.",
              "since": "2026-07-15",
              "sunset": "2026-10-15"
            }
          },
          "issuer_request_id": {
            "description": "Unique identifier of the redemption request set by the issuer",
            "type": "string"
          },
          "network": {
            "$ref": "#/components/schemas/TokenizationNetwork"
          },
          "qty": {
            "description": "The quantity to convert into the underlying asset. It can be fractional.",
            "type": "string"
          },
          "token_symbol": {
            "description": "The tokenized asset symbol",
            "type": "string"
          },
          "tx_hash": {
            "description": "Transaction hash of the completed request on the blockchain",
            "type": "string"
          },
          "underlying_symbol": {
            "description": "The underlying asset symbol",
            "type": "string"
          },
          "wallet_address": {
            "description": "The address where the redeemed tokens were originally held",
            "type": "string"
          }
        },
        "required": [
          "issuer_request_id",
          "underlying_symbol",
          "token_symbol",
          "qty",
          "network",
          "wallet_address",
          "tx_hash"
        ],
        "title": "TokenizationRedeemRequest",
        "type": "object"
      },
      "TokenizationRedeemResponse": {
        "properties": {
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "issuer": {
            "$ref": "#/components/schemas/TokenizationIssuer"
          },
          "issuer_request_id": {
            "description": "Unique identifier of the redemption request set by the issuer",
            "type": "string"
          },
          "network": {
            "$ref": "#/components/schemas/TokenizationNetwork"
          },
          "qty": {
            "description": "The quantity to convert into the underlying asset. It can be fractional.",
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
          "tx_hash": {
            "description": "Transaction hash of the completed request on the blockchain",
            "type": "string"
          },
          "type": {
            "$ref": "#/components/schemas/TokenizationRequestType"
          },
          "underlying_symbol": {
            "description": "The underlying asset symbol",
            "type": "string"
          },
          "wallet_address": {
            "description": "The address where the redeemed tokens were originally held",
            "type": "string"
          }
        },
        "required": [
          "tokenization_request_id",
          "issuer_request_id",
          "created_at",
          "type",
          "status",
          "underlying_symbol",
          "token_symbol",
          "qty",
          "issuer",
          "network",
          "wallet_address",
          "tx_hash"
        ],
        "title": "TokenizationRedeemResponse",
        "type": "object"
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
      },
      "TokenizationRequestType": {
        "description": "Tokenization request type",
        "enum": [
          "mint",
          "redeem"
        ],
        "example": "mint",
        "title": "TokenizationRequestType",
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
    "/v1/accounts/{account_id}/tokenization/callback/redeem": {
      "post": {
        "description": "This endpoint is used by the tokenized asset issuer to confirm the redemption of tokens previously held in the Authorized Participant's wallet. When the issuer invokes this endpoint, Alpaca will  initiate a journal of the underlying asset into the Authorized Participant's account.\n\n**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is\nidempotent. Multiple requests with the same key and identical request body will\ncreate only one redeem request. A subsequent request returns the previously created\nrequest with the same response (no duplicate is created). If the same key is used\nwith a different request body, the API returns `422 Unprocessable Entity`.\n\n**Recommended for production**: Always supply `Idempotency-Key` when requesting a\nredemption. This allows safe retries on timeouts, network errors, or 5xx responses\nwithout risking duplicate requests. Use a client-generated unique value (e.g. UUID).",
        "operationId": "postTokenizationRedeem",
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
                "$ref": "#/components/schemas/TokenizationRedeemRequest"
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
                  "$ref": "#/components/schemas/TokenizationRedeemResponse"
                }
              }
            },
            "description": "Successfully requested redemption of a tokenized asset."
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
            "description": "Bad request (e.g. malformed input, insufficient quantity, or account not authorized to redeem). Also returned when the `Idempotency-Key` header is malformed, or when replaying a request that was originally rejected."
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
                  "message": "issuer_request_id is required, tx_hash is required"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "One or more request parameters are missing or invalid, or the same `Idempotency-Key` was reused with a different request body."
          }
        },
        "summary": "Redeem a Tokenized Asset",
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