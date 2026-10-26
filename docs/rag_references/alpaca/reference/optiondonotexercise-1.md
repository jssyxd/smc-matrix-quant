# Do Not Exercise an Options Position

Source: https://docs.alpaca.markets/us/reference/optiondonotexercise-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Do Not Exercise an Options Position

This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.
By default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.
DNE requests will be processed immediately once received. DNE requests submitted between market close and midnight will be rejected to avoid any confusion about when the instruction will take effect.
To cancel a DNE request or to submit an exercise instruction, please contact our support team.

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
      "DoNotExerciseRequest": {
        "description": "Request to submit a do-not-exercise (DNE) instruction for an option contract for an account.\nThe request body is empty. A successful request will mark the entire position as do not exercise.",
        "title": "DoNotExerciseRequest",
        "type": "object"
      },
      "DoNotExerciseResponse": {
        "description": "Response to a do-not-exercise request.\nA 200 response indicates that the entire position is set as do not exercise.\nThe response body is empty.",
        "title": "DoNotExerciseResponse",
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
    "/v1/trading/accounts/{account_id}/positions/{symbol_or_contract_id}/do-not-exercise": {
      "post": {
        "description": "This endpoint enables users to submit a do-not-exercise (DNE) instruction for a held option contract, preventing automatic exercise at expiry.\nBy default, Alpaca will automatically exercise in-the-money (ITM) contracts at expiry. This endpoint allows users to override that behavior.\nDNE requests will be processed immediately once received. DNE requests submitted between market close and midnight will be rejected to avoid any confusion about when the instruction will take effect.\nTo cancel a DNE request or to submit an exercise instruction, please contact our support team.",
        "operationId": "optionDoNotExercise",
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
                "$ref": "#/components/schemas/DoNotExerciseRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/DoNotExerciseResponse"
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
                      "message": "cannot submit DNE for short position"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Forbidden"
          },
          "422": {
            "content": {
              "application/json": {
                "examples": {
                  "Invalid Symbol": {
                    "value": {
                      "code": 42210000,
                      "message": "invalid symbol_or_contract_id"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Invalid Symbol\n\nThe specified symbol_or_contract_id is invalid."
          }
        },
        "summary": "Do Not Exercise an Options Position",
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