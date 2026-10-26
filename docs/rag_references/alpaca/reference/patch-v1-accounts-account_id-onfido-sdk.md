# Update the Onfido SDK Outcome

Source: https://docs.alpaca.markets/us/reference/patch-v1-accounts-account_id-onfido-sdk.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Update the Onfido SDK Outcome

This request allows you to send Alpaca the result of the Onfido SDK flow in your app. A notification of a successful outcome is required for Alpaca to continue the KYC process.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "OnfidoSDKOutcome": {
        "description": "\"NOT_STARTED\"\tThe user has not started the SDK flow yet. outcome is set to this default value upon token generation\n\"USER_EXITED\"\tThe user exited the SDK flow\n\"SDK_ERROR\"\tAn error occurred in the SDK flow\n\"USER_COMPLETED\"\tThe user completed the SDK flow",
        "title": "OnfidoSDKOutcome",
        "type": "string"
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
    "/v1/accounts/{account_id}/onfido/sdk": {
      "parameters": [
        {
          "in": "path",
          "name": "account_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ],
      "patch": {
        "description": "This request allows you to send Alpaca the result of the Onfido SDK flow in your app. A notification of a successful outcome is required for Alpaca to continue the KYC process.",
        "operationId": "patch-v1-accounts-account_id-onfido-sdk",
        "requestBody": {
          "content": {
            "application/json": {
              "examples": {
                "Example 1": {
                  "value": {
                    "outcome": "USER_EXITED",
                    "reason": "User denied consent",
                    "token": "header.payload.signature"
                  }
                }
              },
              "schema": {
                "properties": {
                  "outcome": {
                    "$ref": "#/components/schemas/OnfidoSDKOutcome"
                  },
                  "reason": {
                    "description": "Any additional information related to the outcome",
                    "type": "string"
                  },
                  "token": {
                    "description": "The SDK token associated with the SDK flow you are updating the outcome for",
                    "type": "string"
                  }
                },
                "required": [
                  "outcome",
                  "token"
                ],
                "type": "object"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Account Not Found"
          },
          "422": {
            "description": "Invalid input value for outcome."
          }
        },
        "summary": "Update the Onfido SDK Outcome",
        "tags": [
          "KYC"
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
      "name": "KYC"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```