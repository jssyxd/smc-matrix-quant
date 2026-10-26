# Inactivate Portfolio By ID

Source: https://docs.alpaca.markets/us/reference/delete-v1-rebalancing-portfolios-portfolio_id.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Inactivate Portfolio By ID

Archives a portfolio (soft delete). Only permitted when the portfolio has no active subscriptions. Archived portfolios are hidden from the default list response and cannot be used for new subscriptions.

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
    "/v1/rebalancing/portfolios/{portfolio_id}": {
      "delete": {
        "description": "Archives a portfolio (soft delete). Only permitted when the portfolio has no active subscriptions. Archived portfolios are hidden from the default list response and cannot be used for new subscriptions.",
        "operationId": "delete-v1-rebalancing-portfolios-portfolio_id",
        "responses": {
          "204": {
            "description": "No Content"
          },
          "400": {
            "description": "Bad Request"
          },
          "422": {
            "description": "Unprocessable Entity "
          }
        },
        "summary": "Inactivate Portfolio By ID",
        "tags": [
          "Rebalancing"
        ]
      },
      "parameters": [
        {
          "description": "The Portfolio ID",
          "in": "path",
          "name": "portfolio_id",
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
      "name": "Rebalancing"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```