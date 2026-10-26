# Subscribe to System Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetosystemeventv2sse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to System Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to system event updates as they happen in our backend.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can't be used at the same time
- `until` and `until_id` can't be used at the same time
Behavior:
- if `since` or `since_id` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "SystemEventV2": {
        "description": "Represents that system event had occurred and sent over the events streaming api.\n",
        "examples": [
          {
            "at": "2026-01-05T10:28:23.163857Z",
            "description": "End-of-day balances are now available.",
            "event_id": "01F535Y1FVY8WZHE763HCNS8SZ",
            "system_date": "2026-01-05",
            "type": "eod_balances_ready"
          }
        ],
        "properties": {
          "at": {
            "description": "Timestamp of the event",
            "format": "date-time",
            "type": "string"
          },
          "description": {
            "description": "The human readable description of the system event",
            "type": "string"
          },
          "event_id": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "system_date": {
            "description": "the system date to which this system event belongs to",
            "format": "date",
            "type": "string"
          },
          "type": {
            "description": "the machine readable type of the system event",
            "enum": [
              "eod_balances_ready",
              "eod_positions_ready"
            ],
            "type": "string"
          }
        },
        "required": [
          "at",
          "event_id",
          "type",
          "system_date",
          "description"
        ],
        "title": "SystemEvent",
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
    "/v2/events/system": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to system event updates as they happen in our backend.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can't be used at the same time\n- `until` and `until_id` can't be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n",
        "operationId": "subscribeToSystemEventV2SSE",
        "parameters": [
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "since",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "until",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "since_id",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "until_id",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "text/event-stream": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/SystemEventV2"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to System Events (SSE)",
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