# Retrieve Announcements

Source: https://docs.alpaca.markets/us/reference/get-v2-corporate_actions-announcements-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Announcements

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
    "/v2/corporate_actions/announcements": {
      "get": {
        "deprecated": true,
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.",
        "operationId": "get-v2-corporate_actions-announcements",
        "parameters": [
          {
            "description": "A comma-delimited list of corporate action types.",
            "explode": false,
            "in": "query",
            "name": "ca_types",
            "required": true,
            "schema": {
              "items": {
                "$ref": "#/components/schemas/CorporateActionCaType"
              },
              "type": "array"
            },
            "style": "form"
          },
          {
            "description": "The start (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "in": "query",
            "name": "since",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The end (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "in": "query",
            "name": "until",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The symbol of the company initiating the announcement.",
            "in": "query",
            "name": "symbol",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The CUSIP of the company initiating the announcement.",
            "in": "query",
            "name": "cusip",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "declaration_date, ex_date, record_date, or payable_date",
            "in": "query",
            "name": "date_type",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "Example 1": {
                    "value": [
                      {
                        "ca_sub_type": "DIV",
                        "ca_type": "Dividend",
                        "cash": "0.018",
                        "corporate_actions_id": "F58684224_XY37",
                        "declaration_date": "2021-01-05",
                        "expiration_date": "2021-01-12",
                        "id": "be3c368a-4c7c-4384-808e-f02c9f5a8afe",
                        "initiating_original_cusip": "55275E101",
                        "initiating_symbol": "MLLAX",
                        "new_rate": "1",
                        "old_rate": "1",
                        "payable_date": "2021-01-14",
                        "record_date": "2021-01-13",
                        "target_original_cusip": "55275E101",
                        "target_symbol": "MLLAX"
                      },
                      {
                        "ca_sub_type": "cash",
                        "ca_type": "Dividend",
                        "cash": "0.145",
                        "corporate_action_id": "48251W104_AD21",
                        "declaration_date": "2021-11-01",
                        "ex_date": "2021-11-12",
                        "initiating_original_cusip": "G52830109",
                        "initiating_symbol": "KKR",
                        "new_rate": "1",
                        "old_rate": "1",
                        "payable_date": "2021-11-30",
                        "record_date": "2021-11-15",
                        "target_original_cusip": "G52830109",
                        "target_symbol": "KKR"
                      }
                    ]
                  }
                },
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/CorporateAnnouncement"
                  },
                  "type": "array"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve Announcements",
        "tags": [
          "Corporate Actions"
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
      "name": "Corporate Actions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```