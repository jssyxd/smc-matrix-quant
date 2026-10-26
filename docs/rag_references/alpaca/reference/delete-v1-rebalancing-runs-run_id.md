# Cancel Run by ID

Source: https://docs.alpaca.markets/us/reference/delete-v1-rebalancing-runs-run_id.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Cancel Run by ID

Cancels a run. Only runs within certain statuses (QUEUED, CANCELED, SELLS_IN_PROGRESS, BUYS_IN_PROGRESS) are cancelable. If this endpoint is called after orders have been submitted, we'll attempt to cancel the orders.

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
    "/v1/rebalancing/runs/{run_id}": {
      "delete": {
        "description": "Cancels a run. Only runs within certain statuses (QUEUED, CANCELED, SELLS_IN_PROGRESS, BUYS_IN_PROGRESS) are cancelable. If this endpoint is called after orders have been submitted, we'll attempt to cancel the orders.",
        "operationId": "delete-v1-rebalancing-runs-run_id",
        "responses": {
          "204": {
            "description": "No Content"
          }
        },
        "summary": "Cancel Run by ID",
        "tags": [
          "Rebalancing"
        ]
      },
      "parameters": [
        {
          "description": "the id of the portfolio run",
          "in": "path",
          "name": "run_id",
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