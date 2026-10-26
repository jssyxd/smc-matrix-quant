# Issue tokens

Source: https://docs.alpaca.markets/us/reference/issuetokens.md

---
updatedAt: 2026-06-15T17:19:21.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Issue tokens

Issue access tokens using various grant types:
- `client_credentials`: Exchange client credentials for an access token
- `urn:ietf:params:oauth:grant-type:jwt-bearer`: Exchange JWT assertion (Keycloak for brokerdash or Google for admin)
- `refresh_token`: Refresh an admin access token using a refresh token


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "client_id": {
        "description": "Client ID",
        "example": "AKSF5FVOKXYKG4ATGCJQBA",
        "maxLength": 32,
        "minLength": 20,
        "pattern": "^[A-Z0-9]+$",
        "type": "string"
      },
      "error_code": {
        "description": "Error code",
        "enum": [
          "unknown_error",
          "invalid_request_uri",
          "invalid_request_object",
          "consent_required",
          "interaction_required",
          "login_required",
          "request_unauthorized",
          "request_forbidden",
          "invalid_request",
          "unauthorized_client",
          "access_denied",
          "unsupported_response_type",
          "unsupported_response_mode",
          "invalid_scope",
          "server_error",
          "temporarily_unavailable",
          "unsupported_grant_type",
          "invalid_grant",
          "invalid_client",
          "not_found",
          "invalid_state",
          "misconfiguration",
          "insufficient_entropy",
          "invalid_token",
          "token_signature_mismatch",
          "scope_not_granted",
          "token_claim",
          "token_inactive",
          "request_not_supported",
          "request_uri_not_supported",
          "jti_known",
          "quota_exceeded",
          "conflict"
        ],
        "type": "string"
      },
      "error_response": {
        "properties": {
          "error": {
            "$ref": "#/components/schemas/error_code"
          },
          "fields": {
            "description": "List of invalid request fields, if any",
            "items": {
              "$ref": "#/components/schemas/error_response_field"
            },
            "type": "array"
          }
        },
        "required": [
          "error"
        ],
        "type": "object"
      },
      "error_response_field": {
        "properties": {
          "name": {
            "description": "Name of the request field",
            "type": "string"
          }
        },
        "required": [
          "name"
        ],
        "type": "object"
      },
      "token_request": {
        "properties": {
          "client_assertion": {
            "description": "Client assertion JWT (if using private_key_jwt)",
            "maxLength": 16384,
            "type": "string"
          },
          "client_assertion_type": {
            "description": "Client assertion type (if using private_key_jwt)",
            "enum": [
              "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
            ],
            "type": "string"
          },
          "client_id": {
            "$ref": "#/components/schemas/client_id"
          },
          "client_secret": {
            "description": "Client secret (if using client_secret)",
            "example": "MFRGGZDFMZTWQYLCMNSGKZTHNBQWEY3EMVTGO2DBMJRWIZLGM5UGCYTDMRSWMZ3I",
            "maxLength": 128,
            "type": "string"
          },
          "grant_type": {
            "description": "Grant type",
            "enum": [
              "client_credentials",
              "urn:ietf:params:oauth:grant-type:jwt-bearer",
              "refresh_token"
            ],
            "type": "string"
          }
        },
        "required": [
          "grant_type"
        ],
        "type": "object"
      },
      "token_response": {
        "properties": {
          "access_token": {
            "description": "Access token",
            "type": "string"
          },
          "expires_in": {
            "description": "Time in seconds until the token expires",
            "example": 900,
            "type": "integer"
          },
          "refresh_token": {
            "description": "Refresh token",
            "type": "string"
          },
          "token_type": {
            "description": "Type of the token (e.g., Bearer)",
            "enum": [
              "Bearer"
            ],
            "type": "string"
          }
        },
        "required": [
          "access_token",
          "expires_in",
          "token_type"
        ],
        "type": "object"
      }
    }
  },
  "info": {
    "description": "Authenticate clients and manage access to Alpaca APIs.",
    "license": {
      "name": "Creative Commons Attribution Share Alike 4.0 International",
      "url": "https://spdx.org/licenses/CC-BY-SA-4.0.html"
    },
    "title": "Authentication API",
    "version": "1.0.0"
  },
  "openapi": "3.1.2",
  "paths": {
    "/oauth2/token": {
      "post": {
        "description": "Issue access tokens using various grant types:\n- `client_credentials`: Exchange client credentials for an access token\n- `urn:ietf:params:oauth:grant-type:jwt-bearer`: Exchange JWT assertion (Keycloak for brokerdash or Google for admin)\n- `refresh_token`: Refresh an admin access token using a refresh token\n",
        "operationId": "IssueTokens",
        "requestBody": {
          "content": {
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/token_request"
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
                  "$ref": "#/components/schemas/token_response"
                }
              }
            },
            "description": "OK"
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/error_response"
                }
              }
            },
            "description": "Error"
          }
        },
        "security": [],
        "summary": "Issue tokens",
        "tags": [
          "OAuth2"
        ]
      }
    }
  },
  "servers": [
    {
      "description": "Production",
      "url": "https://authx.alpaca.markets/v1"
    },
    {
      "description": "Sandbox",
      "url": "https://authx.sandbox.alpaca.markets/v1"
    }
  ],
  "tags": [
    {
      "description": "OAuth2 endpoints",
      "name": "OAuth2"
    }
  ]
}
```