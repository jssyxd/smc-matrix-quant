# Retrieve JIT Ledger Balances

Source: https://docs.alpaca.markets/us/reference/get-v1-transfers-jit-ledger_id-balances.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve JIT Ledger Balances

Returns an array of objects that correspond to each ledger account.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "Transaction": {
        "examples": [
          {
            "account_id": "06b9d76e-1733-460c-844e-48d1ae0f10c3",
            "account_name": "Just In Time Receivable - JITS",
            "account_no": "JTRJITS00",
            "amount": "1",
            "balance": "4186.36",
            "contra_account_name": "Just In Time Interest Income",
            "description": "debit balance = 4185.36, base_rate = 0.0375, spread = 0.05",
            "entry_type": "JNLC",
            "system_date": "2022-06-10"
          }
        ],
        "properties": {
          "account_id": {
            "description": "The ledger ID",
            "type": "string"
          },
          "account_name": {
            "description": "The ledger name",
            "type": "string"
          },
          "account_no": {
            "description": "The ledger account number",
            "type": "string"
          },
          "amount": {
            "description": "Total amount of the transaction",
            "type": "string"
          },
          "balance": {
            "description": "Ending balance after thetransaction has been applied",
            "type": "string"
          },
          "contra_account_name": {
            "description": "Contra account of transaction",
            "type": "string"
          },
          "description": {
            "description": "Plain text overview of the transaction",
            "type": "string"
          },
          "entry_type": {
            "description": "Type of transaction",
            "type": "string"
          },
          "system_date": {
            "description": "Date of transaction",
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
    "/v1/transfers/jit/{ledger_id}/balances": {
      "get": {
        "description": "Returns an array of objects that correspond to each ledger account.",
        "operationId": "get-v1-transfers-jit-ledger_id-balances",
        "parameters": [
          {
            "in": "path",
            "name": "ledger_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The start date (inclusive) of the ledgerbalances and activities.",
            "in": "query",
            "name": "start_date",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "The end date (inclusive) of the ledgerbalances and activities.",
            "in": "query",
            "name": "end_date",
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
                  "properties": {
                    "activity_amount": {
                      "description": "The number of transactions related to the ledger during the specified date range ",
                      "format": "decimal",
                      "type": "string"
                    },
                    "ending_balance": {
                      "description": "Ledger balance at the end of the date range",
                      "format": "decimal",
                      "type": "string"
                    },
                    "id": {
                      "description": "The ledger ID",
                      "type": "string"
                    },
                    "ledger_name": {
                      "description": "The ledger name",
                      "type": "string"
                    },
                    "ledger_no": {
                      "description": "The ledger account number",
                      "type": "string"
                    },
                    "starting_balance": {
                      "description": "Ledger balance at the beginning of the date range",
                      "format": "decimal",
                      "type": "string"
                    },
                    "transactions": {
                      "items": {
                        "$ref": "#/components/schemas/Transaction"
                      },
                      "type": "array"
                    }
                  },
                  "type": "object"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve JIT Ledger Balances",
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