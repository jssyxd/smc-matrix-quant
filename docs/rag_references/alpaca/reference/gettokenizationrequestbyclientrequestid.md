# Get Tokenization Request by `client_request_id`

Source: https://docs.alpaca.markets/us/reference/gettokenizationrequestbyclientrequestid.md

---
updatedAt: 2026-06-01T19:35:16.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Tokenization Request by `client_request_id`

An Authorized Participant can use this endpoint to retrieve a single mint tokenization request by their own `client_request_id` -- the AP-supplied label originally passed on the mint request. If the AP has reused a `client_request_id` across multiple requests, the most recently created request is returned.

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
            "example": "06b9d76e-1733-460c-844e-48d1ae0f10c3",
            "type": "string",
            "x-deprecation": {
              "reason": "Use client_account_id instead.",
              "since": "2026-07-15",
              "sunset": "2026-10-15"
            }
          },
          "client_account_id": {
            "description": "Alpaca account UUID of the Authorized Participant associated with this tokenization request",
            "example": "06b9d76e-1733-460c-844e-48d1ae0f10c3",
            "format": "uuid",
            "type": "string"
          },
          "client_external_account_id": {
            "description": "Issuer-side account identifier of the Authorized Participant associated with this tokenization request",
            "example": "AP-EXT-001",
            "type": "string"
          },
          "client_request_id": {
            "description": "Authorized Participant-supplied label associated with this tokenization request",
            "example": "ap-mint-2026-01-05-001",
            "type": "string"
          },
          "created_at": {
            "example": "2026-01-02T15:04:05Z",
            "format": "date-time",
            "type": "string"
          },
          "fees": {
            "description": "Fees charged for this tokenization request",
            "example": null,
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
            "example": "AP-EXT-001",
            "type": "string",
            "x-deprecation": {
              "reason": "Use client_external_account_id instead.",
              "since": "2026-07-15",
              "sunset": "2026-10-15"
            }
          },
          "issuer_request_id": {
            "description": "Unique identifier of the tokenization request set by the issuer",
            "example": null,
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
            "example": "10",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/TokenizationRequestStatus"
          },
          "token_symbol": {
            "description": "The tokenized asset symbol",
            "example": "AAPLx",
            "type": "string"
          },
          "tokenization_request_id": {
            "description": "Unique identifier of the tokenization request set by Alpaca",
            "example": "5b1d6a3e-7f0a-4d2c-b8e1-9e6f1c0d2c4a",
            "type": "string"
          },
          "tx_hash": {
            "description": "Transaction hash of the completed request on the blockchain",
            "example": null,
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
            "example": "AAPL",
            "type": "string"
          },
          "updated_at": {
            "example": null,
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "wallet_address": {
            "description": "The wallet address associated with this tokenization request",
            "example": "5dXY1aH2tQpV3wXmJg6Z7c8B4nKvF9bA1pQrSt2uVwYxXz",
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
    "/v2/tokenization/requests:by_client_request_id": {
      "get": {
        "description": "An Authorized Participant can use this endpoint to retrieve a single mint tokenization request by their own `client_request_id` -- the AP-supplied label originally passed on the mint request. If the AP has reused a `client_request_id` across multiple requests, the most recently created request is returned.",
        "operationId": "getTokenizationRequestByClientRequestID",
        "parameters": [
          {
            "description": "AP-supplied request identifier originally passed on the mint request, echoed back on the tokenization-request response.",
            "in": "query",
            "name": "client_request_id",
            "required": true,
            "schema": {
              "example": "ap-request-2025-11-04-001",
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
            "description": "No tokenization request with the supplied `client_request_id` exists for the calling account."
          },
          "422": {
            "content": {
              "application/json": {
                "example": {
                  "code": 42210001,
                  "message": "client_request_id query parameter is required"
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The `client_request_id` query parameter is missing."
          }
        },
        "summary": "Get Tokenization Request by `client_request_id`",
        "tags": [
          "Tokenization"
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
      "description": "Request minting of tokenized assets and list tokenization requests on the Instant Tokenization Network (ITN).",
      "name": "Tokenization"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```