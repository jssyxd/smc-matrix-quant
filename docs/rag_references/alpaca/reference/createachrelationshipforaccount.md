# Create an ACH Relationship

Source: https://docs.alpaca.markets/us/reference/createachrelationshipforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create an ACH Relationship

Create a new ACHRelationship for an account

If successful, will return 200 code with a newly created ACH Relationship entity.

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
    "responses": {
      "BadRequest": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "Malformed input."
      },
      "NotAuthorized": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "Client is not authorized for this operation."
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
      },
      "CreateACHRelationshipRequest": {
        "description": "Represents the fields used in creation of a new ACHRelationship.\n\nYou can create an ACHRelationship by passing the required fields here or if you have an account with Plaid you can use our integration with Plaid to create a relationship.\n\nPlease see the documentation [here](https://alpaca.markets/docs/api-references/broker-api/funding/ach/#plaid-integration-for-bank-transfers) for more info on using Plaid with Alpaca",
        "properties": {
          "account_owner_name": {
            "minLength": 1,
            "type": "string"
          },
          "bank_account_number": {
            "description": "In sandbox, this still must be a valid format",
            "minLength": 1,
            "type": "string"
          },
          "bank_account_type": {
            "description": "Must be `CHECKING` or `SAVINGS`",
            "enum": [
              "CHECKING",
              "SAVINGS"
            ],
            "minLength": 1,
            "type": "string"
          },
          "bank_routing_number": {
            "description": "In sandbox, this still must be a valid format",
            "minLength": 1,
            "type": "string"
          },
          "instant": {
            "type": "boolean"
          },
          "nickname": {
            "minLength": 1,
            "type": "string"
          },
          "processor_token": {
            "description": "If using Plaid, you can specify a Plaid processor token here ",
            "type": "string"
          }
        },
        "required": [
          "account_owner_name",
          "bank_account_type",
          "bank_account_number",
          "bank_routing_number"
        ],
        "title": "CreateACHRelationshipRequest",
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
    "/v1/accounts/{account_id}/ach_relationships": {
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        }
      ],
      "post": {
        "description": "Create a new ACHRelationship for an account\n\nIf successful, will return 200 code with a newly created ACH Relationship entity.",
        "operationId": "createACHRelationshipForAccount",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateACHRelationshipRequest"
              }
            }
          },
          "description": "Create ACH Relationship ",
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ACHRelationship"
                }
              }
            },
            "description": "returns the newly created ACH Relationship entity."
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/NotAuthorized"
          },
          "409": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The account already has an active relationship."
          }
        },
        "summary": "Create an ACH Relationship",
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