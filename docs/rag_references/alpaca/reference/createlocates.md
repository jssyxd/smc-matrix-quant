# Create Locate

Source: https://docs.alpaca.markets/us/reference/createlocates.md

---
updatedAt: 2026-06-19T17:13:53.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create Locate

Creates a locate request for a short sale. This endpoint is not available in paper trading.

**Idempotency**: Reusing the same key with the same request returns the original
locate response. Reusing the same key with a different request returns HTTP 422.


# OpenAPI definition

```json
{
  "components": {
    "parameters": {
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
      "CreateLocateRequest": {
        "description": "Request to locate shares for a short sale.",
        "example": {
          "all_or_none": false,
          "limit_price": "0.05",
          "qty": 100,
          "symbol": "TSLA"
        },
        "properties": {
          "all_or_none": {
            "default": false,
            "description": "Reject the locate unless the full requested quantity is available.",
            "example": false,
            "type": "boolean"
          },
          "limit_price": {
            "description": "Maximum acceptable locate fee per share, as a decimal string in USD.\nIf omitted, any quoted fee is accepted.\n",
            "example": "0.05",
            "type": [
              "string",
              "null"
            ]
          },
          "qty": {
            "description": "Number of shares to locate. Must be positive and in round lots of 100; invalid quantities return HTTP 400.",
            "example": 100,
            "format": "int64",
            "minimum": 1,
            "type": "integer"
          },
          "symbol": {
            "description": "Stock symbol.",
            "example": "TSLA",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "qty"
        ],
        "type": "object"
      },
      "ErrorResponse": {
        "description": "API error response.",
        "properties": {
          "message": {
            "example": "Internal Server Error",
            "type": "string"
          }
        },
        "type": "object"
      },
      "Locate": {
        "description": "A locate request and its current lifecycle status.",
        "example": {
          "all_or_none": false,
          "created_at": "2026-01-02T15:04:05Z",
          "expires_at": "2026-01-03T01:00:00Z",
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "limit_price": "0.05",
          "located_price": "0.05",
          "located_qty": 100,
          "requested_qty": 100,
          "status": "active",
          "symbol": "TSLA",
          "total_fee": "5.00"
        },
        "properties": {
          "all_or_none": {
            "description": "Whether the request required the full quantity.",
            "example": false,
            "type": "boolean"
          },
          "created_at": {
            "description": "Time when the locate was created.",
            "example": "2026-01-02T15:04:05Z",
            "format": "date-time",
            "type": "string"
          },
          "expires_at": {
            "description": "Time when the active locate expires. Omitted when rejected.",
            "example": "2026-01-03T01:00:00Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "id": {
            "description": "Locate ID.",
            "example": "550e8400-e29b-41d4-a716-446655440000",
            "format": "uuid",
            "type": "string"
          },
          "limit_price": {
            "description": "Maximum acceptable fee per share from the request.",
            "example": "0.05",
            "type": [
              "string",
              "null"
            ]
          },
          "located_price": {
            "description": "Locate fee per share in USD. Omitted when rejected.",
            "example": "0.05",
            "type": [
              "string",
              "null"
            ]
          },
          "located_qty": {
            "description": "Number of shares located. Omitted when rejected.",
            "example": 100,
            "format": "int64",
            "type": [
              "integer",
              "null"
            ]
          },
          "rejection_reason": {
            "description": "Machine-readable rejection reason.",
            "example": "inventory_unavailable",
            "type": [
              "string",
              "null"
            ]
          },
          "requested_qty": {
            "description": "Number of shares requested.",
            "example": 100,
            "format": "int64",
            "type": "integer"
          },
          "status": {
            "$ref": "#/components/schemas/LocateStatus"
          },
          "symbol": {
            "description": "Stock symbol.",
            "example": "TSLA",
            "type": "string"
          },
          "total_fee": {
            "description": "Total locate fee in USD. Omitted when rejected.",
            "example": "5.00",
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [
          "id",
          "symbol",
          "requested_qty",
          "all_or_none",
          "status",
          "created_at"
        ],
        "type": "object"
      },
      "LocateError": {
        "description": "Locates API error response. Locate-specific 400 and create locate 422 errors include a machine-readable `code`.",
        "properties": {
          "code": {
            "description": "Machine-readable error code. Present on locate-specific 400 and create locate 422 errors.",
            "enum": [
              "invalid_input",
              "invalid_request_body",
              "invalid_limit_price",
              "invalid_symbols",
              "symbol_not_found",
              "security_not_found",
              "insufficient_buying_power",
              "easy_to_borrow",
              "threshold_security",
              "idempotency_key_conflict",
              "quote_unavailable"
            ],
            "example": "invalid_symbols",
            "type": "string"
          },
          "message": {
            "description": "Error message.",
            "example": "symbols must contain at most 100 unique symbols",
            "type": "string"
          }
        },
        "required": [
          "message"
        ],
        "type": "object"
      },
      "LocateStatus": {
        "description": "Locate status.",
        "enum": [
          "active",
          "expired",
          "rejected"
        ],
        "example": "active",
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
    "/v1/locates": {
      "post": {
        "description": "Creates a locate request for a short sale. This endpoint is not available in paper trading.\n\n**Idempotency**: Reusing the same key with the same request returns the original\nlocate response. Reusing the same key with a different request returns HTTP 422.\n",
        "operationId": "createLocates",
        "parameters": [
          {
            "$ref": "#/components/parameters/LegacyIdempotencyKey"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateLocateRequest"
              }
            }
          },
          "description": "Locate request details.",
          "required": true
        },
        "responses": {
          "201": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Locate"
                }
              }
            },
            "description": "Created"
          },
          "400": {
            "content": {
              "application/json": {
                "examples": {
                  "invalid_input": {
                    "value": {
                      "code": "invalid_input",
                      "message": "invalid input: quantity must be in round lots of 100"
                    }
                  },
                  "invalid_limit_price": {
                    "value": {
                      "code": "invalid_limit_price",
                      "message": "invalid limit_price"
                    }
                  },
                  "invalid_request_body": {
                    "value": {
                      "code": "invalid_request_body",
                      "message": "invalid request body"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/LocateError"
                }
              }
            },
            "description": "Invalid locate request."
          },
          "401": {
            "content": {
              "application/json": {
                "example": {
                  "message": "Unauthorized"
                },
                "schema": {
                  "$ref": "#/components/schemas/ErrorResponse"
                }
              }
            },
            "description": "Authentication headers are missing or invalid. Make sure you authenticate your request with a valid API key."
          },
          "403": {
            "content": {
              "application/json": {
                "example": {
                  "message": "Forbidden"
                },
                "schema": {
                  "$ref": "#/components/schemas/ErrorResponse"
                }
              }
            },
            "description": "User has no access to a resource."
          },
          "422": {
            "content": {
              "application/json": {
                "examples": {
                  "easy_to_borrow": {
                    "value": {
                      "code": "easy_to_borrow",
                      "message": "security is easy-to-borrow and does not require a locate"
                    }
                  },
                  "idempotency_key_conflict": {
                    "value": {
                      "code": "idempotency_key_conflict",
                      "message": "idempotency key was already used with a different request"
                    }
                  },
                  "insufficient_buying_power": {
                    "value": {
                      "code": "insufficient_buying_power",
                      "message": "insufficient buying power to cover locate fee"
                    }
                  },
                  "quote_unavailable": {
                    "value": {
                      "code": "quote_unavailable",
                      "message": "locate quote is unavailable for this symbol"
                    }
                  },
                  "symbol_not_found": {
                    "value": {
                      "code": "symbol_not_found",
                      "message": "symbol not found"
                    }
                  },
                  "threshold_security": {
                    "value": {
                      "code": "threshold_security",
                      "message": "security is on the threshold list and cannot be located"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/LocateError"
                }
              }
            },
            "description": "Cannot complete locate request."
          },
          "500": {
            "content": {
              "application/json": {
                "example": {
                  "message": "Internal Server Error"
                },
                "schema": {
                  "$ref": "#/components/schemas/ErrorResponse"
                }
              }
            },
            "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on Slack or on the Community Forum."
          }
        },
        "summary": "Create Locate",
        "tags": [
          "Locates"
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
      "description": "Endpoints for locate requests and quotes.",
      "name": "Locates"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```