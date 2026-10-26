# Get Tokenization Request by ID

Source: https://docs.alpaca.markets/us/reference/gettokenizationrequestbyidbroker.md

---
updatedAt: 2026-06-01T19:33:45.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Tokenization Request by ID

Retrieve a single tokenization request by its `tokenization_request_id`. This endpoint may be used by the tokenized asset issuer or by an Authorized Participant (AP), and returns either a mint or a redeem request.

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
      "TokenizationRequest": {
        "properties": {
          "account": {
            "deprecated": true,
            "description": "Alpaca account ID associated with this tokenization request. Use `client_account_id` instead.",
            "type": "string",
            "x-deprecation": {
              "reason": "Use client_account_id instead.",
              "since": "2026-07-15",
              "sunset": "2026-10-15"
            }
          },
          "client_account_id": {
            "description": "Alpaca account UUID of the Authorized Participant associated with this tokenization request",
            "format": "uuid",
            "type": "string"
          },
          "client_external_account_id": {
            "description": "Issuer-side account identifier of the Authorized Participant associated with this tokenization request",
            "type": "string"
          },
          "client_request_id": {
            "description": "Authorized Participant-supplied label associated with this tokenization request",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "fees": {
            "description": "Fees charged for this tokenization request",
            "type": [
              "string",
              "null"
            ]
          },
          "issuer": {
            "$ref": "#/components/schemas/TokenizationIssuer"
          },
          "issuer_account": {
            "deprecated": true,
            "description": "Issuer's account ID associated with this tokenization request. Use `client_external_account_id` instead.",
            "type": "string",
            "x-deprecation": {
              "reason": "Use client_external_account_id instead.",
              "since": "2026-07-15",
              "sunset": "2026-10-15"
            }
          },
          "issuer_request_id": {
            "description": "Unique identifier of the tokenization request set by the issuer",
            "type": [
              "string",
              "null"
            ]
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
          "tx_hash": {
            "description": "Transaction hash of the completed request on the blockchain",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "$ref": "#/components/schemas/TokenizationRequestType"
          },
          "underlying_symbol": {
            "description": "The underlying asset symbol",
            "type": "string"
          },
          "updated_at": {
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "wallet_address": {
            "description": "The wallet address associated with this tokenization request",
            "type": "string"
          }
        },
        "required": [
          "tokenization_request_id",
          "created_at",
          "type",
          "status",
          "underlying_symbol",
          "token_symbol",
          "qty",
          "issuer",
          "network",
          "wallet_address"
        ],
        "title": "TokenizationRequest",
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
    "/v1/accounts/{account_id}/tokenization/requests/{tokenization_request_id}": {
      "get": {
        "description": "Retrieve a single tokenization request by its `tokenization_request_id`. This endpoint may be used by the tokenized asset issuer or by an Authorized Participant (AP), and returns either a mint or a redeem request.",
        "operationId": "getTokenizationRequestByIDBroker",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          },
          {
            "description": "Unique identifier of the tokenization request, as returned by the mint endpoint or the list-requests endpoint.",
            "in": "path",
            "name": "tokenization_request_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "example": {
                  "created_at": "2025-11-04T18:38:01.942282Z",
                  "fees": "0.5",
                  "issuer": "xstocks",
                  "network": "solana",
                  "qty": "1.0",
                  "status": "completed",
                  "token_symbol": "TSLAx",
                  "tokenization_request_id": "5b1d6a3e-7f0a-4d2c-b8e1-9e6f1c0d2c4a",
                  "tx_hash": "5J7ZxK4QwR3vH2pY1aB6sN8cM9tD0fA2eXyVwUjL3kPqR4mZcF7nB1tA8sH6dG2pE",
                  "type": "mint",
                  "underlying_symbol": "TSLA",
                  "updated_at": "2025-11-04T18:38:42.117004Z",
                  "wallet_address": "5dXY1aH2tQpV3wXmJg6Z7c8B4nKvF9bA1pQrSt2uVwYxXz"
                },
                "schema": {
                  "$ref": "#/components/schemas/TokenizationRequest"
                }
              }
            },
            "description": "Successful response"
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
          "404": {
            "content": {
              "application/json": {
                "example": {
                  "code": 40410000,
                  "message": "tokenization request not found"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "No tokenization request with the supplied `tokenization_request_id` exists for this account."
          },
          "422": {
            "content": {
              "application/json": {
                "example": {
                  "code": 42210001,
                  "message": "tokenization_request_id is not a valid UUID"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The `tokenization_request_id` path parameter is not a valid UUID."
          }
        },
        "summary": "Get Tokenization Request by ID",
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