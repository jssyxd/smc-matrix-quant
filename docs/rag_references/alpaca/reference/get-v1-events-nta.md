# Subscribe to Non-Trading Activities Events (SSE)

Source: https://docs.alpaca.markets/us/reference/get-v1-events-nta.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Non-Trading Activities Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to non-trading activities updates as they get processed by our backoffice, for both end-user and firm accounts.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

You can listen to when NTAs are pushed such as CSDs, JNLC (journals) or FEEs.

Query Params Rules:
- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since_ulid` required if `until_ulid` specified
- `since`, `since_id` or `since_ulid`  can't be used at the same time
Behavior:
- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data
- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)'

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "NonTradeActivityEvent": {
        "description": "Represents a non-trade activity SSE event",
        "examples": [
          {
            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
            "at": "2024-11-26T15:25:17.803914Z",
            "description": "",
            "entry_type": "JNLC",
            "event_ulid": "01JDMH7BKCCB4XY5F11HN63NZX",
            "id": "afb78fa2-7e4c-4e0a-bca2-2e0d26a87f88",
            "net_amount": 10,
            "qty": 0,
            "settle_date": "2024-11-26",
            "status": "executed",
            "symbol": "",
            "system_date": "2024-11-26"
          },
          {
            "account_id": "11629972-5fd6-4e14-ad9e-0f0cabd2777f",
            "at": "2024-11-12T01:15:53.132425Z",
            "description": "TAF fee for proceed of 0.010052895 shares (1 trades) on 2024-11-11 by 613651765",
            "entry_sub_type": "TAF",
            "entry_type": "FEE",
            "event_ulid": "01JCEZ1ZDCE44GFX6WZ75N4199",
            "id": "d96cea8a-6a77-46cd-bb7b-df6d74442653",
            "net_amount": -0.01,
            "qty": 0,
            "settle_date": "2024-11-12",
            "status": "executed",
            "symbol": "",
            "system_date": "2024-11-11"
          }
        ],
        "properties": {
          "account_id": {
            "description": "Account UUID",
            "format": "uuid",
            "type": "string"
          },
          "at": {
            "description": "Timestamp of when the event was emitted",
            "format": "date-time",
            "type": "string"
          },
          "cusip": {
            "description": "CUSIP the event is associated with, not present when no CUSIP is applicable",
            "example": "037833100",
            "type": "string"
          },
          "description": {
            "description": "Additional information about the event, empty string if not applicable",
            "example": "Example description",
            "type": "string"
          },
          "entry_type": {
            "description": "Type of entry for e.g JNLC, FEE, INT, DIVNRA etc",
            "example": "JNLC",
            "type": "string"
          },
          "event_id": {
            "description": "Monotonically increasing 64bit integer",
            "type": "integer"
          },
          "event_ulid": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "id": {
            "description": "Record UUID",
            "format": "uuid",
            "type": "string"
          },
          "net_amount": {
            "description": "Net amount if applicable, 0 otherwise",
            "example": 1,
            "format": "decimal",
            "type": "number"
          },
          "per_share_amount": {
            "description": "Per share amount if applicable",
            "example": 0.3,
            "format": "decimal",
            "type": "number"
          },
          "price": {
            "description": "Price if applicable.",
            "example": "0.38921",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "Quantity of the stock affected. 0 for cash events",
            "format": "decimal",
            "type": "number"
          },
          "settle_date": {
            "description": "Date of settlement if applicable",
            "format": "date",
            "type": "string"
          },
          "status": {
            "description": "Status of the event. `pending` is an internal/preprocessing status for journal-type NTAs and is only emitted when the subscriber opts in with `include_preprocessing=true`.\n",
            "enum": [
              "executed",
              "correct",
              "canceled",
              "pending"
            ],
            "example": "executed",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol the event is associated with, empty string when no symbol is applicable",
            "example": "AAPL",
            "type": "string"
          },
          "system_date": {
            "description": "Date of the event recorded in the system",
            "format": "date",
            "type": "string"
          }
        },
        "required": [
          "account_id",
          "at",
          "id",
          "event_ulid",
          "system_date",
          "settle_date",
          "net_amount",
          "entry_type",
          "description"
        ],
        "title": "NonTradeActivityEvent",
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
    "/v1/events/nta": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to non-trading activities updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nYou can listen to when NTAs are pushed such as CSDs, JNLC (journals) or FEEs.\n\nQuery Params Rules:\n- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since_ulid` required if `until_ulid` specified\n- `since`, `since_id` or `since_ulid`  can't be used at the same time\nBehavior:\n- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data\n- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)'",
        "operationId": "get-v1-events-nta",
        "parameters": [
          {
            "in": "query",
            "name": "id",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "since",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "until",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "deprecated": true,
            "in": "query",
            "name": "since_id",
            "schema": {
              "type": "integer"
            },
            "x-deprecation": {
              "reason": "Use since_ulid instead.",
              "since": "2023-08-01",
              "sunset": "2027-02-15"
            }
          },
          {
            "deprecated": true,
            "in": "query",
            "name": "until_id",
            "schema": {
              "type": "integer"
            },
            "x-deprecation": {
              "reason": "Use until_ulid instead.",
              "since": "2023-08-01",
              "sunset": "2027-02-15"
            }
          },
          {
            "in": "query",
            "name": "since_ulid",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "until_ulid",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "include_preprocessing",
            "schema": {
              "type": "boolean"
            }
          },
          {
            "description": "ID used to link activities who share a sibling relationship",
            "in": "query",
            "name": "group_id",
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/NonTradeActivityEvent"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Subscribe to Non-Trading Activities Events (SSE)",
        "tags": [
          "Events"
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
      "name": "Events"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```