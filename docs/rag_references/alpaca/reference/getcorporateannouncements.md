# Retrieve Announcements

Source: https://docs.alpaca.markets/us/reference/getcorporateannouncements.md

---
updatedAt: 2026-05-27T17:58:38.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Announcements

This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.

# OpenAPI definition

```json
{
  "components": {
    "responses": {
      "BadRequest": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "Malformed input."
      }
    },
    "schemas": {
      "Announcement": {
        "description": "The announcements endpoint contains public information on previous and upcoming dividends, mergers, spinoffs, and stock splits.\n\nAnnouncement data is made available through the API as soon as it is ingested by Alpaca, which is typically the following trading day after the declaration date. This provides insight into future account stock position and cash balance changes that will take effect on an announcement's payable date. Additionally, viewing previous announcement details can improve bookkeeping and reconciling previous account cash and position changes.",
        "examples": [
          {
            "ca_sub_type": "cash",
            "ca_type": "dividend",
            "cash": "0",
            "corporate_action_id": "78467X109_AA22",
            "declaration_date": "2021-12-19",
            "ex_date": "2022-01-21",
            "id": "bebc5ece-34be-47e9-b944-687e69a102be",
            "initiating_original_cusip": "252787106",
            "initiating_symbol": "DIA",
            "new_rate": "1",
            "old_rate": "1",
            "payable_date": "2022-02-14",
            "record_date": "2022-01-24",
            "target_original_cusip": "252787106",
            "target_symbol": "DIA"
          }
        ],
        "properties": {
          "ca_sub_type": {
            "$ref": "#/components/schemas/AnnouncementCASubType"
          },
          "ca_type": {
            "$ref": "#/components/schemas/AnnouncementCAType"
          },
          "cash": {
            "description": "The amount of cash to be paid per share held by an account on the record date.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "corporate_action_id": {
            "description": "ID that remains consistent across all announcements for the same corporate action. Unlike 'id', this can be used to connect multiple announcements to see how the terms have changed throughout the lifecycle of the corporate action event.",
            "minLength": 1,
            "type": "string"
          },
          "declaration_date": {
            "description": "Date the corporate action or subsequent terms update was announced.",
            "minLength": 1,
            "type": "string"
          },
          "ex_date": {
            "description": "The first date that purchasing a security will not result in a corporate action entitlement.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "id": {
            "description": "ID that is specific to a single announcement.",
            "minLength": 1,
            "type": "string"
          },
          "initiating_original_cusip": {
            "description": "CUSIP of the company initiating the announcement.",
            "minLength": 1,
            "type": "string"
          },
          "initiating_symbol": {
            "description": "Symbol of the company initiating the announcement.",
            "minLength": 1,
            "type": "string"
          },
          "new_rate": {
            "description": "The numerator to determine any quantity change ratios in positions.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "old_rate": {
            "description": "The denominator to determine any quantity change ratios in positions.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "payable_date": {
            "description": "The date the announcement will take effect. On this date, account stock and cash balances are expected to be processed accordingly.",
            "minLength": 1,
            "type": "string"
          },
          "record_date": {
            "description": "The date an account must hold a settled position in the security in order to receive the corporate action entitlement.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "target_original_cusip": {
            "description": "CUSIP of the child company involved in the announcement.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          },
          "target_symbol": {
            "description": "Symbol of the child company involved in the announcement.",
            "minLength": 1,
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [
          "id",
          "corporate_action_id",
          "ca_type",
          "ca_sub_type",
          "initiating_symbol",
          "initiating_original_cusip",
          "target_symbol",
          "target_original_cusip",
          "declaration_date",
          "ex_date",
          "record_date",
          "payable_date",
          "cash",
          "old_rate",
          "new_rate"
        ],
        "title": "Announcement",
        "type": "object"
      },
      "AnnouncementCASubType": {
        "description": "Announcements have both a type and a subtype to categorize them. This model represents the lowever level abstract \"sub types\" of Announcement. Please see the AnnouncementCAType model for higher level descriptions of the possible types\n\nPossible values are:\n\n- from the `dividend` type:\n  - **cash**\n\n    A cash payment based on the number of shares the account holds on the record date.\n  - **stock**\n\n    A stock payment based on the number of shares the account holds on the record date.\n\n- from the `merger` type:\n  - **merger_update**\n\n    An update to the terms of an upcoming merger. This can happen any number of times before the merger is completed and can be tracked by using the id parameter.\n\n  - **merger_completion**\n\n    A final update in the terms of the merger in which the intiating_symbol will acquire the target_symbol. Any previous terms updates for this announcement will have the same id value.\n\n- from the `split` type:\n  - **stock_split**\n\n    An increase in the number of shares outstanding with a decrease in the dollar value of each share. The new_rate and old_rate parameters will be returned in order to derive the ratio of the split\n  - **until_split**\n\n    An increase in the number of shares outstanding with a decrease in the dollar value of each share. The new_rate and old_rate parameters will be returned in order to derive the ratio of the split.\n  - **reverse_split**\n\n    A decrease in the number of shares outstanding with an increase in the dollar value of each share. The new_rate and old_rate parameters will be returned in order to derive the ratio of the spli\n  - **recapitalization**\n\n    A stock recapitalization, typically used by a company to adjust debt and equity ratios.\n\n- from the `spinoff` type:\n  - **spinoff**\n\n    A disbursement of a newly tradable security when the intiating_symbol creates the target_symbol.",
        "enum": [
          "cash",
          "stock",
          "merger_update",
          "merger_completion",
          "stock_split",
          "until_split",
          "reverse_split",
          "recapitalization",
          "spinoff"
        ],
        "title": "",
        "type": "string"
      },
      "AnnouncementCAType": {
        "description": "Announcements have both a type and a subtype to categorize them. This model represents the higher level abstract \"types\" of Announcement. Please see the AnnouncementCASubType model for finer grain descriptions of the subtypes\n\nPossible values are:\n- dividend\n  can have `cash` and `stock` subtypes\n- merger\n  has `merger_update` and `merger_completion` sub types\n- split\n  has `stock_split`, `until_split`, `reverse_split`, and `recapitalization` sub types\n- spinoff\n  currently has only the `spinoff` subtype and thus is just this higher level category for now. A disbursement of a newly tradable security when the intiating_symbol creates the target_symbol.",
        "enum": [
          "dividend",
          "merger",
          "split",
          "spinoff"
        ],
        "example": "dividend",
        "title": "",
        "type": "string"
      },
      "Error": {
        "properties": {
          "code": {
            "type": "number"
          },
          "message": {
            "type": "string"
          }
        },
        "required": [
          "code",
          "message"
        ],
        "title": "Error",
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
    "/v1/corporate_actions/announcements": {
      "get": {
        "deprecated": true,
        "description": "This endpoint is deprecated, please use [the new corporate actions endpoint](https://docs.alpaca.markets/reference/corporateactions-1) instead.",
        "operationId": "getCorporateAnnouncements",
        "parameters": [
          {
            "description": "A comma-delimited list of CorporateActionType values",
            "in": "query",
            "name": "ca_types",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The start (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "in": "query",
            "name": "since",
            "required": true,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "The end (inclusive) of the date range when searching corporate action announcements. This should follow the YYYY-MM-DD format. The date range is limited to 90 days.",
            "in": "query",
            "name": "until",
            "required": true,
            "schema": {
              "format": "date",
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
            "description": "An emum of possible ways to use the `since` and `until` parameters to search by.\n\nthe types are:\n\n- **declaration_date**: The date of the preliminary announcement details or the date that any subsequent term updates took place.\n- **ex_date**: The date on which any security purchasing activity will not result in a corporate action entitlement. Any selling activity that takes place on or after this date will result in a corporate action entitlement.\n- **record_date**: The date the company checks its records to determine who is shareholder in order to allocate entitlements.\n- **payable_date**: The date that the stock and cash positions will update according to the account positions as of the record date.",
            "in": "query",
            "name": "date_type",
            "schema": {
              "enum": [
                "declaration_date",
                "ex_date",
                "record_date",
                "payable_date"
              ],
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Announcement"
                  },
                  "type": "array"
                }
              }
            },
            "description": "OK"
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
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
      "name": "Corporate Actions"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```