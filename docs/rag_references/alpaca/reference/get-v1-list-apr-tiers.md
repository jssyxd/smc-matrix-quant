# List APR Tiers

Source: https://docs.alpaca.markets/us/reference/get-v1-list-apr-tiers.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List APR Tiers

List all available APR tiers. These tiers may be assigned to an account, and will be used to determine the interest rate paid on uninvested cash balances.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "APRTier": {
        "properties": {
          "account_rate_bps": {
            "description": "The annualized account interest rate, in basis points.",
            "example": 450,
            "type": "integer"
          },
          "correspondent_rate_bps": {
            "description": "The annualized correspondent fee rate, in basis points.",
            "example": 25,
            "type": "integer"
          },
          "created_at": {
            "description": "The timestamp the APR tier was created, in RFC 3339 format.",
            "example": "2024-09-16T20:06:32.207729Z",
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "The currency of the APR tier",
            "example": "USD",
            "type": "string"
          },
          "details": {
            "$ref": "#/components/schemas/APRTierDetails"
          },
          "id": {
            "description": "The unique identifier of the APR tier",
            "example": "150df7eb-31e7-46b3-8848-a54ca21ff3bc",
            "format": "uuid",
            "type": "string"
          },
          "is_default": {
            "description": "True if this is the default APR tier. Only one APR tier can be default per currency.\n",
            "example": true,
            "type": "boolean"
          },
          "name": {
            "description": "The unique name of the APR tier",
            "example": "gold",
            "type": "string"
          },
          "updated_at": {
            "description": "The timestamp of the last update to the APR tier, in RFC 3339 format.",
            "example": "2024-09-16T20:06:32.207729Z",
            "format": "date-time",
            "type": "string"
          }
        },
        "type": "object"
      },
      "APRTierDetails": {
        "description": "Additional details of the APR tier\n",
        "properties": {
          "as_of": {
            "description": "The date on which the total balance was recorded, at the end of the day. YYYY-MM-DD format.\n",
            "example": "2024-09-27",
            "format": "date",
            "type": "string"
          },
          "total_accounts": {
            "description": "The total number of accounts assigned this APR tier.",
            "example": 42,
            "type": "integer"
          },
          "total_balance": {
            "description": "The total balance of funds in this APR tier.",
            "example": "10485.76",
            "format": "decimal",
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
      },
      "ListAPRTiersResponse": {
        "description": "Response to a successful request for a list of APR tiers.\n",
        "properties": {
          "apr_tiers": {
            "description": "All configured APR tiers available for assignment to accounts",
            "items": {
              "$ref": "#/components/schemas/APRTier"
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
    "/v1/cash_interest/apr_tiers": {
      "get": {
        "description": "List all available APR tiers. These tiers may be assigned to an account, and will be used to determine the interest rate paid on uninvested cash balances.",
        "operationId": "get-v1-list-apr-tiers",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListAPRTiersResponse"
                }
              }
            },
            "description": "Successful response, returns a list of APR tiers or none if no tiers are available."
          },
          "401": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Unauthorized. Please check your API key and try again."
          },
          "429": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Too many requests. Please wait a moment and try again."
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "A server error occurred. Please contact Alpaca."
          }
        },
        "summary": "List APR Tiers",
        "tags": [
          "Cash Interest"
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
      "name": "Cash Interest"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```