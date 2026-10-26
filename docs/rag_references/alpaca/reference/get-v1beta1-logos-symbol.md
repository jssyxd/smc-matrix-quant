# Get Logo

Source: https://docs.alpaca.markets/us/reference/get-v1beta1-logos-symbol.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Logo

Alpaca's Logo API serves uniform logo images for select stock and crypto symbols.

Note: For Logo API pricing details, reach out to sales@alpaca.markets

The API response will return the raw image as a binary

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
    "/v1beta1/logos/{symbol}": {
      "get": {
        "description": "Alpaca's Logo API serves uniform logo images for select stock and crypto symbols.\n\nNote: For Logo API pricing details, reach out to sales@alpaca.markets\n\nThe API response will return the raw image as a binary",
        "operationId": "get-v1beta1-logos-symbol",
        "parameters": [
          {
            "description": "True by default, will return sample placeholder images with the first letter of the asset symbol. If false, 404 will be returned for symbols which do not contain an image.",
            "in": "query",
            "name": "placeholder",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "The API response will return the raw image as a binary"
          }
        },
        "summary": "Get Logo",
        "tags": [
          "Logos"
        ]
      },
      "parameters": [
        {
          "description": "Stock or crypto symbol (e.g. AAPL, BTCUSD, etc.)",
          "in": "path",
          "name": "symbol",
          "required": true,
          "schema": {
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
      "name": "Logos"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```