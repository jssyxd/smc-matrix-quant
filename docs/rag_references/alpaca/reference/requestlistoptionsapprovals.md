# Retrieve options level approval requests (BETA)

Source: https://docs.alpaca.markets/us/reference/requestlistoptionsapprovals.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve options level approval requests (BETA)

This endpoint retrieves options trading level approval requests. Query parameters can be specified to filter the results. If multiple query parameters are specified, the results will be filtered to include only those that match all of the specified parameters. Each query parameter can only be specified once.

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "PageToken": {
        "description": "Used for pagination, this token retrieves the next page of results. It is obtained from the response of the preceding page when additional pages are available.",
        "in": "query",
        "name": "page_token",
        "required": false,
        "schema": {
          "example": "MA==",
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
      "NextPageToken": {
        "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
        "example": "MTAwMA==",
        "type": [
          "string",
          "null"
        ]
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
      },
      "OptionsApprovalsList": {
        "description": "A list of options approval requests.",
        "properties": {
          "next_page_token": {
            "$ref": "#/components/schemas/NextPageToken"
          },
          "options_approvals": {
            "description": "An array of options approval requests.",
            "items": {
              "$ref": "#/components/schemas/OptionsApprovalResponse"
            },
            "type": "array"
          }
        },
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
    "/v1/accounts/options/approvals": {
      "get": {
        "description": "This endpoint retrieves options trading level approval requests. Query parameters can be specified to filter the results. If multiple query parameters are specified, the results will be filtered to include only those that match all of the specified parameters. Each query parameter can only be specified once.",
        "operationId": "requestListOptionsApprovals",
        "parameters": [
          {
            "description": "Only return results for the specified account.",
            "in": "query",
            "name": "account_id",
            "schema": {
              "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "requested_level",
            "schema": {
              "description": "Only return requests with the specified requested level.\n0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
              "enum": [
                0,
                1,
                2,
                3
              ],
              "example": 3,
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "approved_level",
            "schema": {
              "description": "Only return requests with the specified approved level.\n0=Disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
              "enum": [
                0,
                1,
                2,
                3
              ],
              "example": 3,
              "type": "integer"
            }
          },
          {
            "description": "Only return requests with the specified approval request status.",
            "in": "query",
            "name": "status",
            "schema": {
              "$ref": "#/components/schemas/OptionsApprovalStatus"
            }
          },
          {
            "description": "The maximum number of results to return. The default (and maximum value) is 1000.",
            "in": "query",
            "name": "page_size",
            "schema": {
              "default": 1000,
              "maximum": 1000,
              "minimum": 1,
              "type": "integer"
            }
          },
          {
            "$ref": "#/components/parameters/PageToken"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OptionsApprovalsList"
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
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The correspondent entity does not have access to options approvals or the account does not exist.\n"
          }
        },
        "summary": "Retrieve options level approval requests (BETA)",
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