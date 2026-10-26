# Subscribe to Admin Action Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetoadminactionsse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Admin Action Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

This endpoint streams events related to administrative actions performed by our systems.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can't be used at the same time
Behavior:
- if `since` or `since_id` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

Warning: Currently OAS-3 doesn't have full support for representing SSE style responses from an API.

In case the client code is generated from this OAS spec, don't specify a `since` and `until` there is a good chance the generated clients will hang forever waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific endpoint until the OAS-3 standards come to a consensus on how to represent this behavior in OAS-3.

---

###  Comment messages
According to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.

#####  Slow client

The server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`

##### Internal server error

An error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`

---

**Event Types**

- **LegacyNote:** Old free text based admin notes
- **Liquidation:** Event for a position liquidation which initialized by an admin
- **TransactionCancel:** Event for a manually cancelled transaction

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AdminActionBelongsTo": {
        "description": "Represents structure of an Identifier for all AdminAction type",
        "properties": {
          "id_reference": {
            "type": "string"
          },
          "kind": {
            "$ref": "#/components/schemas/AdminActionBelongsToKind"
          }
        },
        "title": "AdminActionBelongsTo",
        "type": "object"
      },
      "AdminActionBelongsToKind": {
        "enum": [
          "account",
          "owner",
          "correspondent"
        ]
      },
      "AdminActionCategory": {
        "description": "Category of the Admin Action",
        "enum": [
          "accounts",
          "order",
          "other"
        ]
      },
      "AdminActionCreatedBy": {
        "description": "Represents structure of an Creator's Identifier for all AdminAction type\n",
        "properties": {
          "id_reference": {
            "type": "string"
          },
          "kind": {
            "$ref": "#/components/schemas/AdminActionCreatedByKind"
          }
        },
        "title": "AdminActionCreatedBy",
        "type": "object"
      },
      "AdminActionCreatedByKind": {
        "enum": [
          "admin"
        ]
      },
      "AdminActionEventGeneral": {
        "description": "Represents general fields for all AdminAction type",
        "properties": {
          "at": {
            "description": "Timestamp of event",
            "format": "date-time",
            "type": "string"
          },
          "belongs_to": {
            "$ref": "#/components/schemas/AdminActionBelongsTo"
          },
          "category": {
            "$ref": "#/components/schemas/AdminActionCategory"
          },
          "correspondent": {
            "description": "Related correspondent",
            "type": "string"
          },
          "created_by": {
            "$ref": "#/components/schemas/AdminActionCreatedBy"
          },
          "event_id": {
            "description": "Lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "note": {
            "description": "Free text form description of the admin action",
            "type": "string"
          },
          "replaces_event_id": {
            "description": "Id of the replaced event (optional)",
            "format": "ulid",
            "type": "string"
          },
          "type": {
            "$ref": "#/components/schemas/AdminActionType"
          },
          "visibility": {
            "$ref": "#/components/schemas/AdminActionVisibility"
          }
        },
        "required": [
          "event_id",
          "at",
          "belongs_to",
          "created_by",
          "type",
          "category",
          "visibility",
          "note",
          "correspondent"
        ],
        "title": "AdminActionEvent",
        "type": "object"
      },
      "AdminActionLegacyNote": {
        "allOf": [
          {
            "$ref": "#/components/schemas/AdminActionEventGeneral"
          },
          {
            "properties": {
              "context": {
                "description": "Variable schema type which depends on the type",
                "type": "object"
              }
            },
            "required": [
              "context"
            ],
            "title": "AdminActionContextLegacyNote",
            "type": "object"
          }
        ],
        "description": "Represents structure of a LegacyNote type AdminAction",
        "examples": [
          {
            "at": "2023-03-06T16:38:01Z",
            "belongs_to": {
              "kind": "account",
              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
            },
            "category": "other",
            "context": {},
            "correspondent": "LPCA",
            "created_by": {
              "kind": "admin",
              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
            },
            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
            "note": "Performed action: Positions split AMZN (long): 1.011266402\n",
            "type": "legacy_note_admin_event",
            "visibility": "internal"
          }
        ]
      },
      "AdminActionLiquidation": {
        "allOf": [
          {
            "$ref": "#/components/schemas/AdminActionEventGeneral"
          },
          {
            "properties": {
              "context": {
                "description": "Variable schema type which depends on the type",
                "properties": {
                  "available_qty": {
                    "format": "decimal",
                    "type": "string"
                  },
                  "error": {
                    "type": "string"
                  },
                  "reason": {
                    "type": "string"
                  },
                  "requested_qty": {
                    "format": "decimal",
                    "type": "string"
                  },
                  "symbol": {
                    "type": "string"
                  }
                },
                "type": "object"
              }
            },
            "required": [
              "context"
            ],
            "title": "AdminActionContextLiquidation",
            "type": "object"
          }
        ],
        "description": "Represents structure of a Liquidation type AdminAction",
        "examples": [
          {
            "at": "2023-03-06T16:38:01Z",
            "belongs_to": {
              "kind": "account",
              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
            },
            "category": "accounts",
            "context": {
              "available_qty": "0.0001",
              "error": "",
              "reason": "Liquidation due to real time risk",
              "requested_qty": "0.0001",
              "symbol": "TSLA"
            },
            "correspondent": "LPCA",
            "created_by": {
              "kind": "admin",
              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
            },
            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
            "note": "Performed action: Position liquidated: Asset: TSLA, Quantity: 0.0001, Reason: Liquidation due to real time risk\n",
            "type": "liquidation_admin_event",
            "visibility": "external"
          }
        ]
      },
      "AdminActionTransactionCancel": {
        "allOf": [
          {
            "$ref": "#/components/schemas/AdminActionEventGeneral"
          },
          {
            "properties": {
              "context": {
                "description": "Variable schema type which depends on the type",
                "properties": {
                  "entry_type": {
                    "type": "string"
                  },
                  "external_id": {
                    "type": "string"
                  },
                  "transaction_id": {
                    "format": "uuid",
                    "type": "string"
                  }
                },
                "type": "object"
              }
            },
            "required": [
              "context"
            ],
            "title": "AdminActionContextTransactionCancel",
            "type": "object"
          }
        ],
        "description": "Represents structure of a TransactionCancel type AdminAction",
        "examples": [
          {
            "at": "2023-03-06T16:38:01Z",
            "belongs_to": {
              "kind": "account",
              "value": "0bbf1dd7-4235-4eca-8b1a-0db63572c735"
            },
            "category": "accounts",
            "context": {
              "entry_type": "JNLC",
              "external_id": "d5eede2c-1c08-45df-9800-87ad5eefc11f",
              "transaction_id": "fdf18af2-142b-409e-8aad-d1731e276af0"
            },
            "correspondent": "LPCA",
            "created_by": {
              "kind": "admin",
              "value": "19455a3c-595f-457f-97b3-64a2b5aeae96"
            },
            "event_id": "01GTVS4FVS2KJDTPYH2WM6NAXF",
            "note": "\"Transaction fdf18af2-142b-409e-8aad-d1731e276af0 cancelled for LPCA-12345678\n",
            "type": "transaction_cancel_admin_event",
            "visibility": "external"
          }
        ]
      },
      "AdminActionType": {
        "description": "Type of the Admin Action",
        "enum": [
          "liquidation_admin_event",
          "legacy_note_admin_event",
          "transaction_cancel_admin_event"
        ]
      },
      "AdminActionVisibility": {
        "description": "Visibility of the Admin Action",
        "enum": [
          "internal",
          "external",
          "correspondent_only"
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
    "/v2/events/admin-actions": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nThis endpoint streams events related to administrative actions performed by our systems.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can't be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nWarning: Currently OAS-3 doesn't have full support for representing SSE style responses from an API.\n\nIn case the client code is generated from this OAS spec, don't specify a `since` and `until` there is a good chance the generated clients will hang forever waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific endpoint until the OAS-3 standards come to a consensus on how to represent this behavior in OAS-3.\n\n---\n\n###  Comment messages\nAccording to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.\n\n#####  Slow client\n\nThe server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`\n\n##### Internal server error\n\nAn error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`\n\n---\n\n**Event Types**\n\n- **LegacyNote:** Old free text based admin notes\n- **Liquidation:** Event for a position liquidation which initialized by an admin\n- **TransactionCancel:** Event for a manually cancelled transaction",
        "operationId": "subscribeToAdminActionSSE",
        "parameters": [
          {
            "description": "Format: RFC3339 or YYYY-MM-DD",
            "in": "query",
            "name": "since",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "Format: RFC3339 or YYYY-MM-DD",
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
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/AdminActionLegacyNote"
                      },
                      {
                        "$ref": "#/components/schemas/AdminActionLiquidation"
                      },
                      {
                        "$ref": "#/components/schemas/AdminActionTransactionCancel"
                      }
                    ]
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to Admin Action Events (SSE)",
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