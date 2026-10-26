# Cancel a Pending Journal

Source: https://docs.alpaca.markets/us/reference/deletejournalbyid.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Cancel a Pending Journal

You can only delete a journal if the journal is still in a pending state, if a journal is executed you will not be able to delete. The alternative is to create a mirror journal entry to reverse the flow of funds.

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
    "/v1/journals/{journal_id}": {
      "delete": {
        "description": "You can only delete a journal if the journal is still in a pending state, if a journal is executed you will not be able to delete. The alternative is to create a mirror journal entry to reverse the flow of funds.",
        "operationId": "deleteJournalById",
        "responses": {
          "204": {
            "description": "The cancel request succeeded. (No-content)\n"
          },
          "404": {
            "description": "The journal is not found.\n"
          },
          "422": {
            "description": "The journal is not in the pending status.\n"
          }
        },
        "summary": "Cancel a Pending Journal",
        "tags": [
          "Journals"
        ]
      },
      "parameters": [
        {
          "in": "path",
          "name": "journal_id",
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
      "name": "Journals"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```