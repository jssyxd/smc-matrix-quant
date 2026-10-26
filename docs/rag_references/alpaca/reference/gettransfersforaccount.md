# Retrieve List of Transfers for an Account.

Source: https://docs.alpaca.markets/us/reference/gettransfersforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve List of Transfers for an Account.

You can query a list of transfers for an account.


You can filter requested transfers by values such as direction and status.

Returns a list of transfer entities ordered by created_at


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
      "Transfer": {
        "description": "Transfers allow you to transfer money/balance into your end customers' account (deposits) or out (withdrawal).\n\n[Main docs here](https://alpaca.markets/docs/api-references/broker-api/funding/transfers/#the-transfer-object)",
        "examples": [
          {
            "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
            "additional_information": "string",
            "amount": "string",
            "bank_id": "f1ae96de-94c1-468e-93a3-6b7213930ca8",
            "created_at": "2019-08-24T14:15:22Z",
            "direction": "INCOMING",
            "expires_at": "2019-08-24T14:15:22Z",
            "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
            "ira": {
              "distribution_reason": "normal",
              "fed_withholding_amount": "102.5",
              "fed_withholding_pct": "10.25",
              "state_withholding_amount": "97.5",
              "state_withholding_pct": "9.75",
              "tax_year": "2024"
            },
            "reason": "string",
            "relationship_id": "81412018-ffa2-43f9-a3eb-d39f1c5e0f87",
            "status": "QUEUED",
            "type": "ach",
            "updated_at": "2019-08-24T14:15:22Z"
          }
        ],
        "properties": {
          "account_id": {
            "description": "The account ID",
            "format": "uuid",
            "type": "string"
          },
          "additional_information": {
            "description": "Additional information. Only applies when type = \"wire\".",
            "type": [
              "string",
              "null"
            ]
          },
          "amount": {
            "description": "Must be > 0.00",
            "format": "decimal",
            "type": "string"
          },
          "bank_id": {
            "description": "The ID of the Bank, only present if type = \"wire\"",
            "format": "uuid",
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp when transfer was created",
            "format": "date-time",
            "type": "string"
          },
          "direction": {
            "$ref": "#/components/schemas/TransferDirection"
          },
          "expires_at": {
            "description": "Timestamp when transfer expires",
            "format": "date-time",
            "type": "string"
          },
          "fee": {
            "description": "Fee amount to be collected. Only applies when type = \"wire\".",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "fee_payment_method": {
            "description": "Either \"user\" or \"invoice\". Only applies when type = \"wire\".",
            "type": [
              "string",
              "null"
            ]
          },
          "hold_until": {
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "The transfer ID",
            "format": "uuid",
            "type": "string"
          },
          "instant_amount": {
            "type": "string"
          },
          "ira": {
            "$ref": "#/components/schemas/TransferIRADetails"
          },
          "reason": {
            "description": "Cause of the status",
            "type": [
              "string",
              "null"
            ]
          },
          "relationship_id": {
            "description": "The ACH relationship ID only present if type = \"ach\"",
            "format": "uuid",
            "type": "string"
          },
          "requested_amount": {
            "description": "Must be > 0.00. Only applies when type = \"wire\".",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "status": {
            "$ref": "#/components/schemas/TransferStatus"
          },
          "type": {
            "$ref": "#/components/schemas/TransferType"
          },
          "updated_at": {
            "description": "Timestamp when transfer was updated",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "id",
          "account_id",
          "type",
          "status",
          "amount",
          "direction",
          "created_at"
        ],
        "title": "Transfer",
        "type": "object"
      },
      "TransferDirection": {
        "description": "- **INCOMING**\nFunds incoming to user's account (deposit).\n- **OUTGOING**\nFunds outgoing from user's account (withdrawal).\n",
        "enum": [
          "INCOMING",
          "OUTGOING"
        ],
        "example": "INCOMING",
        "type": "string"
      },
      "TransferIRADetails": {
        "properties": {
          "distribution_reason": {
            "example": "normal",
            "type": "string"
          },
          "fed_withholding_amount": {
            "example": "102.5",
            "type": "string"
          },
          "fed_withholding_pct": {
            "example": "10.25",
            "type": "string"
          },
          "state_withholding_amount": {
            "example": "97.5",
            "type": "string"
          },
          "state_withholding_pct": {
            "example": "9.75",
            "type": "string"
          },
          "tax_year": {
            "example": "2024",
            "type": "string"
          }
        },
        "type": "object"
      },
      "TransferStatus": {
        "description": "- **QUEUED**\nTransfer is in queue to be processed.\n- **APPROVAL_PENDING**\nTransfer is pending approval.\n- **PENDING**\nTransfer is pending processing.\n- **SENT_TO_CLEARING**\nTransfer is being processed by the clearing firm.\n- **REJECTED**\nTransfer is rejected.\n- **CANCELED**\nClient initiated transfer cancellation.\n- **APPROVED**\nTransfer is approved.\n- **COMPLETE**\nTransfer is completed.\n- **RETURNED**\nThe bank issued an ACH return for the transfer.\n",
        "enum": [
          "QUEUED",
          "APPROVAL_PENDING",
          "PENDING",
          "SENT_TO_CLEARING",
          "REJECTED",
          "CANCELED",
          "APPROVED",
          "COMPLETE",
          "RETURNED"
        ],
        "example": "QUEUED",
        "type": "string"
      },
      "TransferType": {
        "description": "- **ach**\nTransfer via ACH (US Only). Supports both `INCOMING` (deposit) and `OUTGOING` (withdrawal) directions.\n- **wire**\nTransfer via wire. `OUTGOING` (withdrawal) only.\n",
        "enum": [
          "ach",
          "wire"
        ],
        "example": "ach",
        "title": "TransferType",
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
    "/v1/accounts/{account_id}/transfers": {
      "get": {
        "description": "You can query a list of transfers for an account.\n\n\nYou can filter requested transfers by values such as direction and status.\n\nReturns a list of transfer entities ordered by created_at\n",
        "operationId": "getTransfersForAccount",
        "parameters": [
          {
            "description": "INCOMING or OUTGOING",
            "in": "query",
            "name": "direction",
            "schema": {
              "enum": [
                "INCOMING",
                "OUTGOING"
              ],
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "limit",
            "schema": {
              "format": "int32",
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "offset",
            "schema": {
              "format": "int32",
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "example-1": {
                    "value": [
                      {
                        "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
                        "additional_information": "string",
                        "amount": "string",
                        "bank_id": "f1ae96de-94c1-468e-93a3-6b7213930ca8",
                        "created_at": "2019-08-24T14:15:22Z",
                        "direction": "INCOMING",
                        "expires_at": "2019-08-24T14:15:22Z",
                        "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                        "ira": {
                          "distribution_reason": "normal",
                          "fed_withholding_amount": "102.5",
                          "fed_withholding_pct": "10.25",
                          "state_withholding_amount": "97.5",
                          "state_withholding_pct": "9.75",
                          "tax_year": "2024"
                        },
                        "reason": "string",
                        "relationship_id": "81412018-ffa2-43f9-a3eb-d39f1c5e0f87",
                        "status": "QUEUED",
                        "type": "ach",
                        "updated_at": "2019-08-24T14:15:22Z"
                      }
                    ]
                  },
                  "example-2": {
                    "value": [
                      {
                        "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
                        "additional_information": "string",
                        "amount": "string",
                        "bank_id": "f1ae96de-94c1-468e-93a3-6b7213930ca8",
                        "created_at": "2019-08-24T14:15:22Z",
                        "direction": "INCOMING",
                        "expires_at": "2019-08-24T14:15:22Z",
                        "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                        "ira": {
                          "distribution_reason": "normal",
                          "fed_withholding_amount": "102.5",
                          "fed_withholding_pct": "10.25",
                          "state_withholding_amount": "97.5",
                          "state_withholding_pct": "9.75",
                          "tax_year": "2024"
                        },
                        "reason": "string",
                        "relationship_id": "81412018-ffa2-43f9-a3eb-d39f1c5e0f87",
                        "status": "QUEUED",
                        "type": "ach",
                        "updated_at": "2019-08-24T14:15:22Z"
                      }
                    ]
                  }
                },
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Transfer"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Success."
          }
        },
        "summary": "Retrieve List of Transfers for an Account.",
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