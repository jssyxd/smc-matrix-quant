# List contra brokers

Source: https://docs.alpaca.markets/us/reference/listacatscontrabrokers.md

---
updatedAt: 2026-06-23T06:50:20.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List contra brokers

This information is provided based on the latest ACATS Participant Master File, and contains the DTCC account numbers of valid contra brokers. Only participants that are either brokers or banks are returned. These numbers are the valid values for the `broker_number` property that is required for initiating transfers.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AcatsContraBroker": {
        "description": "A contra broker or bank participating in ACATS, identified by its DTCC account number.",
        "properties": {
          "name": {
            "description": "Participant name",
            "type": "string"
          },
          "number": {
            "description": "DTCC account number",
            "type": "string"
          },
          "type": {
            "$ref": "#/components/schemas/AcatsContraBrokerType"
          }
        },
        "required": [
          "number",
          "type",
          "name"
        ],
        "type": "object"
      },
      "AcatsContraBrokerType": {
        "description": "ACATS participant type",
        "enum": [
          "BANK",
          "BROKER"
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
      "AcatsListContraBrokersResponse": {
        "description": "Response containing the list of valid ACATS contra brokers.",
        "example": {
          "brokers": [
            {
              "name": "Example Brokerage Inc.",
              "number": "0001",
              "type": "BROKER"
            },
            {
              "name": "Example Bank, N.A.",
              "number": "0002",
              "type": "BANK"
            }
          ]
        },
        "properties": {
          "brokers": {
            "items": {
              "$ref": "#/components/schemas/AcatsContraBroker"
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
    "/v1beta1/acats/contrabrokers": {
      "get": {
        "description": "This information is provided based on the latest ACATS Participant Master File, and contains the DTCC account numbers of valid contra brokers. Only participants that are either brokers or banks are returned. These numbers are the valid values for the `broker_number` property that is required for initiating transfers.",
        "operationId": "listACATSContraBrokers",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "example": {
                  "brokers": [
                    {
                      "name": "Example Brokerage Inc.",
                      "number": "0001",
                      "type": "BROKER"
                    },
                    {
                      "name": "Example Bank, N.A.",
                      "number": "0002",
                      "type": "BANK"
                    }
                  ]
                },
                "schema": {
                  "$ref": "#/components/schemas/AcatsListContraBrokersResponse"
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
        "summary": "List contra brokers",
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