# Retrieve funding wallet transfer by ID

Source: https://docs.alpaca.markets/us/reference/getfundingwallettransferbyid.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve funding wallet transfer by ID

Returns a single funding wallet transfer for the specified account by `transfer_id`. Responds with 404 if no matching transfer exists for the account.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "Currency": {
        "description": "\"USD\" // US Dollar\n\"JPY\" // Japanese Yen\n\"EUR\" // Euro\n\"CAD\" // Canadian Dollar\n\"GBP\" // British Pound Sterling\n\"CHF\" // Swiss Franc\n\"TRY\" // Turkish Lira\n\"AUD\" // Australian Dollar\n\"CZK\" // Czech Koruna\n\"SEK\" // Swedish Krona\n\"DKK\" // Danish Krone\n\"SGD\" // Singapore Dollar\n\"HKD\" // Hong Kong Dollar\n\"HUF\" // Hungarian Forint\n\"NZD\" // New Zealand Dollar\n\"NOK\" // Norwegian Krone\n\"PLN\" // Poland Złoty",
        "title": "Currency",
        "type": "string"
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
      "FeePaymentType": {
        "description": "Status:\n * `invoice`\n",
        "enum": [
          "invoice"
        ],
        "type": "string"
      },
      "FeeType": {
        "description": "Status:\n  * `withdrawal_fee`: Withdrawal fee\n  * `fx_fee`: FX Fee\n  * `network_fee`\n  * `deposit_fee`\n  * `ach_return_fee`\n  * `parnter_fee`\n  * `alpaca_fee`\n",
        "enum": [
          "withdrawal_fee",
          "fx_fee",
          "network_fee",
          "deposit_fee",
          "ach_return_fee",
          "parnter_fee",
          "alpaca_fee"
        ],
        "type": "string"
      },
      "FundingDetailPaymentType": {
        "description": "Status:\n * `swift_wire`: SWIFT wire\n * `local_rails`: Local scheme\n",
        "enum": [
          "swift_wire",
          "local_rails"
        ],
        "type": "string"
      },
      "FundingWalletTransfer": {
        "properties": {
          "account_id": {
            "format": "uuid",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "direction": {
            "$ref": "#/components/schemas/FundingWalletTransferDirection"
          },
          "fees": {
            "items": {
              "$ref": "#/components/schemas/TransferFee"
            },
            "type": "array"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "original_amount": {
            "deprecated": true,
            "description": "Deprecated. Prefer `total_amount` for the actual amount debited from the account. The amount you should expect to receive, calculated as requested amount - fees.",
            "format": "decimal",
            "type": "string",
            "x-deprecation": {
              "reason": "Use total_amount for the actual amount debited from the account.",
              "since": "2026-09-22",
              "sunset": "2026-12-21"
            }
          },
          "original_currency": {
            "description": "The currency of the withdrawn amount, 3-letter ISO code",
            "type": "string"
          },
          "payment_type": {
            "$ref": "#/components/schemas/FundingDetailPaymentType"
          },
          "requested_amount": {
            "description": "The amount requested when the transfer was created.",
            "format": "decimal",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/FundingWalletTransferStatus"
          },
          "total_amount": {
            "description": "The total amount moved for the transfer. For outgoing transfers with fees added on top, this is the requested amount plus fees (the total debited from the account). For fee-inclusive outgoing withdrawals, fees are taken out of the requested amount, so this equals requested_amount. For incoming transfers, this is the requested amount credited to the account.",
            "format": "decimal",
            "type": "string"
          },
          "updated_at": {
            "format": "date-time",
            "type": "string"
          },
          "usd": {
            "$ref": "#/components/schemas/Usd"
          }
        },
        "type": "object"
      },
      "FundingWalletTransferDirection": {
        "description": "Status:\n * `incoming`: incoming amount\n * `outgoing`: outgoing amount\n",
        "enum": [
          "incoming",
          "outgoing"
        ],
        "type": "string"
      },
      "FundingWalletTransferStatus": {
        "description": "Status:\n * `PENDING`: Created and waiting to be processed\n * `CANCELED`: Canceled\n * `FAILED`: Failed mostly due to technical reasons\n * `COMPLETE`: Transfer has settled\n",
        "enum": [
          "PENDING",
          "CANCELED",
          "EXECUTED",
          "FAILED",
          "COMPLETE"
        ],
        "type": "string"
      },
      "TransferFee": {
        "properties": {
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "currency": {
            "$ref": "#/components/schemas/Currency"
          },
          "payment_type": {
            "$ref": "#/components/schemas/FeePaymentType"
          },
          "type": {
            "$ref": "#/components/schemas/FeeType"
          }
        },
        "required": [
          "type",
          "amount",
          "currency",
          "payment_type"
        ],
        "type": "object"
      },
      "Usd": {
        "properties": {
          "amount": {
            "format": "decimal",
            "type": "string"
          }
        },
        "required": [
          "amount"
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
    "/v1beta/accounts/{account_id}/funding_wallet/transfers/{transfer_id}": {
      "get": {
        "description": "Returns a single funding wallet transfer for the specified account by `transfer_id`. Responds with 404 if no matching transfer exists for the account.",
        "operationId": "getFundingWalletTransferByID",
        "parameters": [
          {
            "description": "Alpaca account UUID",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "transfer UUID",
            "in": "path",
            "name": "transfer_id",
            "required": true,
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
                  "$ref": "#/components/schemas/FundingWalletTransfer"
                }
              }
            },
            "description": "transfer response if found"
          },
          "404": {
            "description": "error response if transfer is not found"
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "error"
          }
        },
        "summary": "Retrieve funding wallet transfer by ID",
        "tags": [
          "Funding Wallets"
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
      "name": "Funding Wallets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```