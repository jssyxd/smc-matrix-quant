# Search for VASPs

Source: https://docs.alpaca.markets/us/reference/searchvasps-1.md

---
updatedAt: 2026-07-29T12:06:40.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Search for VASPs

Search for Virtual Asset Service Providers, or crypto exchanges, on Notabene's network.
This endpoint can be used to find the VASP DID for your beneficiary's exchange when submitting
travel rule information for your whitelisted wallets. Use the `q` parameter to search for exchanges.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "SearchVASPsResponse": {
        "description": "Paginated VASP directory search results.",
        "properties": {
          "page": {
            "example": 1,
            "type": "integer"
          },
          "pages": {
            "example": 1,
            "type": "integer"
          },
          "total": {
            "description": "Total count of matching records.",
            "example": 1,
            "type": "integer"
          },
          "vasps": {
            "example": [
              {
                "id": "vasp-1",
                "name": "Example Exchange"
              }
            ],
            "items": {
              "$ref": "#/components/schemas/VASP"
            },
            "type": "array"
          }
        },
        "type": "object"
      },
      "VASP": {
        "description": "Virtual Asset Service Provider returned by the directory search.",
        "properties": {
          "address": {
            "type": "string"
          },
          "city": {
            "type": "string"
          },
          "country": {
            "description": "ISO 3166-1 alpha-2 country code for the VASP.",
            "example": "US",
            "type": "string"
          },
          "did": {
            "description": "The W3C Decentralized Identifier (DID) representing the VASP.",
            "example": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
            "pattern": "^did:[a-zA-Z0-9]*:.*$",
            "type": "string"
          },
          "emailDomain": {
            "type": "string"
          },
          "id": {
            "description": "Opaque identifier for the VASP directory record.",
            "example": "vasp-1",
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "postalCode": {
            "type": "string"
          },
          "state": {
            "type": "string"
          },
          "website": {
            "format": "uri",
            "type": "string"
          }
        },
        "required": [
          "id",
          "name"
        ],
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
    "/v2/wallets/travel-rule/vasps": {
      "get": {
        "description": "Search for Virtual Asset Service Providers, or crypto exchanges, on Notabene's network.\nThis endpoint can be used to find the VASP DID for your beneficiary's exchange when submitting\ntravel rule information for your whitelisted wallets. Use the `q` parameter to search for exchanges.",
        "operationId": "searchVASPs",
        "parameters": [
          {
            "description": "General search query string.",
            "in": "query",
            "name": "q",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Filter by VASP email domain.",
            "in": "query",
            "name": "emailDomain",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Filter by Chainalysis-specific VASP name.",
            "in": "query",
            "name": "chainalysisName",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Specify which fields to return (comma-separated).",
            "in": "query",
            "name": "fields",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The zero-based page number to retrieve.",
            "in": "query",
            "name": "page",
            "schema": {
              "default": 0,
              "minimum": 0,
              "type": "integer"
            }
          },
          {
            "description": "Number of items per page.",
            "in": "query",
            "name": "per_page",
            "schema": {
              "default": 10,
              "maximum": 100,
              "minimum": 1,
              "type": "integer"
            }
          },
          {
            "description": "Field-based sort expression, such as name:ASC. Multiple expressions may be comma-separated. Defaults to name:ASC.",
            "in": "query",
            "name": "order",
            "schema": {
              "default": "name:ASC",
              "example": "name:ASC",
              "pattern": "^([ A-Za-z]+(:(ASC|DESC))?(:NULLS (FIRST|LAST))?(,?))+$",
              "type": "string"
            }
          },
          {
            "description": "Whether to include child/subsidiary entities.",
            "in": "query",
            "name": "includeSubsidiaryVASPs",
            "schema": {
              "default": false,
              "type": "boolean"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "example": {
                  "page": 1,
                  "pages": 1,
                  "total": 1,
                  "vasps": [
                    {
                      "country": "US",
                      "did": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
                      "id": "vasp-1",
                      "name": "Example Exchange"
                    }
                  ]
                },
                "schema": {
                  "$ref": "#/components/schemas/SearchVASPsResponse"
                }
              }
            },
            "description": "Successful request. Returns an array of VASPs or an empty list if no matches found."
          }
        },
        "summary": "Search for VASPs",
        "tags": [
          "Crypto Funding"
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
      "name": "Crypto Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```