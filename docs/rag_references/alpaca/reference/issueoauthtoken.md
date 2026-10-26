# Issue an OAuth token

Source: https://docs.alpaca.markets/us/reference/issueoauthtoken.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Issue an OAuth token

The operation issues an OAuth code which can be used in the OAuth code flow.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "IssueOAuthTokenResponse": {
        "description": "",
        "examples": [
          {
            "access_token": "87586f14-c3f4-4912-b107-f75bc17ff87a",
            "scope": "general",
            "token_type": "Bearer"
          }
        ],
        "properties": {
          "access_token": {
            "description": "OAuth token",
            "type": "string"
          },
          "scope": {
            "description": "Token's scope",
            "type": "string"
          },
          "token_type": {
            "description": "Always `Bearer`",
            "enum": [
              "Bearer"
            ],
            "example": "Bearer",
            "type": "string"
          }
        },
        "required": [
          "access_token",
          "token_type",
          "scope"
        ],
        "type": "object"
      },
      "OAuthTokenRequest": {
        "description": "This model is used for both the Issue and Authorize OAuth token routes",
        "example": {
          "account_id": "0d18ae51-3c94-4511-b209-101e1666416b",
          "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
          "client_secret": "bbb14da2b6b8e7117a3c52a910e1dc2a",
          "redirect_uri": "http://localhost",
          "scope": "general"
        },
        "properties": {
          "account_id": {
            "description": "end-user account ID",
            "format": "uuid",
            "type": "string"
          },
          "client_id": {
            "description": "OAuth client ID",
            "type": "string"
          },
          "client_secret": {
            "description": "OAuth client secret",
            "type": "string"
          },
          "redirect_uri": {
            "description": "redirect URI for the OAuth flow",
            "type": "string"
          },
          "scope": {
            "description": "scopes requested by the OAuth flow",
            "type": "string"
          }
        },
        "required": [
          "client_id",
          "client_secret",
          "redirect_uri",
          "scope",
          "account_id"
        ],
        "title": "OAuthTokenRequest",
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
    "/v1/oauth/token": {
      "post": {
        "description": "The operation issues an OAuth code which can be used in the OAuth code flow.\n",
        "operationId": "issueOAuthToken",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OAuthTokenRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "example-1": {
                    "value": {
                      "access_token": "87586f14-c3f4-4912-b107-f75bc17ff87a",
                      "scope": "general",
                      "token_type": "Bearer"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/IssueOAuthTokenResponse"
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
            "description": "Client does not exist, you do not have access to the client, or \"client_secret\" is incorrect.\n"
          },
          "422": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "description": "Redirect URI or scope is invalid.\n"
          }
        },
        "summary": "Issue an OAuth token",
        "tags": [
          "OAuth"
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
      "name": "OAuth"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```