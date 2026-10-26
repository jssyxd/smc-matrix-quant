# List transfers for an account

Source: https://docs.alpaca.markets/us/reference/listacatstransfersbyaccount.md

---
updatedAt: 2026-06-23T06:50:20.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List transfers for an account

List all incoming and outgoing transfers where the account was one of the parties. The list may include transfers not initiated using this API. By default, the response includes all transfers for the account for backwards compatibility. To paginate results, provide the `limit` query parameter and use the `page_token` value returned in the response to continue listing transfers.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AcatsAccountType": {
        "description": "Account type, as represented by DTCC",
        "enum": [
          "AGENCY",
          "BANK_CUSTODY",
          "BENEFICIARY",
          "BENEFICIARY_ROTH_IRA",
          "CORPORATE",
          "CO_TRUSTEE",
          "COVERDELL_IRA",
          "CUSTODIAN_UGMA",
          "DIRECT_ROLLOVER",
          "ESTATE",
          "HSA",
          "IRA",
          "JOINT",
          "MEDICAL_SAVINGS_ACCOUNT",
          "OTHER",
          "QUALIFIED_OR_PROFIT_SHARING_OR_PENSION",
          "ROTH_401K",
          "ROTH_IRA",
          "ROTH_SEP",
          "ROTH_SIMPLE",
          "ROTH_SOLO_401K",
          "SARSEP",
          "SEP_IRA",
          "SIMPLE_IRA",
          "SINGLE",
          "SOLO_401K",
          "TRUST",
          "TYPE_401K",
          "TYPE_403B",
          "TYPE_457_PLAN",
          "TYPE_529_PLAN"
        ],
        "type": "string"
      },
      "AcatsContraBrokerType": {
        "description": "ACATS participant type",
        "enum": [
          "BANK",
          "BROKER"
        ],
        "type": "string"
      },
      "AcatsDtccStatus": {
        "description": "Transfer status as tracked by DTCC",
        "enum": [
          "REQUEST",
          "REQUEST_ADJUST",
          "REQUEST_ADJUST_PAST",
          "REQUEST_PAST",
          "REQUEST_REJECT",
          "REVIEW",
          "REVIEW_ADJUST_DELIVERER",
          "REVIEW_ERROR",
          "REVIEW_ACCELERATE",
          "REVIEW_ADJUST_RECEIVER_ACCELERATE",
          "SETTLE_PREP",
          "SETTLE_CLOSE",
          "CLOSE_PURGE",
          "REQUEST_PTR",
          "MEMO_PURGE_PARTIAL_TRANSFER_REQUEST_RECEIVER",
          "REJECT",
          "SYSTEM_REJECTED"
        ],
        "type": "string"
      },
      "AcatsDtccTransferType": {
        "description": "ACATS transfer type",
        "enum": [
          "FUL",
          "FRV",
          "MFC",
          "PTD",
          "PTR",
          "RCL",
          "RCR",
          "PTF"
        ],
        "type": "string"
      },
      "AcatsError": {
        "description": "Body for responses with HTTP status codes indicating an error",
        "example": {
          "message": "contra broker number is required"
        },
        "properties": {
          "message": {
            "type": "string"
          }
        },
        "required": [
          "message"
        ],
        "type": "object"
      },
      "AcatsListTransfersResponse": {
        "description": "A page of ACATS transfers, with optional pagination tokens.",
        "example": {
          "page_token_next": "eyJjcmVhdGVkX2F0IjoiMjAyNi0wNC0yOFQxNDozMDowMFoiLCJpZCI6IjAxQUJDIn0=",
          "pending_transfers": 37,
          "transfers": [
            {
              "acats_id": "2c827687-ddd3-4ad9-bee8-0a3cdad35301",
              "account_id": "9ac16d7d-1f6e-445b-8e51-807e77ba2902",
              "account_name": "John Doe",
              "account_number": "12345678",
              "account_type": "SINGLE",
              "contra_account_number": "A00000123",
              "contra_broker_name": "Alpaca Clearing",
              "contra_broker_number": "00001234",
              "contra_broker_type": "BANK",
              "created_at": "2026-04-21T12:41:03.505862Z",
              "direction": "INCOMING",
              "ip_address": "203.0.113.42",
              "rejection_details": {
                "rejection_message": "SS# Tax ID Mismatch",
                "rejection_reason": "SS_TAX_ID_MISMATCH"
              },
              "status": {
                "dtcc_status": "REJECT",
                "transfer_status": "REJECTED"
              },
              "total_transfer_value": "24223.62",
              "transfer_identifier": "03251237654321",
              "transfer_type": "FUL"
            }
          ]
        },
        "properties": {
          "page_token_next": {
            "allOf": [
              {
                "description": "Page token for the next page of transfers. Pass it back in the `page_token` query parameter to fetch that page. Not returned when the caller is on the last page."
              },
              {
                "$ref": "#/components/schemas/AcatsPageToken"
              }
            ]
          },
          "page_token_previous": {
            "allOf": [
              {
                "description": "Page token for the previous page of transfers. Pass it back in the `page_token` query parameter to fetch that page. Not returned when the caller is on the first page."
              },
              {
                "$ref": "#/components/schemas/AcatsPageToken"
              }
            ]
          },
          "pending_transfers": {
            "description": "The count of ACATS transfers pending review",
            "example": 37,
            "format": "int32",
            "type": "integer"
          },
          "transfers": {
            "items": {
              "$ref": "#/components/schemas/AcatsTransfer"
            },
            "type": "array"
          }
        },
        "required": [
          "transfers"
        ],
        "type": "object"
      },
      "AcatsPageToken": {
        "description": "Page token, pass it back unchanged in the `page_token` query parameter to fetch the next or previous page.",
        "example": "eyJjcmVhdGVkX2F0IjoiMjAyNi0wNC0yOFQxNDozMDowMFoiLCJpZCI6IjAxQUJDIn0=",
        "type": "string"
      },
      "AcatsRejectionDetails": {
        "description": "Why the transfer was rejected, only present on transfers in rejected status",
        "properties": {
          "rejection_message": {
            "description": "Human readable message regarding the reason for the rejection",
            "type": "string"
          },
          "rejection_reason": {
            "description": "Rejection reason, as returned by DTCC",
            "enum": [
              "SS_TAX_ID_MISMATCH",
              "ACCOUNT_TITLE_MISMATCH",
              "DOCUMENTATION_NEEDED",
              "ACCOUNT_FLAT",
              "INVALID_ACCOUNT_NUMBER",
              "DUPLICATE",
              "ACCOUNT_IN_DISTRIBUTION_OR_TRANSFER",
              "CLIENT_RESCINDED",
              "MISSING_AUTHORIZATION_SIGNATURE",
              "ACCOUNT_VIOLATES_CREDIT_POLICY_OF_RECEIVING_FIRM",
              "UNRECOGNIZED_FOR_RESIDUAL_CREDIT_BALANCE",
              "PARTIAL_TRANSFER_DELIVERER_INITIATED_REJECT",
              "FAIL_REVERSAL_REJECT",
              "RECLAIM_REJECT",
              "MUTUAL_FUND_CLEANUP",
              "SYSTEM_REJECTED",
              "INVALID_PARTICIPANT",
              "ASSOCIATED_RECORD_NOT_PRESENT_OR_INVALID",
              "MISSED_CUTOFF"
            ],
            "type": "string"
          }
        },
        "type": "object"
      },
      "AcatsStatusDetails": {
        "description": "Status details",
        "properties": {
          "dtcc_status": {
            "$ref": "#/components/schemas/AcatsDtccStatus"
          },
          "transfer_status": {
            "$ref": "#/components/schemas/AcatsTransferStatus"
          }
        },
        "type": "object"
      },
      "AcatsTimestamp": {
        "description": "Timestamp in RFC-3339 format with microsecond precision",
        "example": "2026-01-01T00:00:00Z",
        "format": "date-time",
        "type": "string"
      },
      "AcatsTransfer": {
        "description": "An ACATS transfer and its current status.",
        "example": {
          "acats_id": "2c827687-ddd3-4ad9-bee8-0a3cdad35301",
          "account_id": "9ac16d7d-1f6e-445b-8e51-807e77ba2902",
          "account_name": "John Doe",
          "account_number": "12345678",
          "account_type": "SINGLE",
          "contra_account_number": "A00000123",
          "contra_broker_name": "Alpaca Clearing",
          "contra_broker_number": "00001234",
          "contra_broker_type": "BANK",
          "created_at": "2026-04-21T12:41:03.505862Z",
          "direction": "INCOMING",
          "ip_address": "203.0.113.42",
          "rejection_details": {
            "rejection_message": "SS# Tax ID Mismatch",
            "rejection_reason": "SS_TAX_ID_MISMATCH"
          },
          "status": {
            "dtcc_status": "REJECT",
            "transfer_status": "REJECTED"
          },
          "total_transfer_value": "24223.62",
          "transfer_identifier": "03251237654321",
          "transfer_type": "FUL"
        },
        "properties": {
          "acats_id": {
            "description": "The ID of the ACATS transfer",
            "format": "uuid",
            "type": "string"
          },
          "account_id": {
            "description": "Account ID associated with the ACATS transfer",
            "format": "uuid",
            "type": "string"
          },
          "account_name": {
            "description": "Name on the Alpaca account associated with the transfer",
            "type": "string"
          },
          "account_number": {
            "description": "Account number at Alpaca",
            "type": "string"
          },
          "account_type": {
            "$ref": "#/components/schemas/AcatsAccountType"
          },
          "contra_account_number": {
            "description": "Account number at the contra broker",
            "type": "string"
          },
          "contra_broker_name": {
            "description": "Name of the contra broker",
            "type": "string"
          },
          "contra_broker_number": {
            "description": "DTCC account number for the contra broker",
            "type": "string"
          },
          "contra_broker_type": {
            "$ref": "#/components/schemas/AcatsContraBrokerType"
          },
          "created_at": {
            "$ref": "#/components/schemas/AcatsTimestamp"
          },
          "direction": {
            "$ref": "#/components/schemas/AcatsTransferDirection"
          },
          "ip_address": {
            "description": "User's IP address (IPv4 or IPv6) at time of submission",
            "type": "string"
          },
          "original_transfer_identifier": {
            "description": "DTCC transfer identifier for a previous, related transfer",
            "type": "string"
          },
          "rejection_details": {
            "$ref": "#/components/schemas/AcatsRejectionDetails"
          },
          "settlement_date": {
            "$ref": "#/components/schemas/AcatsTimestamp"
          },
          "status": {
            "$ref": "#/components/schemas/AcatsStatusDetails"
          },
          "total_transfer_value": {
            "description": "Total transfer value is the sum of the market value of all assets and securities in an ACAT at the time of settlement, plus any cash balance.",
            "format": "decimal",
            "type": "string"
          },
          "transfer_identifier": {
            "description": "DTCC transfer identifier, also known as the control number",
            "type": "string"
          },
          "transfer_type": {
            "$ref": "#/components/schemas/AcatsDtccTransferType"
          }
        },
        "required": [
          "acats_id",
          "account_id",
          "account_number",
          "created_at",
          "contra_account_number",
          "contra_broker_number",
          "transfer_type",
          "direction",
          "status"
        ],
        "type": "object"
      },
      "AcatsTransferDirection": {
        "description": "Transfer direction",
        "enum": [
          "INCOMING",
          "OUTGOING"
        ],
        "type": "string"
      },
      "AcatsTransferStatus": {
        "description": "Transfer status as tracked by Alpaca",
        "enum": [
          "PENDING",
          "IN_PROGRESS",
          "REJECTED",
          "SETTLED"
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
    "/v1beta1/acats/{account_id}": {
      "get": {
        "description": "List all incoming and outgoing transfers where the account was one of the parties. The list may include transfers not initiated using this API. By default, the response includes all transfers for the account for backwards compatibility. To paginate results, provide the `limit` query parameter and use the `page_token` value returned in the response to continue listing transfers.",
        "operationId": "listACATSTransfersByAccount",
        "parameters": [
          {
            "description": "Account ID associated with the ACATS transfer",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "Maximum number of transfers to return on one page",
            "in": "query",
            "name": "limit",
            "required": false,
            "schema": {
              "format": "int32",
              "type": "integer"
            }
          },
          {
            "description": "Page token for the next or previous page, used to continue listing transfers",
            "in": "query",
            "name": "page_token",
            "required": false,
            "schema": {
              "$ref": "#/components/schemas/AcatsPageToken"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsListTransfersResponse"
                }
              }
            },
            "description": "OK"
          },
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Forbidden"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "summary": "List transfers for an account",
        "tags": [
          "ACATS"
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
      "name": "ACATS"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```