# Create an instant funding request

Source: https://docs.alpaca.markets/us/reference/post-v1-instant-funding.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create an instant funding request

Creates an instant funding request. The request will be processed and the funds will be
made available to the account in the form of a Memopost non trade activity. Upon settlement
the Memoposted will be corrected to a CSD activity.

**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is
idempotent. Multiple requests with the same key and identical request body will
create only one transfer. A subsequent request returns the previously created
transfer with the same response (no duplicate is created). If the same key is used
with a different request body, the API returns `422 Unprocessable Entity`.

**Recommended for production**: Always supply `Idempotency-Key` when creating
transfers. This allows safe retries on timeouts, network errors, or 5xx responses
without risking duplicate transfers. Use a client-generated unique value (e.g. UUID).


Creates an instant funding request. The request will be processed and the funds will be made available to the account in the form of a Memopost non trade activity. Upon settlement the Memoposted will be corrected to a CSD activity.

**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is idempotent. Multiple requests with the same key and identical request body will create only one transfer. A subsequent request returns the previously created transfer with the same response (no duplicate is created). If the same key is used with a different request body, the API returns `422 Unprocessable Entity`.

**Recommended for production**: Always supply `Idempotency-Key` when creating transfers. This allows safe retries on timeouts, network errors, or 5xx responses without risking duplicate transfers. Use a client-generated unique value (e.g. UUID).

**Formatting:** Amount must have a maximum of 2 decimal places. If your system currently generates amounts with more precision, please update your logic to round to 2 decimals.

***

<br />

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
      "CreateIFTransferRequest": {
        "description": "Request to create a new instant funding transfer\n",
        "properties": {
          "account_no": {
            "type": "string"
          },
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "source_account_no": {
            "type": "string"
          }
        },
        "required": [
          "account_no",
          "source_account_no",
          "amount"
        ],
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
      },
      "IFFee": {
        "properties": {
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "type": {
            "$ref": "#/components/schemas/IFFeeType"
          }
        },
        "required": [
          "id",
          "amount",
          "type"
        ],
        "type": "object"
      },
      "IFFeeType": {
        "description": "Status:\n * `partner`: The fee on a transfer that was allocated to the partner\n * `alpaca`: The fee on a transfer that was allocated to Alpaca\n",
        "enum": [
          "partner",
          "alpaca"
        ],
        "type": "string"
      },
      "InstantFunding": {
        "properties": {
          "account_no": {
            "type": "string"
          },
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "deadline": {
            "format": "date",
            "type": "string"
          },
          "fees": {
            "items": {
              "$ref": "#/components/schemas/IFFee"
            },
            "type": "array"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "interests": {
            "items": {
              "$ref": "#/components/schemas/Interest"
            },
            "type": "array"
          },
          "remaining_payable": {
            "format": "decimal",
            "type": "string"
          },
          "source_account_no": {
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/InstantFundingStatus"
          },
          "system_date": {
            "format": "date",
            "type": "string"
          },
          "total_interest": {
            "format": "decimal",
            "type": "string"
          }
        },
        "required": [
          "id",
          "amount",
          "account_no",
          "source_account_no",
          "status",
          "system_date",
          "deadline",
          "created_at",
          "total_interest",
          "remaining_payable",
          "interests",
          "fees"
        ],
        "type": "object"
      },
      "InstantFundingStatus": {
        "description": "Status:\n * `PENDING`: Created and waiting to be processed\n * `CANCELED`: Canceled\n * `EXECUTED`: All fees (including Partner fee) are transacted\n * `FAILED`: Failed mostly due to technical reasons\n * `COMPLETED`: All transactions are settled\n",
        "enum": [
          "PENDING",
          "CANCELED",
          "EXECUTED",
          "FAILED",
          "COMPLETED"
        ],
        "type": "string"
      },
      "Interest": {
        "properties": {
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "date": {
            "format": "date",
            "type": "string"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "reconciled_at": {
            "format": "date-time",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/InstantFundingStatus"
          }
        },
        "required": [
          "id",
          "date",
          "amount",
          "status",
          "created_at",
          "reconciled_at"
        ],
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
    "/v1/instant_funding": {
      "post": {
        "description": "Creates an instant funding request. The request will be processed and the funds will be\nmade available to the account in the form of a Memopost non trade activity. Upon settlement\nthe Memoposted will be corrected to a CSD activity.\n\n**Idempotency**: When the `Idempotency-Key` header is supplied, this endpoint is\nidempotent. Multiple requests with the same key and identical request body will\ncreate only one transfer. A subsequent request returns the previously created\ntransfer with the same response (no duplicate is created). If the same key is used\nwith a different request body, the API returns `422 Unprocessable Entity`.\n\n**Recommended for production**: Always supply `Idempotency-Key` when creating\ntransfers. This allows safe retries on timeouts, network errors, or 5xx responses\nwithout risking duplicate transfers. Use a client-generated unique value (e.g. UUID).\n",
        "operationId": "post-v1-instant-funding",
        "parameters": [
          {
            "$ref": "#/components/parameters/LegacyIdempotencyKey"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateIFTransferRequest"
              }
            }
          },
          "description": "details of the instant funding request",
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/InstantFunding"
                }
              }
            },
            "description": "Instant transfer request created."
          },
          "422": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Unprocessable Entity. Returned when an idempotency key is reused with a different request body."
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Error response."
          }
        },
        "summary": "Create an instant funding request",
        "tags": [
          "Instant Funding"
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
      "name": "Instant Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```