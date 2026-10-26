# Retrieve a Single Journal Entry

Source: https://docs.alpaca.markets/us/reference/get-v1-journals-journal_id.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve a Single Journal Entry

You can query a specific journal entry that you submitted to Alpaca by passing into the query the journal_id.

Will return a journal entry if a journal entry with journal_id exists, otherwise will throw an error.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
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
    "/v1/journals/{journal_id}": {
      "get": {
        "description": "You can query a specific journal entry that you submitted to Alpaca by passing into the query the journal_id.\n\nWill return a journal entry if a journal entry with journal_id exists, otherwise will throw an error.",
        "operationId": "get-v1-journals-journal_id",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Journal"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve a Single Journal Entry",
        "tags": [
          "Journals"
        ]
      },
      "parameters": [
        {
          "in": "path",
          "name": "journal_id",
          "required": true,
          "schema": {
            "format": "uuid",
            "type": "string"
          }
        }
      ]
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