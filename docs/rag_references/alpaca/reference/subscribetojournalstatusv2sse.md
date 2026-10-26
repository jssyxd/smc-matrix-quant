# Subscribe to Journal Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetojournalstatusv2sse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Journal Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to journal status updates as they get processed by our backoffice.

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

There is no compatibility between /v1/events/journals/status and /v2/events/journals/status, the ids (ulid) are always different, and the number of events might also different

Please note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.
We encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.
In the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "JournalEntryType": {
        "description": "This enum represents the various kinds of Journal alpaca supports.\n\nCurrent values are:\n\n- **JNLC**\n\n  Journal Cash between accounts\n\n- **JNLS**\n\n  Journal Securities between accounts",
        "enum": [
          "JNLC",
          "JNLS"
        ],
        "title": "",
        "type": "string"
      },
      "JournalStatus": {
        "description": "Represents the status that a Journal instance can be in.\n\n**Current Values**\n\nqueued\tJournal in queue to be processed. Journal is not processed yet.\n\nsent_to_clearing\tJournal sent to be processed by Alpaca's booking system. The journal is not processed yet.\n\npending\t    Journal pending to be processed as it requires manual approval from Alpaca operations (for example due to hitting JNLC daily limits).\n\nexecuted\tJournal executed and balances updated for both sides of \nthe journal transaction. This is not a final status, journals can be reversed if there is an error.\n\nactivity_created\tNon-trade activity has been created for journal (JNLC v2-only).\n\nrejected\tJournal rejected. Please try again.\n\ncanceled\tJournal canceled. This is a **FINAL** status.\n\nrefused\tJournal refused. Please try again.\n\ndeleted\tJournal deleted. This is a **FINAL** status.\n\ncorrect\tJournal is corrected. Previously executed journal is cancelled and a new journal is corrected amount is created. This is a **FINAL** status.",
        "enum": [
          "pending",
          "canceled",
          "executed",
          "activity_created",
          "queued",
          "rejected",
          "deleted",
          "refused",
          "sent_to_clearing",
          "correct"
        ],
        "type": "string"
      },
      "JournalStatusEventV2": {
        "description": "Represents a change in a Journal's status, sent over the events streaming api.\n",
        "examples": [
          {
            "at": "2021-05-07T10:28:23.163857Z",
            "description": "Journal of cash between accounts",
            "entry_type": "JNLC",
            "event_id": "01F535Y1FVY8WZHE763HCNS8SZ",
            "journal_id": "2f144d2a-91e6-46ff-8e37-959a701cc58d",
            "status_from": "",
            "status_to": "queued"
          },
          {
            "at": "2021-05-07T10:28:23.163857Z",
            "description": "Journal of cash between accounts",
            "entry_type": "JNLC",
            "event_id": "01F535Y1FVY8WZHE763HCNS8SZ",
            "idempotency_key": "72bdf18f-7410-43ec-b4e8-b6e41c5c0160",
            "idempotency_key_type": "single",
            "journal_id": "2f144d2a-91e6-46ff-8e37-959a701cc58d",
            "status_from": "queued",
            "status_to": "executed"
          }
        ],
        "properties": {
          "at": {
            "description": "Timestamp of event",
            "format": "date-time",
            "minLength": 1,
            "type": "string"
          },
          "batch_error_message": {
            "description": "If journal submitted in batch (that is, idempotency_key_type is batch), this is the error message of the batch journal execution.",
            "type": "string"
          },
          "description": {
            "description": "The description of the journal event when submitted",
            "example": "Journal of cash between accounts",
            "type": "string"
          },
          "entry_type": {
            "$ref": "#/components/schemas/JournalEntryType"
          },
          "event_id": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "idempotency_key": {
            "description": "The idempotency key of the journal event",
            "format": "uuid",
            "type": "string"
          },
          "idempotency_key_type": {
            "description": "The type of idempotency key",
            "enum": [
              "single",
              "batch"
            ],
            "type": "string"
          },
          "journal_id": {
            "description": "The UUID of the related Journal",
            "format": "uuid",
            "type": "string"
          },
          "status_from": {
            "$ref": "#/components/schemas/JournalStatusFrom"
          },
          "status_to": {
            "$ref": "#/components/schemas/JournalStatus"
          }
        },
        "required": [
          "at",
          "entry_type",
          "event_id",
          "journal_id",
          "status_from",
          "status_to"
        ],
        "title": "JournalStatusEvent",
        "type": "object"
      },
      "JournalStatusFrom": {
        "description": "Previous journal status in stream status-change events. Empty string is used for the initial status-change event when there is no previous status.",
        "oneOf": [
          {
            "$ref": "#/components/schemas/JournalStatus"
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
    "/v2/events/journals/status": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to journal status updates as they get processed by our backoffice.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can't be used at the same time\n- `until` and `until_id` can't be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nThere is no compatibility between /v1/events/journals/status and /v2/events/journals/status, the ids (ulid) are always different, and the number of events might also different\n\nPlease note that the new `/v2` endpoint, is the same as, and was originally available under `/v2beta1`.\nWe encourage all customers to adjust their codebase from that interim beta endpoint to the `/v2` stable endpoint.\nIn the near future we will setup permanent redirect from `/v2beta1` to `/v2` before we completely remove the beta endpoint.\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n",
        "operationId": "subscribeToJournalStatusV2SSE",
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
          },
          {
            "in": "query",
            "name": "id",
            "schema": {
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
                    "$ref": "#/components/schemas/JournalStatusEventV2"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to Journal Events (SSE)",
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