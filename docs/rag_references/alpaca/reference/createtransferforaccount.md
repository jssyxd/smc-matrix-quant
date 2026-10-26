# Request a New Transfer

Source: https://docs.alpaca.markets/us/reference/createtransferforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Request a New Transfer

Create a new transfer to deposit money into or withdraw money from an account.

Two `transfer_type` values are accepted, and both are available in sandbox and production:

- **`ach`** — supports both `INCOMING` (deposit) and `OUTGOING` (withdrawal) directions. A `relationship_id` from a previously created [ACH Relationship](https://docs.alpaca.markets/reference/createachrelationshipforaccount) is required.
- **`wire`** — supports the `OUTGOING` (withdrawal) direction only. Incoming wires cannot be initiated through this endpoint; they are pushed in by the sending bank and recorded automatically. A `bank_id` from a previously created [Bank Relationship](https://docs.alpaca.markets/reference/createrecipientbank) is required, and the bank must be in `APPROVED` status before the transfer will progress past `QUEUED`.

In the sandbox environment, ACH deposits and withdrawals settle instantly against virtual funds. Outgoing wire withdrawals are accepted and simulated end-to-end — no funds are transmitted to a bank, but the transfer progresses to `COMPLETE` and the account is debited against virtual funds. Sandbox wire withdrawals are asynchronous (not instant) and auto-complete on weekdays only; transfers submitted on a weekend will not progress until Monday. For more on funding accounts in sandbox, see [this tutorial](https://alpaca.markets/learn/fund-broker-api/).

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
      "CreateTransferRequest": {
        "description": "[See main docs here](https://alpaca.markets/docs/api-references/broker-api/funding/transfers/#creating-a-transfer-entity)",
        "properties": {
          "additional_information": {
            "description": "Additional details for when type = `wire`",
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
            "description": "Required if type = `wire`\n\nThe bank_relationship created for the account_id [here](https://alpaca.markets/docs/api-references/broker-api/funding/bank/#creating-a-new-bank-relationship)",
            "format": "uuid",
            "type": "string"
          },
          "direction": {
            "$ref": "#/components/schemas/TransferDirection"
          },
          "fee_payment_method": {
            "$ref": "#/components/schemas/FeePaymentMethod"
          },
          "ira": {
            "$ref": "#/components/schemas/TransferIRA"
          },
          "relationship_id": {
            "description": "Required if type = `ach`\n\nThe ach_relationship created for the account_id [here](https://alpaca.markets/docs/api-references/broker-api/funding/ach/#creating-an-ach-relationship)",
            "format": "uuid",
            "type": "string"
          },
          "transfer_type": {
            "$ref": "#/components/schemas/TransferType"
          }
        },
        "required": [
          "transfer_type",
          "amount",
          "direction"
        ],
        "title": "CreateTransferRequest",
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
      "FeePaymentMethod": {
        "description": "Only outgoing wire fees are currently supported for automated processing.\n\n\n**user**\tThe end user will pay any applicable fees\n**invoice**\tAny applicable fees will be billed to the client in the following monthly invoice",
        "title": "FeePaymentMethod",
        "type": "string"
      },
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
      "TransferIRA": {
        "description": "This field is used for IRA Account only",
        "properties": {
          "distribution_reason": {
            "example": "normal",
            "type": "string"
          },
          "tax_withholding": {
            "$ref": "#/components/schemas/TransferIRATaxWithholding"
          },
          "tax_year": {
            "example": "2024",
            "type": "string"
          }
        },
        "type": "object"
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
      "TransferIRATaxWithholding": {
        "properties": {
          "fed_pct": {
            "example": "10.25",
            "type": "string"
          },
          "state_pct": {
            "example": "8.25",
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
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        }
      ],
      "post": {
        "description": "Create a new transfer to deposit money into or withdraw money from an account.\n\nTwo `transfer_type` values are accepted, and both are available in sandbox and production:\n\n- **`ach`** — supports both `INCOMING` (deposit) and `OUTGOING` (withdrawal) directions. A `relationship_id` from a previously created [ACH Relationship](https://docs.alpaca.markets/reference/createachrelationshipforaccount) is required.\n- **`wire`** — supports the `OUTGOING` (withdrawal) direction only. Incoming wires cannot be initiated through this endpoint; they are pushed in by the sending bank and recorded automatically. A `bank_id` from a previously created [Bank Relationship](https://docs.alpaca.markets/reference/createrecipientbank) is required, and the bank must be in `APPROVED` status before the transfer will progress past `QUEUED`.\n\nIn the sandbox environment, ACH deposits and withdrawals settle instantly against virtual funds. Outgoing wire withdrawals are accepted and simulated end-to-end — no funds are transmitted to a bank, but the transfer progresses to `COMPLETE` and the account is debited against virtual funds. Sandbox wire withdrawals are asynchronous (not instant) and auto-complete on weekdays only; transfers submitted on a weekend will not progress until Monday. For more on funding accounts in sandbox, see [this tutorial](https://alpaca.markets/learn/fund-broker-api/).",
        "operationId": "createTransferForAccount",
        "parameters": [
          {
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateTransferRequest"
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
                  "$ref": "#/components/schemas/Transfer"
                }
              }
            },
            "description": "Successfully requested a transfer."
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request body is malformed (e.g. invalid JSON)."
          },
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The account is not permitted to perform this transfer. Examples include:\n\n- `deposits are not permitted for this account` — the account's `depositable_status` is not `allowed` / `limited`.\n- `withdrawals are not permitted for this account` — the account's `withdrawable_status` is not `allowed` / `limited`.\n"
          },
          "422": {
            "content": {
              "application/json": {
                "examples": {
                  "wireIncomingRejected": {
                    "summary": "Wire transfer with direction = INCOMING",
                    "value": {
                      "code": 40010001,
                      "message": "cannot submit incoming wire transfer using this API"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request was rejected by validation. Common reasons include:\n\n- `cannot submit incoming wire transfer using this API` — sent `transfer_type: wire` with `direction: INCOMING`. Incoming wires cannot be initiated through this endpoint.\n- `invalid relationship_id` / `bank_id required for wire transfer` — missing the required relationship/bank identifier for the chosen `transfer_type`.\n- `bank_id should be empty for ach transfer` / `relationship_id should be empty for wire transfer` — provided the wrong identifier for the chosen `transfer_type`.\n- `only wire transfer type can provide additional information for the transfer` — `additional_information` was supplied on a non-wire request.\n- `amount must be greater than 0.00` / `deposit amount must be greater than or equal to <min>` / `withdrawal amount must be greater than <min>` — amount fails the minimum-amount checks.\n- `transfer_type must be either ach or wire` / `direction must be either incoming or outgoing` — invalid enum values.\n"
          }
        },
        "summary": "Request a New Transfer",
        "tags": [
          "Funding",
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
    },
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