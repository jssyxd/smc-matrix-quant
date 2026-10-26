# Subscribe to Funding Status Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetofundingstatussse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Funding Status Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to funding status updates as they get processed by our backoffice, for both end-user and firm accounts.

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
      "StatusFundingEvent": {
        "description": "Represents a change in a Funding entity's status, sent over the events streaming api. Currently, the suppported entities are: bank relationships, bank wires, transfers and funding wallets.",
        "examples": [
          {
            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
            "at": "2025-04-11T19:52:24.066998Z",
            "correspondent": "LPCA",
            "entity_id": "c4ed4206-697b-4859-ab71-b9de6649859d",
            "entity_type": "BankRelationship",
            "event_id": "01F7VQQ782DM57SJNWAYMD14J9",
            "status_to": "QUEUED"
          },
          {
            "account_id": "8e00606a-c9ac-409a-ba45-f55e8f77984a",
            "at": "2025-04-11T19:52:24.066998Z",
            "correspondent": "LPCA",
            "entity_id": "c4ed4206-697b-4859-ab71-b9de6649859d",
            "entity_type": "BankRelationship",
            "event_id": "01F7VQQ782DM57SJNWAYMD14J9",
            "reason": "bank account owner name does not match brokerage account name",
            "status_from": "QUEUED",
            "status_to": "REJECTED"
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
            "minLength": 1,
            "type": "string"
          },
          "correspondent": {
            "description": "Correspondent's code",
            "format": "ABCD",
            "maxLength": 4,
            "minLength": 1,
            "type": "string"
          },
          "entity_id": {
            "description": "Entity's UUID",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "entity_type": {
            "description": "Valid values are BankRelationship, WireBank, Transfer and FundingWallet.",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "event_id": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "minLength": 1,
            "type": "string"
          },
          "reason": {
            "description": "Used when an a bank relationship is rejected, a wire bank is canceled, etc.",
            "type": "string"
          },
          "status_from": {
            "description": "Valid values are based on entity type:\n- BankRelationship:\n  - QUEUED\n  - CANCEL_REQUESTED\n  - CANCEL_SENT\n  - CANCEL_FAILED\n  - PENDING\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- WireBank:\n  - QUEUED\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- Transfer:\n  - QUEUED\n  - APPROVAL_PENDING\n  - CANCELED\n  - EXPIRED\n  - APPROVED\n  - REJECTED\n  - SENT_TO_CLEARING\n  - COMPLETE\n  - RETURNED\n- FundingWallet:\n  - active\n  - pending\n",
            "type": "string"
          },
          "status_to": {
            "description": "Valid values are based on entity type:\n- BankRelationship:\n  - QUEUED\n  - CANCEL_REQUESTED\n  - CANCEL_SENT\n  - CANCEL_FAILED\n  - PENDING\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- WireBank:\n  - QUEUED\n  - SENT_TO_CLEARING\n  - APPROVED\n  - CANCELED\n  - REJECTED\n- Transfer:\n  - QUEUED\n  - APPROVAL_PENDING\n  - CANCELED\n  - EXPIRED\n  - APPROVED\n  - REJECTED\n  - SENT_TO_CLEARING\n  - COMPLETE\n  - RETURNED\n- FundingWallet:\n  - active\n  - pending\n",
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "event_id",
          "at",
          "account_id",
          "correspondent",
          "entity_id",
          "entity_type",
          "status_to"
        ],
        "title": "StatusFundingEvent",
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
    "/v2/events/funding/status": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to funding status updates as they get processed by our backoffice, for both end-user and firm accounts.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can't be used at the same time\n- `until` and `until_id` can't be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.",
        "operationId": "subscribeToFundingStatusSSE",
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
                    "$ref": "#/components/schemas/StatusFundingEvent"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to Funding Status Events (SSE)",
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