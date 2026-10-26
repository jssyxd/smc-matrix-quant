# Get instant funding report

Source: https://docs.alpaca.markets/us/reference/get-v1-instant-funding-reports.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get instant funding report

Returns instant funding reports which are to be used for daily reconciliation reporting.

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
      },
      "ReportsResponse": {
        "properties": {
          "account_no": {
            "type": "string"
          },
          "deadline": {
            "format": "date",
            "type": "string"
          },
          "instant_funding_transfers": {
            "items": {
              "$ref": "#/components/schemas/InstantFunding"
            },
            "type": "array"
          },
          "system_date": {
            "format": "date",
            "type": "string"
          },
          "total_amount_owed": {
            "format": "decimal",
            "type": "string"
          },
          "total_interest_penalty": {
            "format": "decimal",
            "type": "string"
          }
        },
        "required": [
          "system_date",
          "account_no",
          "total_amount_owed",
          "total_interest_penalty",
          "deadline"
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
    "/v1/instant_funding/reports": {
      "get": {
        "description": "Returns instant funding reports which are to be used for daily reconciliation reporting.",
        "operationId": "get-v1-instant-funding-reports",
        "parameters": [
          {
            "description": "The report type to be returned; 'summary' or 'detail', defaults to 'summary'",
            "in": "query",
            "name": "report_type",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The system date to be used for the report. If not provided then the last system date will be used.\n",
            "in": "query",
            "name": "system_date",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/ReportsResponse"
                  },
                  "type": "array"
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
        "summary": "Get instant funding report",
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