# Create a new JIT settlement

Source: https://docs.alpaca.markets/us/reference/post-v1-jit-settlements.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create a new JIT settlement

Creates a new JIT settlement, which will trigger the reconciliation process for all included accounts. There is a limit of 150,000 accounts per settlement. If more than 150,000 accounts need to be settled, they should be batched in multiple settlements.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CreateJITSettlementRequest": {
        "description": "Request to create a new settlement. All transfers included must use the same source account, and the total amount received must be in the same currency as the base currency of the source account.\n",
        "properties": {
          "accounts": {
            "items": {
              "$ref": "#/components/schemas/SettlementAccount"
            },
            "type": "array"
          },
          "additional_info": {
            "description": "Additional remittance information. Include if the funding source may require additional information to associate to the source account or settlement.\n",
            "type": "string"
          },
          "asset_class": {
            "$ref": "#/components/schemas/JITAssetClass"
          },
          "currency": {
            "description": "The currency of the settlement. All accounts identified should have this base currency.\n",
            "type": "string"
          }
        },
        "required": [
          "currency",
          "asset_class",
          "accounts"
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
      "JITAssetClass": {
        "description": "Values:\n * `crypto`: Used to identify a crypto only account\n * `us_equity`: Used to identify an account that trades US equities, or both crypto and\n  US equities.\n",
        "enum": [
          "crypto",
          "us_equity"
        ],
        "type": "string"
      },
      "SettlementAccount": {
        "properties": {
          "account_number": {
            "description": "The account number of the client account to settle\n",
            "type": "string"
          },
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "transmitter_info": {
            "$ref": "#/components/schemas/TransmitterInfo"
          }
        },
        "required": [
          "account_number",
          "amount",
          "transmitter_info"
        ],
        "type": "object"
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
      },
      "TransmitterInfo": {
        "description": "Information about the transmitter to satisfy travel rule requirements. Required if the requesting correspondent qualifies as a financial institution\n",
        "properties": {
          "originator_bank_account_number": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_bank_name": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_city": {
            "type": "string"
          },
          "originator_country": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_full_name": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_postal_code": {
            "type": "string"
          },
          "originator_state": {
            "type": "string"
          },
          "originator_street_address": {
            "type": "string"
          },
          "other_identifying_information": {
            "description": "Used to facilitate transfer lookup in the event it is required. Recommended to be the originating bank's reference number for the transfer\n",
            "type": "string"
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
    "/v1/jit/settlements": {
      "post": {
        "description": "Creates a new JIT settlement, which will trigger the reconciliation process for all included accounts. There is a limit of 150,000 accounts per settlement. If more than 150,000 accounts need to be settled, they should be batched in multiple settlements.\n",
        "operationId": "post-v1-jit-settlements",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateJITSettlementRequest"
              }
            }
          },
          "description": "details of the JIT settlement request",
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/SettlementResponse"
                }
              }
            },
            "description": "Settlement created."
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
        "summary": "Create a new JIT settlement",
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