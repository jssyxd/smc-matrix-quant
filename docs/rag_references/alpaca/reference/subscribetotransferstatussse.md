# Subscribe to Transfer Events (SSE) (Legacy)

Source: https://docs.alpaca.markets/us/reference/subscribetotransferstatussse.md

---
updatedAt: 2026-05-27T17:58:38.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Transfer Events (SSE) (Legacy)

**Deprecation notice**

As part of the deprecation process, the legacy transfer events API is now only available for existing broker-partners at `GET /v1/events/transfers/status` and for compatibility reasons.

All new broker partners will not have the option to use the legacy transfer events endpoint.

They should integrate with the new `/v2/events/funding/status` endpoint instead.

Also, all existing broker partners are now recommended to upgrade to the `/v2/events/funding/status` endpoint, which provides faster event delivery times.

---

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to transfer status updates as they get processed by our backoffice, for both end-user and firm accounts.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since_ulid` required if `until_ulid` specified
- `since`, `since_id` or `since_ulid`  can't be used at the same time
Behavior:
- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data
- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "TransferStatus": {
        "description": "- **QUEUED**\nTransfer is in queue to be processed.\n- **APPROVAL_PENDING**\nTransfer is pending approval.\n- **PENDING**\nTransfer is pending processing.\n- **SENT_TO_CLEARING**\nTransfer is being processed by the clearing firm.\n- **REJECTED**\nTransfer is rejected.\n- **CANCELED**\nClient initiated transfer cancellation.\n- **APPROVED**\nTransfer is approved.\n- **COMPLETE**\nTransfer is completed.\n- **RETURNED**\nThe bank issued an ACH return for the transfer.\n",
        "enum": [
          "QUEUED",
          "APPROVAL_PENDING",
          "PENDING",
          "SENT_TO_CLEARING",
          "REJECTED",
          "CANCELED",
          "APPROVED",
          "COMPLETE",
          "RETURNED"
        ],
        "example": "QUEUED",
        "type": "string"
      },
      "TransferStatusEvent": {
        "description": "Represents a change in a Transfer's status, sent over the events streaming api.",
        "examples": [
          {
            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
            "at": "2021-06-10T19:52:24.066998Z",
            "event_id": 15961,
            "event_ulid": "01F7VQQ782DM57SJNWAYMD14J9",
            "status_from": "QUEUED",
            "status_to": "SENT_TO_CLEARING",
            "transfer_id": "c4ed4206-697b-4859-ab71-b9de6649859d"
          },
          {
            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
            "at": "2021-06-10T20:02:24.280178Z",
            "event_id": 15962,
            "event_ulid": "01F7VQQ782DM57SJNWAYMD14JA",
            "status_from": "SENT_TO_CLEARING",
            "status_to": "COMPLETE",
            "transfer_id": "c4ed4206-697b-4859-ab71-b9de6649859d"
          }
        ],
        "properties": {
          "account_id": {
            "description": "Account UUID",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "at": {
            "description": "Timestamp of when the transfer status changed",
            "format": "date-time",
            "minLength": 1,
            "type": "string"
          },
          "event_id": {
            "description": "Monotonically increasing 64-bit integer not available to new partners, and for backward compatibility purposes only; use `event_ulid` as the stable identifier where possible\n",
            "type": "integer"
          },
          "event_ulid": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "status_from": {
            "$ref": "#/components/schemas/TransferStatusFrom"
          },
          "status_to": {
            "$ref": "#/components/schemas/TransferStatus"
          },
          "transfer_id": {
            "description": "Transfer UUID",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "account_id",
          "at",
          "event_ulid",
          "status_from",
          "status_to",
          "transfer_id"
        ],
        "title": "TransferStatusEvent",
        "type": "object"
      },
      "TransferStatusFrom": {
        "description": "Previous transfer status in stream status-change events. Empty string is used for the initial status-change event when there is no previous status.",
        "oneOf": [
          {
            "$ref": "#/components/schemas/TransferStatus"
          },
          {
            "enum": [
              ""
            ],
            "type": "string"
          }
        ]
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
    "/v1/events/transfers/status": {
      "get": {
        "deprecated": true,
        "description": "**Deprecation notice**\n\nAs part of the deprecation process, the legacy transfer events API is now only available for existing broker-partners at `GET /v1/events/transfers/status` and for compatibility reasons.\n\nAll new broker partners will not have the option to use the legacy transfer events endpoint.\n\nThey should integrate with the new `/v2/events/funding/status` endpoint instead.\n\nAlso, all existing broker partners are now recommended to upgrade to the `/v2/events/funding/status` endpoint, which provides faster event delivery times.\n\n---\n\nThe Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to transfer status updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since_ulid` required if `until_ulid` specified\n- `since`, `since_id` or `since_ulid`  can't be used at the same time\nBehavior:\n- if `since`, `since_id` or `since_ulid` not specified this will not return any historic data\n- if `until`, `until_id` or `until_ulid` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.",
        "operationId": "subscribeToTransferStatusSSE",
        "parameters": [
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
          }
        ],
        "responses": {
          "200": {
            "content": {
              "text/event-stream": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/TransferStatusEvent"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          },
          "410": {
            "description": "Deprecated. The endpoint is not available for this partner."
          }
        },
        "summary": "Subscribe to Transfer Events (SSE) (Legacy)",
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