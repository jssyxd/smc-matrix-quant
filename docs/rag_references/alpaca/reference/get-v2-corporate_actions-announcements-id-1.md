# Retrieve a Specific Announcement

Source: https://docs.alpaca.markets/us/reference/get-v2-corporate_actions-announcements-id-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve a Specific Announcement

This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CorporateActionCaType": {
        "description": "The type of corporate action.",
        "enum": [
          "Spinoff",
          "Merger",
          "Split",
          "Reorg",
          "Dividend"
        ],
        "example": "Dividend",
        "title": "CorporateActionCaType",
        "type": "string"
      },
      "CorporateAnnouncement": {
        "description": "A corporate action announcement.",
        "examples": [
          {
            "ca_sub_type": "DIV",
            "ca_type": "Dividend",
            "cash": "0.018",
            "corporate_action_id": "F58684224_XY37",
            "declaration_date": "2021-01-05",
            "effective_date": "2021-01-08",
            "ex_date": "2021-01-12",
            "id": "be3c368a-4c7c-4384-808e-f02c9f5a8afe",
            "initiating_original_cusip": "55275E101",
            "initiating_symbol": "MLLAX",
            "new_rate": "1",
            "old_rate": "1",
            "payable_date": "2021-01-14",
            "record_date": "2021-01-13",
            "target_original_cusip": "55275E101",
            "target_symbol": "MLLAX"
          }
        ],
        "properties": {
          "ca_sub_type": {
            "type": "string"
          },
          "ca_type": {
            "$ref": "#/components/schemas/CorporateActionCaType"
          },
          "cash": {
            "format": "decimal",
            "type": "string"
          },
          "corporate_action_id": {
            "type": "string"
          },
          "declaration_date": {
            "format": "date",
            "type": "string"
          },
          "effective_date": {
            "format": "date",
            "type": "string"
          },
          "ex_date": {
            "format": "date",
            "type": "string"
          },
          "id": {
            "type": "string"
          },
          "initiating_original_cusip": {
            "type": "string"
          },
          "initiating_symbol": {
            "type": "string"
          },
          "new_rate": {
            "format": "decimal",
            "type": "string"
          },
          "old_rate": {
            "format": "decimal",
            "type": "string"
          },
          "payable_date": {
            "format": "date",
            "type": "string"
          },
          "record_date": {
            "format": "date",
            "type": "string"
          },
          "target_original_cusip": {
            "type": "string"
          },
          "target_symbol": {
            "type": "string"
          }
        },
        "title": "CorporateAnnouncement",
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
    "/v2/corporate_actions/announcements/{id}": {
      "get": {
        "deprecated": true,
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.",
        "operationId": "get-v2-corporate_actions-announcements-id",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CorporateAnnouncement"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve a Specific Announcement",
        "tags": [
          "Corporate Actions"
        ]
      },
      "parameters": [
        {
          "description": "The corporate announcement's id",
          "in": "path",
          "name": "id",
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
      "name": "Corporate Actions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```