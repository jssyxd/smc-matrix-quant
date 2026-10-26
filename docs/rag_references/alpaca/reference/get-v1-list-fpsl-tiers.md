# List FPSL Tiers

Source: https://docs.alpaca.markets/us/reference/get-v1-list-fpsl-tiers.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List FPSL Tiers

List all available FPSL tiers. These tiers may be assigned to an account.

# OpenAPI definition

```json
{
  "components": {
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
      "FPSLTier": {
        "properties": {
          "created_at": {
            "description": "The timestamp the FPSL tier was created, in RFC 3339 format.",
            "example": "2024-09-16T20:06:32.207729Z",
            "format": "date-time",
            "type": "string"
          },
          "customer_split": {
            "description": "Percentage of the customer split represented as a value between 0 and 1.00. Max 2 decimal places are allowed.",
            "example": 0.25,
            "type": "number"
          },
          "id": {
            "description": "The unique identifier of the FPSL tier",
            "example": "150df7eb-31e7-46b3-8848-a54ca21ff3bc",
            "format": "uuid",
            "type": "string"
          },
          "market": {
            "description": "The market of the FPSL tier",
            "example": "US",
            "type": "string"
          },
          "partner_split": {
            "description": "Percentage of the partner split represented as a value between 0 and 1.00. Max 2 decimal places are allowed.",
            "example": 0.3,
            "type": "number"
          },
          "tier_name": {
            "description": "The name of the FPSL tier",
            "example": "gold",
            "type": "string"
          },
          "updated_at": {
            "description": "The timestamp of the last update to the FPSL tier, in RFC 3339 format.",
            "example": "2024-09-16T20:06:32.207729Z",
            "format": "date-time",
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
    "/v1/fpsl/tiers": {
      "get": {
        "description": "List all available FPSL tiers. These tiers may be assigned to an account.",
        "operationId": "get-v1-list-fpsl-tiers",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/FPSLTier"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Successful response, returns a list of FPSL tiers or none if no tiers are available."
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
        "summary": "List FPSL Tiers",
        "tags": [
          "FPSL Program"
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
      "name": "FPSL Program"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```