# Retrieve ACH Relationships for an account

Source: https://docs.alpaca.markets/us/reference/getaccountachrelationships.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve ACH Relationships for an account

Returns a list of ACH Relationships for an account

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
      "ACHRelationship": {
        "properties": {
          "account_id": {
            "format": "uuid",
            "type": "string"
          },
          "account_owner_name": {
            "description": "Name of the account owner",
            "minLength": 1,
            "type": "string"
          },
          "bank_account_number": {
            "minLength": 1,
            "type": "string"
          },
          "bank_account_type": {
            "description": "Must be CHECKING or SAVINGS",
            "enum": [
              "CHECKING",
              "SAVINGS"
            ],
            "minLength": 1,
            "type": "string"
          },
          "bank_routing_number": {
            "minLength": 1,
            "type": "string"
          },
          "created_at": {
            "description": "Format: 2020-01-01T01:01:01Z",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "nickname": {
            "minLength": 1,
            "type": "string"
          },
          "status": {
            "enum": [
              "QUEUED",
              "APPROVED",
              "REJECTED",
              "PENDING",
              "CANCEL_REQUESTED"
            ],
            "type": "string"
          },
          "updated_at": {
            "description": "Format: 2020-01-01T01:01:01Z",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "id",
          "created_at",
          "updated_at",
          "account_id",
          "status",
          "account_owner_name"
        ],
        "title": "ACHRelationship",
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
    "/v1/accounts/{account_id}/ach_relationships": {
      "get": {
        "description": "Returns a list of ACH Relationships for an account",
        "operationId": "getAccountACHRelationships",
        "parameters": [
          {
            "description": "Comma-separated status values",
            "in": "query",
            "name": "statuses",
            "schema": {
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
                    "$ref": "#/components/schemas/ACHRelationship"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Success"
          }
        },
        "summary": "Retrieve ACH Relationships for an account",
        "tags": [
          "Funding"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```