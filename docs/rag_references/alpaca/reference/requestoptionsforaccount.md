# Request options trading for an account (BETA)

Source: https://docs.alpaca.markets/us/reference/requestoptionsforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Request options trading for an account (BETA)

This endpoint requests options trading for an account.
Following submission, an assigned administrator will review the request.
Upon approval, the account's options_approved_level parameter will be modified, granting the account the ability to participate in options trading.
Note: This endpoint is only available for partners who have been enabled for Options BETA.

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
      "OptionsApprovalRequest": {
        "properties": {
          "level": {
            "description": "The desired option trading level. 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
            "enum": [
              1,
              2,
              3
            ],
            "example": 3,
            "type": "integer"
          }
        },
        "type": "object"
      },
      "OptionsApprovalResponse": {
        "properties": {
          "account_id": {
            "description": "The account ID.",
            "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
            "format": "uuid",
            "type": "string"
          },
          "approved_level": {
            "description": "The option trading level approved for this request. Only present once the request has completed processiing.\nNote that a subsequent request may be approved for a different level.\n0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\"\n",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "example": 3,
            "type": "integer"
          },
          "created_at": {
            "description": "The time when the request was submitted.",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "The request ID.",
            "example": "88b5f678-fef5-447b-af15-f21e367e6d8c",
            "format": "uuid",
            "type": "string"
          },
          "requested_level": {
            "description": "The request option trading level. 0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "example": 3,
            "type": "integer"
          },
          "requester": {
            "description": "The requester of the options approval request.",
            "enum": [
              "CORRESPONDENT",
              "ALPACA_ADMIN"
            ],
            "example": "CORRESPONDENT",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/OptionsApprovalStatus"
          },
          "updated_at": {
            "description": "The time when the request was last updated.",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          }
        },
        "type": "object"
      },
      "OptionsApprovalStatus": {
        "description": "The request status.\n- PENDING: The request is under review.\n- APPROVED: The request has been successfully approved, the account is now able to trade options.\n- LOWER_LEVEL_APPROVED: The request has been approved for a level lower than the requested one.\n- REJECTED: The request has been rejected.\n",
        "enum": [
          "PENDING",
          "APPROVED",
          "LOWER_LEVEL_APPROVED",
          "REJECTED"
        ],
        "example": "PENDING",
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
    "/v1/accounts/{account_id}/options/approval": {
      "post": {
        "description": "This endpoint requests options trading for an account.\nFollowing submission, an assigned administrator will review the request.\nUpon approval, the account's options_approved_level parameter will be modified, granting the account the ability to participate in options trading.\nNote: This endpoint is only available for partners who have been enabled for Options BETA.",
        "operationId": "requestOptionsForAccount",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OptionsApprovalRequest"
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
                  "$ref": "#/components/schemas/OptionsApprovalResponse"
                }
              }
            },
            "description": "The request was submitted successfully."
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request body is invalid."
          },
          "401": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Client does not exist, you do not have access to the client, or \"client_secret\" is incorrect.\n"
          },
          "422": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request body did not pass all validations."
          }
        },
        "summary": "Request options trading for an account (BETA)",
        "tags": [
          "Accounts"
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
      "name": "Accounts"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```