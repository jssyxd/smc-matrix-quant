# Create sandbox deposit transfer

Source: https://docs.alpaca.markets/us/reference/demodepositfunding.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create sandbox deposit transfer

Simulates an inbound deposit into an account's funding wallet for end-to-end testing of the deposit flow.

The transfer can only credit accounts that belong to your firm. Available in non-production (sandbox) environments only.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "DemoFundingTransfer": {
        "properties": {
          "amount": {
            "format": "decimal",
            "type": "string"
          },
          "currency": {
            "type": "string"
          },
          "receiver_account_number": {
            "type": "string"
          },
          "receiver_routing_code": {
            "type": "string"
          }
        },
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
    "/v1beta/demo/banking/funding": {
      "post": {
        "description": "Simulates an inbound deposit into an account's funding wallet for end-to-end testing of the deposit flow.\n\nThe transfer can only credit accounts that belong to your firm. Available in non-production (sandbox) environments only.",
        "operationId": "demoDepositFunding",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/DemoFundingTransfer"
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
                  "$ref": "#/components/schemas/DemoFundingTransfer"
                }
              }
            },
            "description": "Demo deposit funding transfer"
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
        "summary": "Create sandbox deposit transfer",
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