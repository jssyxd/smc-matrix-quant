# Get an OAuth client

Source: https://docs.alpaca.markets/us/reference/getoauthclient.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get an OAuth client

The endpoint returns the details of OAuth client to display in the authorization page.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "OathClientResponse": {
        "example": {
          "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
          "description": "Sample description",
          "live_trading_approved": true,
          "name": "TradingApp",
          "privacy_policy": "",
          "redirect_uri": [
            "http://localhost"
          ],
          "status": "ACTIVE",
          "terms_of_use": "",
          "url": "http://test.com"
        },
        "examples": [
          {
            "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
            "description": "Sample description",
            "live_trading_approved": true,
            "name": "TradingApp",
            "privacy_policy": "",
            "redirect_uri": [
              "http://localhost"
            ],
            "status": "ACTIVE",
            "terms_of_use": "",
            "url": "http://test.com"
          }
        ],
        "properties": {
          "client_id": {
            "description": "OAuth client id",
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "live_trading_approved": {
            "example": true,
            "type": "boolean"
          },
          "name": {
            "description": "Broker name (your name)",
            "type": "string"
          },
          "privacy_policy": {
            "description": "URL of Privacy Policy",
            "type": "string"
          },
          "redirect_uri": {
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "status": {
            "description": "ACTIVE or DISABLED",
            "enum": [
              "ACTIVE",
              "DISABLED"
            ],
            "example": "ACTIVE",
            "type": "string"
          },
          "terms_of_use": {
            "description": "URL of Terms of Use",
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        },
        "title": "OathClientResponse",
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
    "/v1/oauth/clients/{client_id}": {
      "get": {
        "description": "The endpoint returns the details of OAuth client to display in the authorization page.\n",
        "operationId": "getOAuthClient",
        "parameters": [
          {
            "description": "code or token",
            "in": "query",
            "name": "response_type",
            "schema": {
              "enum": [
                "code",
                "token"
              ],
              "example": "token",
              "type": "string"
            }
          },
          {
            "description": "Redirect URI of the OAuth flow",
            "in": "query",
            "name": "redirect_uri",
            "schema": {
              "example": "https://example.com/authorize",
              "type": "string"
            }
          },
          {
            "description": "Requested scopes by the OAuth flow",
            "in": "query",
            "name": "scope",
            "schema": {
              "example": "general",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "example-1": {
                    "value": {
                      "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
                      "description": "Sample description",
                      "live_trading_approved": false,
                      "name": "TradingApp",
                      "privacy_policy": "",
                      "redirect_uri": [
                        "http://localhost"
                      ],
                      "status": "ACTIVE",
                      "terms_of_use": "",
                      "url": "http://test.com"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/OathClientResponse"
                }
              }
            },
            "description": "Success."
          },
          "401": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "description": "Client does not exist or you do not have access to the client.\n"
          }
        },
        "summary": "Get an OAuth client",
        "tags": [
          "OAuth"
        ]
      },
      "parameters": [
        {
          "in": "path",
          "name": "client_id",
          "required": true,
          "schema": {
            "format": "uuid",
            "type": "string"
          }
        }
      ]
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
      "name": "OAuth"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```