# Retrieve JIT Ledgers

Source: https://docs.alpaca.markets/us/reference/get-v1-transfers-jit-ledgers.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve JIT Ledgers

Returns an array of objects that correspond to each ledger account, each of whichcontain the following attributes.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "JITLedgerAccount": {
        "examples": [
          {
            "created_at": "1653532627",
            "id": "2896b9e2-3198-44cd-a08e-4cc4079aee33",
            "ledger_name": "Securities JIT IN",
            "status": "active"
          }
        ],
        "properties": {
          "created_at": {
            "description": "Creation time in UNIX format",
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
          "status": {
            "type": "string"
          }
        },
        "title": "JITLedgerAccount",
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
    "/v1/transfers/jit/ledgers": {
      "get": {
        "description": "Returns an array of objects that correspond to each ledger account, each of whichcontain the following attributes.",
        "operationId": "get-v1-transfers-jit-ledgers",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/JITLedgerAccount"
                  },
                  "type": "array"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve JIT Ledgers",
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