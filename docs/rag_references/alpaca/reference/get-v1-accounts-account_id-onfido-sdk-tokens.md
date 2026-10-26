# Retrieve an Onfido SDK Token

Source: https://docs.alpaca.markets/us/reference/get-v1-accounts-account_id-onfido-sdk-tokens.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve an Onfido SDK Token

Get an SDK token to activate the Onfido SDK flow within your app. You will have to keep track of the SDK token so you can pass it back when you upload the SDK outcome. We recommend storing the token in memory rather than persistent storage to reduce any unnecessary overhead in your app.

# OpenAPI definition

```json
{
  "components": {
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
    "/v1/accounts/{account_id}/onfido/sdk/tokens": {
      "get": {
        "description": "Get an SDK token to activate the Onfido SDK flow within your app. You will have to keep track of the SDK token so you can pass it back when you upload the SDK outcome. We recommend storing the token in memory rather than persistent storage to reduce any unnecessary overhead in your app.",
        "operationId": "get-v1-accounts-account_id-onfido-sdk-tokens",
        "parameters": [
          {
            "description": "The account ID",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "The referrer URL of your web app or the application ID of your mobile app. If not passed in, will default to the * wildcard",
            "in": "query",
            "name": "referrer",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Required if referrer provided. Enum values are either mobile or web",
            "in": "query",
            "name": "platform",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "Example 1": {
                    "value": {
                      "token": "header.payload.signature"
                    }
                  }
                },
                "schema": {
                  "properties": {
                    "token": {
                      "type": "string"
                    }
                  },
                  "type": "object"
                }
              }
            },
            "description": "OK"
          },
          "422": {
            "description": "Onfido applicant not yet created for account. If you haven't already contacted Alapca to enable Onfido, please do so."
          }
        },
        "summary": "Retrieve an Onfido SDK Token",
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