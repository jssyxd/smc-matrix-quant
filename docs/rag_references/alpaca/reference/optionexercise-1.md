# Exercise an Options Position

Source: https://docs.alpaca.markets/us/reference/optionexercise-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Exercise an Options Position

This endpoint enables users to exercise a held option contract, converting it into the underlying asset based on the specified terms.
All available held shares of this option contract will be exercised.
By default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry.
Exercise requests will be processed immediately once received. Exercise requests submitted between market close and midnight will be rejected to avoid any confusion about when the exercise will settle.
To cancel an exercise request or to submit a Do-not-exercise (DNE) instruction, you can use the do-not-exercise endpoint or contact our support team.

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
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
      "ExerciseRequest": {
        "description": "Request to exercise an option contract for an account.\nThis can be omitted or left empty, but it also allows for optionally charging a commission for exercising or\nspecifying a specific quantity of contracts to exercise (rather than the full quantity of contracts held).",
        "properties": {
          "commission": {
            "description": "The commission you want to collect from the user. (notional amount)",
            "example": "0.25",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "The number of contracts to exercise. If not provided, all contracts will be exercised.",
            "example": "1",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "ExerciseRequest",
        "type": "object"
      },
      "ExerciseResponse": {
        "description": "Response to an exercise request.\nThis will return the total quantity of contracts exercised as well as the quantity of remaining contracts.",
        "properties": {
          "qty_exercised": {
            "description": "The total quantity of contracts exercised.",
            "format": "decimal",
            "type": "string"
          },
          "qty_remaining": {
            "description": "The total quantity of contracts remaining after the exercise.",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "ExerciseResponse",
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
    "/v1/trading/accounts/{account_id}/positions/{symbol_or_contract_id}/exercise": {
      "post": {
        "description": "This endpoint enables users to exercise a held option contract, converting it into the underlying asset based on the specified terms.\nAll available held shares of this option contract will be exercised.\nBy default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry.\nExercise requests will be processed immediately once received. Exercise requests submitted between market close and midnight will be rejected to avoid any confusion about when the exercise will settle.\nTo cancel an exercise request or to submit a Do-not-exercise (DNE) instruction, you can use the do-not-exercise endpoint or contact our support team.",
        "operationId": "optionExercise",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          },
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
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ExerciseRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ExerciseResponse"
                }
              }
            },
            "description": "Successful Response"
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
                      "message": "cannot exercise short position"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Forbidden\n\nAvailable position quantity is not sufficient."
          }
        },
        "summary": "Exercise an Options Position",
        "tags": [
          "Trading"
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
      "name": "Trading"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```