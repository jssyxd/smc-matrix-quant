# Authorize an OAuth Token

Source: https://docs.alpaca.markets/us/reference/authorizeoauthtoken.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Authorize an OAuth Token

The operation issues an OAuth code which can be used in the OAuth code flow.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AuthorizeOAuthTokenResponse": {
        "description": "",
        "examples": [
          {
            "client_id": "7a3c52a910e1dc2abbb14da2b6b8e711",
            "code": "912b5502-c983-40f7-a01d-6a66f13a754d",
            "redirect_uri": "http://localhost",
            "scope": ""
          }
        ],
        "properties": {
          "client_id": {
            "description": "OAuth `client_id`",
            "minLength": 1,
            "type": "string"
          },
          "code": {
            "description": "OAuth code to exchange with token",
            "minLength": 1,
            "type": "string"
          },
          "redirect_uri": {
            "description": "Redirect URI of OAuth flow",
            "minLength": 1,
            "type": "string"
          },
          "scope": {
            "description": "Granted scopes",
            "type": "string"
          }
        },
        "required": [
          "code",
          "client_id",
          "redirect_uri",
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
    "/v1/oauth/authorize": {
      "post": {
        "description": "The operation issues an OAuth code which can be used in the OAuth code flow.\n",
        "operationId": "authorizeOAuthToken",
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
                "schema": {
                  "$ref": "#/components/schemas/AuthorizeOAuthTokenResponse"
                }
              }
            },
            "description": "Successfully issued a code."
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
        "summary": "Authorize an OAuth Token",
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