# Create a Journal

Source: https://docs.alpaca.markets/us/reference/createjournal.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create a Journal

A journal can be JNLC (move cash) or JNLS (move shares), dictated by `entry_type`. Generally, journal requests are subject to approval and starts from the `pending` status. The status changes are propagated through the Event API. Under certain conditions agreed for the partner, such journal transactions that meet the criteria are executed right away.

**Idempotency**: Reusing the same key with an identical request returns the
previously created journal without creating a duplicate. Reusing the same key with
a different request returns `422 Unprocessable Entity`.


# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "LegacyIdempotencyKey": {
        "description": "Optional client-generated key for safe retries and duplicate request detection.\nThis endpoint currently accepts keys up to 128 characters. Alpaca is moving toward\na 36-character maximum; new implementations should generate a unique UUIDv7 or\nUUIDv4 value (36 characters including hyphens) for each logical operation. Do not\nreuse a key across operations.\n",
        "in": "header",
        "name": "Idempotency-Key",
        "required": false,
        "schema": {
          "maxLength": 128,
          "type": "string"
        }
      }
    },
    "responses": {
      "IdempotencyKeyConflict": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "The idempotency key was already used with a different request payload."
      }
    },
    "schemas": {
      "CreateJournalRequest": {
        "description": "Journals API allows you to move cash or securities from one account to another.\n\nThis model represents the fields you can specify when creating a Journal\n\nFixture Rules\n\n- No Fixtures\n  - anything below limit is executed immediately\n  - anything above limit is pending until executed at EOD,\n- With Fixtures\n  - any status = rejected will be rejected EOD\n  - any status = pending will be pending forever",
        "examples": [
          {
            "amount": "51",
            "description": "test text /fixtures/status=rejected/fixtures/",
            "entry_type": "JNLC",
            "from_account": "c94bu7rn-4483-4199-840f-6c5fe0b7ca24",
            "to_account": "fn68sbrk-6f2a-433c-8c33-17b66b8941fa"
          }
        ],
        "properties": {
          "amount": {
            "description": "Required if `entry_type` = `JNLC`",
            "type": "string"
          },
          "currency": {
            "type": "string"
          },
          "description": {
            "description": "Max 1024 characters. Can include fixtures for amounts that are above the transaction limit",
            "maxLength": 1024,
            "type": "string"
          },
          "entry_type": {
            "$ref": "#/components/schemas/JournalEntryType"
          },
          "from_account": {
            "description": "The account_id you wish to journal from",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "qty": {
            "description": "Required if `entry_type` = `JNLS`",
            "type": "string"
          },
          "symbol": {
            "description": "Required if `entry_type` = `JNLS`",
            "type": "string"
          },
          "to_account": {
            "description": "The account_id you wish to journal to",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "transmitter_account_number": {
            "description": "Max 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
            "maxLength": 255,
            "type": "string"
          },
          "transmitter_address": {
            "description": "Max 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
            "maxLength": 255,
            "type": "string"
          },
          "transmitter_financial_institution": {
            "description": "Max 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
            "maxLength": 255,
            "type": "string"
          },
          "transmitter_name": {
            "description": "Max 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
            "maxLength": 255,
            "type": "string"
          },
          "transmitter_timestamp": {
            "description": "RFC 3339 format. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "to_account",
          "from_account",
          "entry_type"
        ],
        "type": "object"
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
      },
      "JNLC": {
        "allOf": [
          {
            "$ref": "#/components/schemas/JournalBase"
          },
          {
            "properties": {
              "entry_type": {
                "description": "Cash journal discriminator value.",
                "enum": [
                  "JNLC"
                ],
                "type": "string"
              },
              "transmitter_account_number": {
                "description": "Optional for JNLC journals. Maximum 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
                "maxLength": 255,
                "type": "string"
              },
              "transmitter_address": {
                "description": "Optional for JNLC journals. Maximum 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
                "maxLength": 255,
                "type": "string"
              },
              "transmitter_financial_institution": {
                "description": "Optional for JNLC journals. Maximum 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
                "maxLength": 255,
                "type": "string"
              },
              "transmitter_name": {
                "description": "Optional for JNLC journals. Maximum 255 characters. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
                "maxLength": 255,
                "type": "string"
              },
              "transmitter_timestamp": {
                "description": "Optional for JNLC journals. RFC 3339 format. See more details about [Travel Rule](https://alpaca.markets/docs/broker/integration/funding/#travel-rule) in our main documentation.",
                "format": "date-time",
                "type": "string"
              }
            },
            "required": [
              "entry_type"
            ],
            "type": "object"
          }
        ],
        "description": "A cash journal response with all shared Journal fields.",
        "examples": [
          {
            "currency": "USD",
            "description": "",
            "entry_type": "JNLC",
            "from_account": "8f8c8cee-2591-4f83-be12-82c659b5e748",
            "id": "56f106e5-25a4-4eee-96fa-25bb05dc86bc",
            "net_amount": "1000",
            "price": null,
            "qty": null,
            "settle_date": null,
            "status": "pending",
            "symbol": null,
            "system_date": null,
            "to_account": "399f85f1-cbbd-4eaa-a934-70027fb5c1de"
          }
        ],
        "title": "JNLC"
      },
      "JNLS": {
        "allOf": [
          {
            "$ref": "#/components/schemas/JournalBase"
          },
          {
            "properties": {
              "entry_type": {
                "description": "Securities journal discriminator value.",
                "enum": [
                  "JNLS"
                ],
                "type": "string"
              }
            },
            "required": [
              "entry_type"
            ],
            "type": "object"
          }
        ],
        "description": "A securities journal response with all shared Journal fields.",
        "examples": [
          {
            "currency": "USD",
            "description": "this is a test journal",
            "entry_type": "JNLS",
            "from_account": "8f4f3d11-4483-4199-840f-6c5fe0b7ca24",
            "id": "f45f67e8-d1fc-4136-aa4f-cf4460aecdfc",
            "net_amount": null,
            "price": "128.23",
            "qty": "0.5",
            "settle_date": "2020-12-24",
            "status": "executed",
            "symbol": "AAPL",
            "system_date": "2020-12-24",
            "to_account": "a7a7e666-6f2a-433c-8c33-17b66b8941fa"
          }
        ],
        "title": "JNLS"
      },
      "Journal": {
        "description": "Represents a cash or securities transfer between accounts, selected by `entry_type`.",
        "discriminator": {
          "mapping": {
            "JNLC": "#/components/schemas/JNLC",
            "JNLS": "#/components/schemas/JNLS"
          },
          "propertyName": "entry_type"
        },
        "examples": [
          {
            "currency": "USD",
            "description": "",
            "entry_type": "JNLC",
            "from_account": "8f8c8cee-2591-4f83-be12-82c659b5e748",
            "id": "56f106e5-25a4-4eee-96fa-25bb05dc86bc",
            "net_amount": "1000",
            "price": null,
            "qty": null,
            "settle_date": null,
            "status": "pending",
            "symbol": null,
            "system_date": null,
            "to_account": "399f85f1-cbbd-4eaa-a934-70027fb5c1de"
          },
          {
            "currency": "USD",
            "description": "this is a test journal",
            "entry_type": "JNLS",
            "from_account": "8f4f3d11-4483-4199-840f-6c5fe0b7ca24",
            "id": "f45f67e8-d1fc-4136-aa4f-cf4460aecdfc",
            "net_amount": null,
            "price": "128.23",
            "qty": "0.5",
            "settle_date": "2020-12-24",
            "status": "executed",
            "symbol": "AAPL",
            "system_date": "2020-12-24",
            "to_account": "a7a7e666-6f2a-433c-8c33-17b66b8941fa"
          }
        ],
        "oneOf": [
          {
            "$ref": "#/components/schemas/JNLC"
          },
          {
            "$ref": "#/components/schemas/JNLS"
          }
        ],
        "title": "Journal"
      },
      "JournalBase": {
        "description": "Shared response fields returned for cash and securities journals.",
        "properties": {
          "created_at": {
            "description": "The creation time when supplied by the endpoint.",
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "Currency denomination of the journal.",
            "type": "string"
          },
          "description": {
            "description": "The journal description.",
            "type": "string"
          },
          "from_account": {
            "description": "The account ID that initiated the journal.",
            "format": "uuid",
            "type": "string"
          },
          "id": {
            "description": "The journal ID.",
            "format": "uuid",
            "type": "string"
          },
          "net_amount": {
            "description": "The cash amount, or null when not applicable.",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "price": {
            "description": "The journaled security price, or null when not applicable.",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "qty": {
            "description": "The journaled security quantity, or null when not applicable.",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "settle_date": {
            "description": "The settlement date, or null until one is assigned.",
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "status": {
            "$ref": "#/components/schemas/JournalStatus"
          },
          "symbol": {
            "description": "The journaled security symbol, or null for a cash journal.",
            "type": [
              "string",
              "null"
            ]
          },
          "system_date": {
            "description": "The booking-system date, or null until one is assigned.",
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "to_account": {
            "description": "The account ID that received the journal.",
            "format": "uuid",
            "type": "string"
          },
          "transmitter_info": {
            "$ref": "#/components/schemas/TransmitterInfo"
          }
        },
        "required": [
          "id",
          "from_account",
          "to_account",
          "symbol",
          "qty",
          "price",
          "status",
          "settle_date",
          "system_date",
          "net_amount",
          "description",
          "currency"
        ],
        "title": "JournalBase",
        "type": "object"
      },
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
      "TransmitterInfo": {
        "description": "Information about the transmitter to satisfy travel rule requirements. Required if the requesting correspondent qualifies as a financial institution\n",
        "properties": {
          "originator_bank_account_number": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_bank_name": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_city": {
            "type": "string"
          },
          "originator_country": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_full_name": {
            "description": "Required if the requesting correspondent qualifies as a financial institution\n",
            "type": "string"
          },
          "originator_postal_code": {
            "type": "string"
          },
          "originator_state": {
            "type": "string"
          },
          "originator_street_address": {
            "type": "string"
          },
          "other_identifying_information": {
            "description": "Used to facilitate transfer lookup in the event it is required. Recommended to be the originating bank's reference number for the transfer\n",
            "type": "string"
          }
        },
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
    "/v1/journals": {
      "post": {
        "description": "A journal can be JNLC (move cash) or JNLS (move shares), dictated by `entry_type`. Generally, journal requests are subject to approval and starts from the `pending` status. The status changes are propagated through the Event API. Under certain conditions agreed for the partner, such journal transactions that meet the criteria are executed right away.\n\n**Idempotency**: Reusing the same key with an identical request returns the\npreviously created journal without creating a duplicate. Reusing the same key with\na different request returns `422 Unprocessable Entity`.\n",
        "operationId": "createJournal",
        "parameters": [
          {
            "$ref": "#/components/parameters/LegacyIdempotencyKey"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "example": {
                "amount": "115.5",
                "entry_type": "JNLC",
                "from_account": "7c891489-574f-4f9a-82f0-4082a07f4736",
                "to_account": "2d47a229-0c25-40a2-8cc7-b2c8821ff93a"
              },
              "schema": {
                "$ref": "#/components/schemas/CreateJournalRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Journal"
                }
              }
            },
            "description": "The New Journal object"
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "description": "One of the parameters is invalid."
          },
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "description": "The amount requested to move is not available."
          },
          "404": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "description": "One of the account is not found."
          },
          "422": {
            "$ref": "#/components/responses/IdempotencyKeyConflict"
          }
        },
        "summary": "Create a Journal",
        "tags": [
          "Journals"
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
      "name": "Journals"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```