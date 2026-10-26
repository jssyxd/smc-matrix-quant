# Get a single JIT settlement

Source: https://docs.alpaca.markets/us/reference/get-v1-jit-settlements-single.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get a single JIT settlement

Returns the JIT settlement specified by the path parameter.

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
      "JITAssetClass": {
        "description": "Values:\n * `crypto`: Used to identify a crypto only account\n * `us_equity`: Used to identify an account that trades US equities, or both crypto and\n  US equities.\n",
        "enum": [
          "crypto",
          "us_equity"
        ],
        "type": "string"
      },
      "SettlementResponse": {
        "description": "A settlement response, either from creation or retrieval\n",
        "properties": {
          "additional_info": {
            "type": "string"
          },
          "asset_class": {
            "$ref": "#/components/schemas/JITAssetClass"
          },
          "completed_at": {
            "format": "date-time",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "The currency of the settlement. Only applicable to JIT settlements.\n",
            "type": "string"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "interest_amount": {
            "description": "The total interest amount accrued on the transfers included in this settlement. Only applicable for instant funding settlements.\n",
            "format": "decimal",
            "type": "string"
          },
          "reason": {
            "description": "The reason for failure, if applicable\n",
            "type": "string"
          },
          "source_account_number": {
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/SettlementStatus"
          },
          "total_amount": {
            "format": "decimal",
            "type": "string"
          },
          "updated_at": {
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "id",
          "total_amount",
          "status",
          "created_at",
          "updated_at"
        ],
        "type": "object"
      },
      "SettlementStatus": {
        "description": "Values:\n * `PENDING`: Created and waiting to be processed\n * `AWAITING_ADDITIONAL_FUNDS`: Waiting for additional funds to be deposited\n * `COMPLETED`: All transactions are reconciled\n * `FAILED`: Attempt to process this settlement has failed. If this is observed\n  additional remittance information may be required, or one of the transfers being settled\n  accrued additional interest since the settlement was created.\n",
        "enum": [
          "PENDING",
          "AWAITING_ADDITIONAL_FUNDS",
          "COMPLETED",
          "FAILED"
        ],
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
    "/v1/jit/settlements/{settlement_id}": {
      "get": {
        "description": "Returns the JIT settlement specified by the path parameter.",
        "operationId": "get-v1-jit-settlements-single",
        "parameters": [
          {
            "description": "ID of the JIT settlement",
            "in": "path",
            "name": "settlement_id",
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
                "schema": {
                  "$ref": "#/components/schemas/SettlementResponse"
                }
              }
            },
            "description": "Successful response."
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
        "summary": "Get a single JIT settlement",
        "tags": [
          "Funding"
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```