# Do Not Exercise an Options Position

Source: https://docs.alpaca.markets/us/reference/optiondonotexercise.md

---
updatedAt: 2026-04-20T20:39:16.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Do Not Exercise an Options Position

This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.
By default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.
To override this behavior and submit an exercise instruction, please contact our support team.

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
      }
    },
    "securitySchemes": {
      "API_Key": {
        "description": "",
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "API_Secret": {
        "description": "",
        "in": "header",
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Trading API",
    "version": "2.0.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v2/positions/{symbol_or_contract_id}/do-not-exercise": {
      "post": {
        "description": "This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.\nBy default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.\nTo override this behavior and submit an exercise instruction, please contact our support team.",
        "operationId": "optionDoNotExercise",
        "parameters": [
          {
            "description": "Option contract symbol or ID.",
            "in": "path",
            "name": "symbol_or_contract_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response\n\nDo-not-exercise instruction successfully submitted."
          },
          "403": {
            "content": {
              "application/json": {
                "examples": {
                  "No Available Position": {
                    "value": {
                      "code": 40310000,
                      "message": "no available position for the specified contract"
                    }
                  },
                  "Short Position": {
                    "value": {
                      "code": 40310001,
                      "message": "cannot submit DNE for short position"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Forbidden\n\nAvailable position quantity is not sufficient or no position found."
          },
          "422": {
            "content": {
              "application/json": {
                "examples": {
                  "Invalid Symbol": {
                    "value": {
                      "code": 42210000,
                      "message": "invalid symbol"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Invalid Parameters.\n\nOne or more parameters provided are invalid."
          }
        },
        "summary": "Do Not Exercise an Options Position",
        "tags": [
          "Positions"
        ]
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "servers": [
    {
      "description": "Paper",
      "url": "https://paper-api.alpaca.markets"
    },
    {
      "description": "Live",
      "url": "https://api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Positions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```