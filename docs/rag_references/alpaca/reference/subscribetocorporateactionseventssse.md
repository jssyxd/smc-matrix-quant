# Subscribe to Corporate Actions Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetocorporateactionseventssse.md

---
updatedAt: 2026-07-20T08:44:29.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Corporate Actions Events (SSE)

Server-Sent Events (SSE) stream that delivers every corporate-action mutation (`insert` / `update` / `delete`) across all supported CA types on a single long-lived `text/event-stream` connection. When `since`, `since_id`, or the `Last-Event-Id` reconnect header is provided, historical events are replayed first; otherwise only live events are pushed.

Each event carries an `event_type` discriminator that selects the shape of the `ca` payload -- see the [`corporate_action_event`](#/components/schemas/corporate_action_event) schema for the mapping to each per-type schema. The same underlying data is available on demand via [`GET /v1/corporate-actions`](#operation/CorporateActions).


# OpenAPI definition

```json
{
  "components": {
    "headers": {
      "ratelimit_limit": {
        "description": "Request limit per minute.",
        "example": 100,
        "schema": {
          "type": "integer"
        }
      },
      "ratelimit_remaining": {
        "description": "Request limit per minute remaining.",
        "example": 90,
        "schema": {
          "type": "integer"
        }
      },
      "ratelimit_reset": {
        "description": "The UNIX epoch when the remaining quota changes.",
        "example": 1674044551,
        "schema": {
          "type": "integer"
        }
      }
    },
    "parameters": {
      "cas_events_last_event_id": {
        "description": "Standard SSE reconnect header. ULID matching an `event_id`; replay events\nwhose `event_id` is greater than or equal to this value (inclusive -- the\nevent with this id is redelivered on reconnect, so clients should\ndeduplicate by `event_id` if needed). Overrides `since_id` when both are\nset.\n",
        "example": "01J9RPMV5TKB8WX3M4F1KZ7QH2",
        "in": "header",
        "name": "Last-Event-Id",
        "schema": {
          "$ref": "#/components/schemas/event_id"
        }
      },
      "cas_events_region": {
        "description": "Which markets to receive events for. Compared against the envelope's `region`\nfield and applied uniformly to historical and live events.\n\n- `all` (default): every event, regardless of market.\n- `us`: only events with `region == \"us\"`.\n- `non_us`: only events with `region == \"non_us\"`.\n\nUnknown values return `400` with the list of valid values in the error\nmessage. The value is case-insensitive.\n",
        "in": "query",
        "name": "region",
        "schema": {
          "default": "all",
          "enum": [
            "all",
            "us",
            "non_us"
          ],
          "type": "string"
        }
      },
      "cas_events_since": {
        "description": "Replay events emitted on or after this RFC-3339 date. Mutually exclusive with\n`since_id`. Required when `until` is specified.\n",
        "example": "2026-03-20T00:00:00Z",
        "in": "query",
        "name": "since",
        "schema": {
          "format": "date-time",
          "type": "string"
        }
      },
      "cas_events_since_id": {
        "description": "ULID matching an `event_id`; replay events whose `event_id` is greater than\nor equal to this value (inclusive -- the event with this id, if it still\nexists, is redelivered). Mutually exclusive with `since`. Overridden by the\n`Last-Event-Id` header when both are set.\n",
        "example": "01J9RPMV5TKB8WX3M4F1KZ7QH2",
        "in": "query",
        "name": "since_id",
        "schema": {
          "$ref": "#/components/schemas/event_id"
        }
      },
      "cas_events_type": {
        "description": "Filter the stream to a subset of `event_type` values.\n\nPassed as a comma-separated list in the URL query, e.g.\n`?type=cash_dividend_corporateaction_event,stock_dividend_corporateaction_event`.\n\nOnly events whose `event_type` is in this list are delivered. An empty or\nomitted value is treated as \"no filter\" (deliver every type). Unknown values\nreturn `400` with the list of valid values in the error message. The filter\napplies uniformly to both replayed (historical) and live events.\n\nSee [`corporate_action_event_type`](#/components/schemas/corporate_action_event_type)\nfor the full list of accepted values.\n",
        "example": [
          "cash_dividend_corporateaction_event",
          "stock_dividend_corporateaction_event"
        ],
        "explode": false,
        "in": "query",
        "name": "type",
        "schema": {
          "items": {
            "$ref": "#/components/schemas/corporate_action_event_type"
          },
          "type": "array"
        },
        "style": "form"
      },
      "cas_events_until": {
        "description": "Close the connection after the last event on this RFC-3339 date (inclusive).\nRequires `since`; cannot be in the future.\n",
        "example": "2026-03-20T23:59:59Z",
        "in": "query",
        "name": "until",
        "schema": {
          "format": "date-time",
          "type": "string"
        }
      },
      "cas_events_until_id": {
        "description": "ULID matching an `event_id`; close the connection once this id has been\ndelivered (inclusive). Requires `since_id`; cannot be in the future.\n",
        "example": "01J9RVB6Y4ZK8M3N7QD2WX1RFP",
        "in": "query",
        "name": "until_id",
        "schema": {
          "$ref": "#/components/schemas/event_id"
        }
      }
    },
    "responses": {
      "400": {
        "description": "One of the request parameters is invalid. See the returned message for details.\n",
        "headers": {
          "X-RateLimit-Limit": {
            "$ref": "#/components/headers/ratelimit_limit"
          },
          "X-RateLimit-Remaining": {
            "$ref": "#/components/headers/ratelimit_remaining"
          },
          "X-RateLimit-Reset": {
            "$ref": "#/components/headers/ratelimit_reset"
          }
        }
      },
      "401": {
        "description": "Authentication headers are missing or invalid. Make sure you authenticate your request with a valid API key.\n"
      },
      "403": {
        "description": "The requested resource is forbidden.\n"
      },
      "429": {
        "description": "Too many requests. You hit the rate limit. Use the X-RateLimit-... response headers to make sure you're under the rate limit.\n",
        "headers": {
          "X-RateLimit-Limit": {
            "$ref": "#/components/headers/ratelimit_limit"
          },
          "X-RateLimit-Remaining": {
            "$ref": "#/components/headers/ratelimit_remaining"
          },
          "X-RateLimit-Reset": {
            "$ref": "#/components/headers/ratelimit_reset"
          }
        }
      },
      "500": {
        "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on [Slack](https://alpaca.markets/slack) or on the [Community Forum](https://forum.alpaca.markets/).\n"
      }
    },
    "schemas": {
      "ca_event_base": {
        "description": "Common fields present on every `ca` payload regardless of `event_type`.\nNot meant to be referenced directly by clients -- it exists so each\nper-type payload schema (`ca_event_cash_dividend`, `ca_event_forward_split`,\n...) can `allOf`-compose it instead of restating `id` and `process_date`.\nThis makes the \"always present\" invariant structural (guaranteed by the\nschema) rather than emergent from repetition, and matches the \"Common `ca`\nfields\" section of the event-streaming Corporate Actions SSE design doc.\n",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ca_id"
          },
          "process_date": {
            "$ref": "#/components/schemas/process_date"
          }
        },
        "required": [
          "id",
          "process_date"
        ],
        "type": "object"
      },
      "ca_event_capital_gains_distribution": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "long_term_rate": {
                "description": "Long-term capital-gains payment per share, as a decimal string.",
                "examples": [
                  "1.4372"
                ],
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "short_term_rate": {
                "description": "Short-term capital-gains payment per share, as a decimal string.",
                "examples": [
                  "0.1051"
                ],
                "type": "string"
              },
              "symbol": {
                "description": "Ticker paying the distribution.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Capital-gains distribution payload delivered when\n`event_type == capital_gains_distribution_corporateaction_event`. Every\ndecimal field is emitted as a JSON string to preserve precision on the\nwire. At least one of `long_term_rate` / `short_term_rate` is present;\ncombined distributions carry both.\n"
      },
      "ca_event_cash_dividend": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "due_bill_off_date": {
                "description": "End of the due-bill period.",
                "format": "date",
                "type": "string"
              },
              "due_bill_on_date": {
                "description": "Start of the due-bill period.",
                "format": "date",
                "type": "string"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "foreign": {
                "description": "`true` if the issuer is not US-based.",
                "type": "boolean"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "rate": {
                "description": "Cash paid per share, as a decimal string.",
                "examples": [
                  "0.24"
                ],
                "type": "string"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "special": {
                "description": "`true` if this is a one-off dividend outside the issuer's regular\ndistribution schedule.\n",
                "type": "boolean"
              },
              "sub_type": {
                "description": "Optional sub-classification of the dividend.",
                "enum": [
                  "interest",
                  "return_of_capital"
                ],
                "type": "string"
              },
              "symbol": {
                "description": "Ticker paying the dividend.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "rate",
              "special",
              "foreign",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Cash dividend payload delivered when\n`event_type == cash_dividend_corporateaction_event`. Corresponds to\n`cash_dividends` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_cash_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "acquiree_cusip": {
                "description": "CUSIP of the company being bought.",
                "type": "string"
              },
              "acquiree_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquiree_symbol": {
                "description": "Ticker being bought (will disappear after the merger).",
                "type": "string"
              },
              "acquirer_cusip": {
                "description": "Buyer's CUSIP.",
                "type": "string"
              },
              "acquirer_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquirer_symbol": {
                "description": "Buyer's ticker (the surviving company).",
                "type": "string"
              },
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "effective_date": {
                "$ref": "#/components/schemas/effective_date"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "rate": {
                "description": "Cash paid per share of the acquired company, as a decimal string.",
                "examples": [
                  "42.50"
                ],
                "type": "string"
              }
            },
            "required": [
              "acquiree_symbol",
              "acquiree_cusip",
              "rate",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "Cash merger payload delivered when\n`event_type == cash_merger_corporateaction_event`. Corresponds to\n`cash_mergers` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_equity_partial_call": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "dividend_rate": {
                "description": "Dividend rate associated with the called shares, as a decimal string.",
                "examples": [
                  "0.05"
                ],
                "type": "string"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "lottery_date": {
                "description": "When the lottery drawing happens.",
                "format": "date",
                "type": "string"
              },
              "lottery_type": {
                "description": "How called shares were allocated among holders.",
                "enum": [
                  "original",
                  "supplemental"
                ],
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "price": {
                "description": "Price paid per called share, as a decimal string.",
                "examples": [
                  "15.00"
                ],
                "type": "string"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "results_publication_date": {
                "description": "When the lottery results are published.",
                "format": "date",
                "type": "string"
              },
              "symbol": {
                "description": "Ticker being partially called.",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Partial redemption of an equity issue where the issuer calls back only a\nfraction of outstanding shares -- typically allocated to holders via a\nlottery. Delivered when\n`event_type == equity_partial_call_corporateaction_event`. Corresponds to\n`partial_calls` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_forward_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "due_bill_redemption_date": {
                "$ref": "#/components/schemas/due_bill_redemption_date"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_rate": {
                "description": "Shares after the split, as a decimal string.",
                "examples": [
                  "4"
                ],
                "type": "string"
              },
              "old_rate": {
                "description": "Shares before the split, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "symbol": {
                "description": "Ticker being split.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "old_rate",
              "new_rate",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Forward stock split payload delivered when\n`event_type == forward_split_corporateaction_event`. Corresponds to\n`forward_splits` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_name_change": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "new_cusip": {
                "description": "CUSIP after the change.",
                "type": "string"
              },
              "new_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_symbol": {
                "description": "Ticker after the change.",
                "type": "string"
              },
              "old_cusip": {
                "description": "CUSIP before the change.",
                "type": "string"
              },
              "old_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "old_symbol": {
                "description": "Ticker before the change.",
                "type": "string"
              }
            },
            "required": [
              "old_symbol",
              "old_cusip",
              "new_symbol",
              "new_cusip"
            ],
            "type": "object"
          }
        ],
        "description": "Name/ticker change payload delivered when\n`event_type == name_change_corporateaction_event`. Corresponds to\n`name_changes` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response.\n"
      },
      "ca_event_redemption": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "rate": {
                "description": "Cash paid per share, as a decimal string.",
                "examples": [
                  "25.00"
                ],
                "type": "string"
              },
              "symbol": {
                "description": "Ticker being redeemed.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "rate"
            ],
            "type": "object"
          }
        ],
        "description": "Full redemption payload delivered when\n`event_type == redemption_corporateaction_event`. Corresponds to\n`redemptions` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_reorganization": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "cash_rate": {
                "description": "Cash paid per source share, as a decimal string.",
                "examples": [
                  "5.00"
                ],
                "type": "string"
              },
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the original security.",
                "type": "string"
              },
              "effective_date": {
                "$ref": "#/components/schemas/effective_date"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "stock_movements": {
                "description": "One entry per replacement security delivered to holders.",
                "items": {
                  "$ref": "#/components/schemas/ca_event_reorganization_stock_movement"
                },
                "type": "array"
              },
              "symbol": {
                "description": "Ticker undergoing the reorganization.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "General-purpose corporate restructuring (e.g. Chapter 11 emergence) where\nexisting holders receive a mix of cash and/or one or more replacement\nsecurities. Each entry in `stock_movements` describes a separate\nshare-class distribution. Delivered when\n`event_type == reorganization_corporateaction_event`. Corresponds to\n`reorganizations` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_reorganization_stock_movement": {
        "additionalProperties": false,
        "description": "A single replacement-security leg of a\n[`ca_event_reorganization`](#/components/schemas/ca_event_reorganization)\npayload. All decimal fields are emitted as JSON strings to preserve\nprecision on the wire.\n",
        "properties": {
          "cusip": {
            "description": "Replacement CUSIP.",
            "type": "string"
          },
          "isin": {
            "$ref": "#/components/schemas/isin"
          },
          "new_rate": {
            "description": "Replacement shares delivered per `source_rate`, as a decimal string.",
            "examples": [
              "1"
            ],
            "type": "string"
          },
          "source_rate": {
            "description": "Source shares required for each `new_rate`, as a decimal string.",
            "examples": [
              "10"
            ],
            "type": "string"
          },
          "symbol": {
            "description": "Replacement ticker.",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "cusip",
          "new_rate",
          "source_rate"
        ],
        "type": "object"
      },
      "ca_event_reverse_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "new_cusip": {
                "description": "CUSIP after the split.",
                "type": "string"
              },
              "new_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_rate": {
                "description": "Shares after the split, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "new_symbol": {
                "description": "Ticker after the split when the issuer also changes symbol (e.g. with\na \"D\" suffix). Omitted when the ticker doesn't change.\n",
                "type": "string"
              },
              "old_cusip": {
                "description": "CUSIP before the split.",
                "type": "string"
              },
              "old_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "old_rate": {
                "description": "Shares before the split, as a decimal string.",
                "examples": [
                  "10"
                ],
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "symbol": {
                "description": "Ticker being split.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "old_cusip",
              "new_cusip",
              "old_rate",
              "new_rate",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Reverse stock split payload delivered when\n`event_type == reverse_split_corporateaction_event`. Corresponds to\n`reverse_splits` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_rights_distribution": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "expiration_date": {
                "$ref": "#/components/schemas/expiration_date"
              },
              "new_cusip": {
                "description": "CUSIP of the new right.",
                "type": "string"
              },
              "new_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_symbol": {
                "description": "Ticker of the new right/warrant.",
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "rate": {
                "description": "Rights given per share you own, as a decimal string.",
                "examples": [
                  "0.25"
                ],
                "type": "string"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "source_cusip": {
                "description": "CUSIP of the underlying ticker.",
                "type": "string"
              },
              "source_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "source_symbol": {
                "description": "Ticker whose holders receive the rights.",
                "type": "string"
              }
            },
            "required": [
              "source_symbol",
              "source_cusip",
              "new_symbol",
              "new_cusip",
              "rate",
              "ex_date",
              "payable_date"
            ],
            "type": "object"
          }
        ],
        "description": "Rights distribution payload delivered when\n`event_type == rights_distribution_corporateaction_event`. Corresponds to\n`rights_distributions` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_spin_off": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "due_bill_redemption_date": {
                "$ref": "#/components/schemas/due_bill_redemption_date"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "new_cusip": {
                "description": "CUSIP of the new spin-off company.",
                "type": "string"
              },
              "new_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_rate": {
                "description": "New-company shares distributed per `source_rate` parent shares, as a decimal string.",
                "examples": [
                  "0.5"
                ],
                "type": "string"
              },
              "new_symbol": {
                "description": "Ticker of the new spin-off company.",
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "source_cusip": {
                "description": "Parent CUSIP.",
                "type": "string"
              },
              "source_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "source_rate": {
                "description": "Parent shares required per ratio unit, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "source_symbol": {
                "description": "Parent company's ticker.",
                "type": "string"
              }
            },
            "required": [
              "source_symbol",
              "source_cusip",
              "source_rate",
              "new_symbol",
              "new_cusip",
              "new_rate",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Spin-off payload delivered when\n`event_type == spin_off_corporateaction_event`. Corresponds to\n`spin_offs` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_stock_and_cash_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "acquiree_cusip": {
                "description": "CUSIP of the company being bought.",
                "type": "string"
              },
              "acquiree_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquiree_rate": {
                "description": "Bought-side ratio, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "acquiree_symbol": {
                "description": "Ticker being bought (will disappear).",
                "type": "string"
              },
              "acquirer_cusip": {
                "description": "Buyer's CUSIP.",
                "type": "string"
              },
              "acquirer_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquirer_rate": {
                "description": "Buyer shares given per unit ratio, as a decimal string.",
                "examples": [
                  "0.5"
                ],
                "type": "string"
              },
              "acquirer_symbol": {
                "description": "Buyer's ticker (the surviving company).",
                "type": "string"
              },
              "cash_rate": {
                "description": "Extra cash paid per share of the acquired company, as a decimal string.",
                "examples": [
                  "10.00"
                ],
                "type": "string"
              },
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "effective_date": {
                "$ref": "#/components/schemas/effective_date"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              }
            },
            "required": [
              "acquirer_symbol",
              "acquirer_cusip",
              "acquirer_rate",
              "acquiree_symbol",
              "acquiree_cusip",
              "acquiree_rate",
              "cash_rate",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "Merger paying a mix of stock and cash. Delivered when\n`event_type == stock_and_cash_merger_corporateaction_event`. Corresponds\nto `stock_and_cash_mergers` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_stock_dividend": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "ex_date": {
                "$ref": "#/components/schemas/ex_date"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              },
              "rate": {
                "description": "Extra shares received per share held, as a decimal string.",
                "examples": [
                  "0.05"
                ],
                "type": "string"
              },
              "record_date": {
                "$ref": "#/components/schemas/record_date"
              },
              "symbol": {
                "description": "Ticker paying the stock dividend.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip",
              "rate",
              "ex_date"
            ],
            "type": "object"
          }
        ],
        "description": "Stock dividend payload delivered when\n`event_type == stock_dividend_corporateaction_event`. Corresponds to\n`stock_dividends` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_stock_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "acquiree_cusip": {
                "description": "CUSIP of the company being bought.",
                "type": "string"
              },
              "acquiree_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquiree_rate": {
                "description": "Bought-side ratio, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "acquiree_symbol": {
                "description": "Ticker being bought (will disappear).",
                "type": "string"
              },
              "acquirer_cusip": {
                "description": "Buyer's CUSIP.",
                "type": "string"
              },
              "acquirer_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "acquirer_rate": {
                "description": "Buyer-side ratio, as a decimal string.",
                "examples": [
                  "0.75"
                ],
                "type": "string"
              },
              "acquirer_symbol": {
                "description": "Buyer's ticker (the surviving company).",
                "type": "string"
              },
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "effective_date": {
                "$ref": "#/components/schemas/effective_date"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              }
            },
            "required": [
              "acquirer_symbol",
              "acquirer_cusip",
              "acquirer_rate",
              "acquiree_symbol",
              "acquiree_cusip",
              "acquiree_rate",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "All-stock merger payload delivered when\n`event_type == stock_merger_corporateaction_event`. Corresponds to\n`stock_mergers` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_unit_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "alternate_cusip": {
                "description": "CUSIP of the secondary leg.",
                "type": "string"
              },
              "alternate_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "alternate_rate": {
                "description": "Secondary-leg shares delivered per unit, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "alternate_symbol": {
                "description": "Ticker of the secondary leg (usually a warrant).",
                "type": "string"
              },
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "effective_date": {
                "$ref": "#/components/schemas/effective_date"
              },
              "new_cusip": {
                "description": "CUSIP of the primary leg.",
                "type": "string"
              },
              "new_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "new_rate": {
                "description": "Primary-leg shares delivered per unit, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "new_symbol": {
                "description": "Ticker of the primary leg (usually the common share).",
                "type": "string"
              },
              "old_cusip": {
                "description": "CUSIP of the unit.",
                "type": "string"
              },
              "old_isin": {
                "$ref": "#/components/schemas/isin"
              },
              "old_rate": {
                "description": "Units per ratio unit, as a decimal string.",
                "examples": [
                  "1"
                ],
                "type": "string"
              },
              "old_symbol": {
                "description": "Ticker of the unit being split.",
                "type": "string"
              },
              "payable_date": {
                "$ref": "#/components/schemas/payable_date"
              }
            },
            "required": [
              "old_symbol",
              "old_cusip",
              "old_rate",
              "new_symbol",
              "new_cusip",
              "new_rate",
              "alternate_symbol",
              "alternate_cusip",
              "alternate_rate",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "Unit split payload delivered when\n`event_type == unit_split_corporateaction_event`. Corresponds to\n`unit_splits` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response, but\nevery decimal field is emitted as a JSON string to preserve precision on\nthe wire.\n"
      },
      "ca_event_worthless_removal": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ca_event_base"
          },
          {
            "properties": {
              "currency": {
                "$ref": "#/components/schemas/currency"
              },
              "cusip": {
                "description": "CUSIP of the security.",
                "type": "string"
              },
              "isin": {
                "$ref": "#/components/schemas/isin"
              },
              "symbol": {
                "description": "Ticker being removed.",
                "type": "string"
              }
            },
            "required": [
              "symbol",
              "cusip"
            ],
            "type": "object"
          }
        ],
        "description": "Worthless removal payload delivered when\n`event_type == worthless_removal_corporateaction_event`. Corresponds to\n`worthless_removals` on the REST\n[`GET /v1/corporate-actions`](#operation/CorporateActions) response.\n"
      },
      "ca_id": {
        "description": "The internal Alpaca identifier of the corporate action.",
        "format": "uuid",
        "type": "string"
      },
      "corporate_action_event": {
        "description": "A single corporate-action mutation delivered over the\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n\nEvery event uses the same envelope. The `event_type` field selects which of\nthe 15 per-type schemas populates `ca`; see\n[`corporate_action_event_type`](#/components/schemas/corporate_action_event_type)\nfor the full mapping and follow the link on each row to the per-type `ca`\npayload schema.\n\nOptional fields (including `currency` and, on most CA types, `isin`) are\nomitted from the JSON when empty; `null` is never emitted.\n",
        "discriminator": {
          "mapping": {
            "capital_gains_distribution_corporateaction_event": "#/components/schemas/corporate_action_event_capital_gains_distribution",
            "cash_dividend_corporateaction_event": "#/components/schemas/corporate_action_event_cash_dividend",
            "cash_merger_corporateaction_event": "#/components/schemas/corporate_action_event_cash_merger",
            "equity_partial_call_corporateaction_event": "#/components/schemas/corporate_action_event_equity_partial_call",
            "forward_split_corporateaction_event": "#/components/schemas/corporate_action_event_forward_split",
            "name_change_corporateaction_event": "#/components/schemas/corporate_action_event_name_change",
            "redemption_corporateaction_event": "#/components/schemas/corporate_action_event_redemption",
            "reorganization_corporateaction_event": "#/components/schemas/corporate_action_event_reorganization",
            "reverse_split_corporateaction_event": "#/components/schemas/corporate_action_event_reverse_split",
            "rights_distribution_corporateaction_event": "#/components/schemas/corporate_action_event_rights_distribution",
            "spin_off_corporateaction_event": "#/components/schemas/corporate_action_event_spin_off",
            "stock_and_cash_merger_corporateaction_event": "#/components/schemas/corporate_action_event_stock_and_cash_merger",
            "stock_dividend_corporateaction_event": "#/components/schemas/corporate_action_event_stock_dividend",
            "stock_merger_corporateaction_event": "#/components/schemas/corporate_action_event_stock_merger",
            "unit_split_corporateaction_event": "#/components/schemas/corporate_action_event_unit_split",
            "worthless_removal_corporateaction_event": "#/components/schemas/corporate_action_event_worthless_removal"
          },
          "propertyName": "event_type"
        },
        "oneOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_capital_gains_distribution"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_cash_dividend"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_cash_merger"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_equity_partial_call"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_forward_split"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_name_change"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_redemption"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_reorganization"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_reverse_split"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_rights_distribution"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_spin_off"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_stock_and_cash_merger"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_stock_dividend"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_stock_merger"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_unit_split"
          },
          {
            "$ref": "#/components/schemas/corporate_action_event_worthless_removal"
          }
        ]
      },
      "corporate_action_event_action": {
        "description": "Kind of mutation that produced this event on the upstream corporate actions\nstore:\n\n- `insert`: a new corporate action was created.\n- `update`: an existing corporate action was modified (e.g. a date or rate\n  correction). `ca.id` matches the original event.\n- `delete`: a previously published corporate action was removed. `ca.id`\n  matches the original event; subsequent events for the same id (if any)\n  will be new inserts.\n",
        "enum": [
          "insert",
          "update",
          "delete"
        ],
        "type": "string"
      },
      "corporate_action_event_base": {
        "description": "Common envelope fields shared by every variant of\n[`corporate_action_event`](#/components/schemas/corporate_action_event).\nThis schema is not meant to be used directly by clients -- it exists so each\nper-`event_type` `oneOf` branch can `allOf`-compose the envelope basics\n(`event_id`, `at`, `action`, `region`) alongside its narrowed `event_type` /\n`ca` pair. Keeping these in one place is what makes the envelope's\n`discriminator` play nicely with strict OpenAPI validators.\n",
        "properties": {
          "action": {
            "$ref": "#/components/schemas/corporate_action_event_action"
          },
          "at": {
            "description": "RFC-3339 timestamp when the streaming service emitted this event.",
            "examples": [
              "2026-03-20T12:24:58.807230Z"
            ],
            "format": "date-time",
            "type": "string"
          },
          "event_id": {
            "$ref": "#/components/schemas/event_id"
          },
          "region": {
            "$ref": "#/components/schemas/corporate_action_event_region"
          }
        },
        "required": [
          "event_id",
          "at",
          "action",
          "region"
        ],
        "type": "object"
      },
      "corporate_action_event_capital_gains_distribution": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_capital_gains_distribution"
              },
              "event_type": {
                "enum": [
                  "capital_gains_distribution_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\ncapital_gains_distribution_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_cash_dividend": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_cash_dividend"
              },
              "event_type": {
                "enum": [
                  "cash_dividend_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\ncash_dividend_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_cash_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_cash_merger"
              },
              "event_type": {
                "enum": [
                  "cash_merger_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\ncash_merger_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_equity_partial_call": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_equity_partial_call"
              },
              "event_type": {
                "enum": [
                  "equity_partial_call_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nequity_partial_call_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_forward_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_forward_split"
              },
              "event_type": {
                "enum": [
                  "forward_split_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nforward_split_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_name_change": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_name_change"
              },
              "event_type": {
                "enum": [
                  "name_change_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nname_change_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_redemption": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_redemption"
              },
              "event_type": {
                "enum": [
                  "redemption_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nredemption_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_region": {
        "description": "Envelope-level classification derived from `metadata.global` on the upstream\ncorporate-action record. This is the only field the SSE `region` filter\ninspects on each event.\n\n- `us`: US-listed / US-regulated corporate action.\n- `non_us`: everything else.\n",
        "enum": [
          "us",
          "non_us"
        ],
        "type": "string"
      },
      "corporate_action_event_reorganization": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_reorganization"
              },
              "event_type": {
                "enum": [
                  "reorganization_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nreorganization_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_reverse_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_reverse_split"
              },
              "event_type": {
                "enum": [
                  "reverse_split_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nreverse_split_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_rights_distribution": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_rights_distribution"
              },
              "event_type": {
                "enum": [
                  "rights_distribution_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nrights_distribution_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_spin_off": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_spin_off"
              },
              "event_type": {
                "enum": [
                  "spin_off_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nspin_off_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_stock_and_cash_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_stock_and_cash_merger"
              },
              "event_type": {
                "enum": [
                  "stock_and_cash_merger_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nstock_and_cash_merger_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_stock_dividend": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_stock_dividend"
              },
              "event_type": {
                "enum": [
                  "stock_dividend_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nstock_dividend_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_stock_merger": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_stock_merger"
              },
              "event_type": {
                "enum": [
                  "stock_merger_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nstock_merger_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_type": {
        "description": "Discriminator that determines the shape of the `ca` field on a\n[`corporate_action_event`](#/components/schemas/corporate_action_event).\n\nEach value corresponds to a per-type payload schema:\n\n| `event_type` | `ca` schema |\n| --- | --- |\n| `capital_gains_distribution_corporateaction_event` | [`ca_event_capital_gains_distribution`](#/components/schemas/ca_event_capital_gains_distribution) |\n| `cash_dividend_corporateaction_event` | [`ca_event_cash_dividend`](#/components/schemas/ca_event_cash_dividend) |\n| `cash_merger_corporateaction_event` | [`ca_event_cash_merger`](#/components/schemas/ca_event_cash_merger) |\n| `equity_partial_call_corporateaction_event` | [`ca_event_equity_partial_call`](#/components/schemas/ca_event_equity_partial_call) |\n| `forward_split_corporateaction_event` | [`ca_event_forward_split`](#/components/schemas/ca_event_forward_split) |\n| `name_change_corporateaction_event` | [`ca_event_name_change`](#/components/schemas/ca_event_name_change) |\n| `redemption_corporateaction_event` | [`ca_event_redemption`](#/components/schemas/ca_event_redemption) |\n| `reorganization_corporateaction_event` | [`ca_event_reorganization`](#/components/schemas/ca_event_reorganization) |\n| `reverse_split_corporateaction_event` | [`ca_event_reverse_split`](#/components/schemas/ca_event_reverse_split) |\n| `rights_distribution_corporateaction_event` | [`ca_event_rights_distribution`](#/components/schemas/ca_event_rights_distribution) |\n| `spin_off_corporateaction_event` | [`ca_event_spin_off`](#/components/schemas/ca_event_spin_off) |\n| `stock_and_cash_merger_corporateaction_event` | [`ca_event_stock_and_cash_merger`](#/components/schemas/ca_event_stock_and_cash_merger) |\n| `stock_dividend_corporateaction_event` | [`ca_event_stock_dividend`](#/components/schemas/ca_event_stock_dividend) |\n| `stock_merger_corporateaction_event` | [`ca_event_stock_merger`](#/components/schemas/ca_event_stock_merger) |\n| `unit_split_corporateaction_event` | [`ca_event_unit_split`](#/components/schemas/ca_event_unit_split) |\n| `worthless_removal_corporateaction_event` | [`ca_event_worthless_removal`](#/components/schemas/ca_event_worthless_removal) |\n",
        "enum": [
          "capital_gains_distribution_corporateaction_event",
          "cash_dividend_corporateaction_event",
          "cash_merger_corporateaction_event",
          "equity_partial_call_corporateaction_event",
          "forward_split_corporateaction_event",
          "name_change_corporateaction_event",
          "redemption_corporateaction_event",
          "reorganization_corporateaction_event",
          "reverse_split_corporateaction_event",
          "rights_distribution_corporateaction_event",
          "spin_off_corporateaction_event",
          "stock_and_cash_merger_corporateaction_event",
          "stock_dividend_corporateaction_event",
          "stock_merger_corporateaction_event",
          "unit_split_corporateaction_event",
          "worthless_removal_corporateaction_event"
        ],
        "type": "string"
      },
      "corporate_action_event_unit_split": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_unit_split"
              },
              "event_type": {
                "enum": [
                  "unit_split_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nunit_split_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "corporate_action_event_worthless_removal": {
        "allOf": [
          {
            "$ref": "#/components/schemas/corporate_action_event_base"
          },
          {
            "properties": {
              "ca": {
                "$ref": "#/components/schemas/ca_event_worthless_removal"
              },
              "event_type": {
                "enum": [
                  "worthless_removal_corporateaction_event"
                ],
                "type": "string"
              }
            },
            "required": [
              "event_type",
              "ca"
            ],
            "type": "object"
          }
        ],
        "description": "`corporate_action_event` envelope specialised to `event_type ==\nworthless_removal_corporateaction_event`. Emitted through\n[Corporate Actions Events Stream](#operation/SubscribeToCorporateActionsEventsSSE).\n"
      },
      "currency": {
        "description": "The ISO 4217 currency code associated with the corporate action.\nEmpty value can mean USD, non-applicable (e.g. for name changes) or unknown\n(can change later to a valid currency).\n",
        "type": "string"
      },
      "due_bill_redemption_date": {
        "description": "The date when due bill obligations are redeemed.",
        "format": "date",
        "type": "string"
      },
      "effective_date": {
        "description": "The effective date marks the cutoff point for shareholders to be credited.",
        "format": "date",
        "type": "string"
      },
      "event_id": {
        "description": "Lexically sortable, monotonically increasing 26-character\n[ULID](https://github.com/ulid/spec) (Crockford Base32, uppercase) that\nidentifies a single SSE emission. Unique per message -- an `update` or\n`delete` for the same underlying corporate action carries a fresh\n`event_id`. Because ULIDs sort in emission order, they can be used as\nresume cursors via `since_id`, `until_id`, or the standard `Last-Event-Id`\nreconnect header.\n",
        "examples": [
          "01J9RPMV5TKB8WX3M4F1KZ7QH2"
        ],
        "format": "ulid",
        "pattern": "^[0-7][0-9A-HJKMNP-TV-Z]{25}$",
        "type": "string"
      },
      "ex_date": {
        "description": "The ex-date marks the cutoff point for shareholders to be credited.",
        "format": "date",
        "type": "string"
      },
      "expiration_date": {
        "format": "date",
        "type": "string"
      },
      "isin": {
        "description": "International Securities Identification Number (ISIN) as defined by ISO 6166.\nMay be empty for US corporate actions.\n",
        "type": "string"
      },
      "payable_date": {
        "description": "The date when the corporate action benefit is paid or distributed.",
        "format": "date",
        "type": "string"
      },
      "process_date": {
        "description": "The date when the corporate action is processed by Alpaca.",
        "format": "date",
        "type": "string"
      },
      "record_date": {
        "description": "The date shareholders must own shares to receive the benefit.",
        "format": "date",
        "type": "string"
      }
    },
    "securitySchemes": {
      "BasicAuth": {
        "scheme": "basic",
        "type": "http"
      },
      "apiKey": {
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "apiSecret": {
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
    "description": "Access real-time and historical market data for US equities, options, crypto, and foreign exchange data through the Alpaca REST and WebSocket APIs. There are APIs for Stock Pricing, Option Pricing, Crypto Pricing, Forex, Logos, Fixed income, Corporate Actions, Screener, and News.\n",
    "license": {
      "name": "Creative Commons Attribution Share Alike 4.0 International",
      "url": "https://spdx.org/licenses/CC-BY-SA-4.0.html"
    },
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Market Data API",
    "version": "1.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v1beta1/events/corporate-actions": {
      "get": {
        "description": "Server-Sent Events (SSE) stream that delivers every corporate-action mutation (`insert` / `update` / `delete`) across all supported CA types on a single long-lived `text/event-stream` connection. When `since`, `since_id`, or the `Last-Event-Id` reconnect header is provided, historical events are replayed first; otherwise only live events are pushed.\n\nEach event carries an `event_type` discriminator that selects the shape of the `ca` payload -- see the [`corporate_action_event`](#/components/schemas/corporate_action_event) schema for the mapping to each per-type schema. The same underlying data is available on demand via [`GET /v1/corporate-actions`](#operation/CorporateActions).\n",
        "operationId": "SubscribeToCorporateActionsEventsSSE",
        "parameters": [
          {
            "$ref": "#/components/parameters/cas_events_type"
          },
          {
            "$ref": "#/components/parameters/cas_events_region"
          },
          {
            "$ref": "#/components/parameters/cas_events_since"
          },
          {
            "$ref": "#/components/parameters/cas_events_until"
          },
          {
            "$ref": "#/components/parameters/cas_events_since_id"
          },
          {
            "$ref": "#/components/parameters/cas_events_until_id"
          },
          {
            "$ref": "#/components/parameters/cas_events_last_event_id"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "text/event-stream": {
                "examples": {
                  "CapitalGainsDistribution": {
                    "description": "Example SSE payload delivered when\n`event_type == capital_gains_distribution_corporateaction_event`.\nCombined long-term + short-term distribution; single-leg events\ncarry only the applicable `long_term_rate` or `short_term_rate`.\n",
                    "summary": "Capital gains distribution inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T18:00:00.000000Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "36261K509",
                          "ex_date": "2025-12-26",
                          "id": "98c905a1-08c7-450c-8669-b8e7aee8b44d",
                          "isin": "US36261K5090",
                          "long_term_rate": "0.45855",
                          "payable_date": "2026-01-09",
                          "process_date": "2026-01-08",
                          "record_date": "2025-12-29",
                          "short_term_rate": "0.11019",
                          "symbol": "GCAD"
                        },
                        "event_id": "01KMAGXP2FCJ4NR1TDX8ZWKR6E",
                        "event_type": "capital_gains_distribution_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "CashDividend": {
                    "description": "Example SSE payload delivered when `event_type == cash_dividend_corporateaction_event`.",
                    "summary": "Cash dividend inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T12:24:58.807230Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "037833100",
                          "ex_date": "2026-05-09",
                          "foreign": false,
                          "id": "1dbc7685-9517-4a77-a236-8527d49cefdc",
                          "payable_date": "2026-05-15",
                          "process_date": "2026-05-15",
                          "rate": "0.24",
                          "record_date": "2026-05-12",
                          "special": false,
                          "symbol": "AAPL"
                        },
                        "event_id": "01J9RPMV5TKB8WX3M4F1KZ7QH2",
                        "event_type": "cash_dividend_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "CashMerger": {
                    "description": "Example SSE payload delivered when `event_type == cash_merger_corporateaction_event`.",
                    "summary": "Cash merger inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T15:42:11.118274Z",
                        "ca": {
                          "acquiree_cusip": "90184L102",
                          "acquiree_symbol": "TWTR",
                          "acquirer_cusip": "912656104",
                          "acquirer_symbol": "X",
                          "currency": "USD",
                          "effective_date": "2026-04-01",
                          "id": "f8489167-4e4b-431d-a0be-6017ae1cf08a",
                          "payable_date": "2026-04-05",
                          "process_date": "2026-04-01",
                          "rate": "54.20"
                        },
                        "event_id": "01J9RQ5HNZQK7M3RDVJ8XBPCT1",
                        "event_type": "cash_merger_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "EquityPartialCall": {
                    "description": "Example SSE payload delivered when `event_type == equity_partial_call_corporateaction_event`.",
                    "summary": "Equity partial call inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-19T23:26:46.853262Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "123456789",
                          "id": "b2f8b1a4-4c4a-4e8e-9c9a-1f3b8a7c5d6e",
                          "lottery_date": "2026-06-08",
                          "lottery_type": "original",
                          "payable_date": "2026-06-15",
                          "price": "25.00",
                          "process_date": "2026-06-10",
                          "record_date": "2026-06-05",
                          "results_publication_date": "2026-06-09",
                          "symbol": "EXMP"
                        },
                        "event_id": "01J9RSGD8JR2A4K7MZNTPVQ5XW",
                        "event_type": "equity_partial_call_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "ForwardSplit": {
                    "description": "Example SSE payload delivered when `event_type == forward_split_corporateaction_event`.",
                    "summary": "Forward split updated (US)",
                    "value": [
                      {
                        "action": "update",
                        "at": "2026-03-19T22:50:11.729329Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "67066G104",
                          "ex_date": "2026-06-10",
                          "id": "78467a10-9aa2-4222-8927-abcdef012345",
                          "new_rate": "10",
                          "old_rate": "1",
                          "payable_date": "2026-06-09",
                          "process_date": "2026-06-07",
                          "record_date": "2026-06-06",
                          "symbol": "NVDA"
                        },
                        "event_id": "01KM5CDQXQAE67Z5NHCJZHQ5XV",
                        "event_type": "forward_split_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "NameChange": {
                    "description": "Example SSE payload delivered when `event_type == name_change_corporateaction_event`.",
                    "summary": "Name change inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T00:15:42.318901Z",
                        "ca": {
                          "currency": "USD",
                          "id": "c1a2b3c4-d5e6-4f78-8912-abcdef012345",
                          "new_cusip": "30303M102",
                          "new_symbol": "META",
                          "old_cusip": "30303M102",
                          "old_symbol": "FB",
                          "process_date": "2026-06-09"
                        },
                        "event_id": "01KM5CDZN6KX5V8WQ8KXDH917J",
                        "event_type": "name_change_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "Redemption": {
                    "description": "Example SSE payload delivered when `event_type == redemption_corporateaction_event`.",
                    "summary": "Redemption inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T12:24:52.325158Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "987654321",
                          "id": "4e5f6a7b-8c9d-4e01-a234-56789abcdef0",
                          "payable_date": "2026-07-03",
                          "process_date": "2026-07-01",
                          "rate": "10.00",
                          "symbol": "XYZ"
                        },
                        "event_id": "01J9RVB6Y4ZK8M3N7QD2WX1RFP",
                        "event_type": "redemption_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "Reorganization": {
                    "description": "Example SSE payload delivered when `event_type == reorganization_corporateaction_event`.",
                    "summary": "Reorganization inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T13:12:03.500000Z",
                        "ca": {
                          "cash_rate": "5.00",
                          "currency": "USD",
                          "cusip": "111222333",
                          "effective_date": "2026-08-15",
                          "id": "6a7b8c9d-0e1f-4234-5678-90abcdef1234",
                          "payable_date": "2026-08-20",
                          "process_date": "2026-08-15",
                          "stock_movements": [
                            {
                              "cusip": "444555666",
                              "new_rate": "1",
                              "source_rate": "10",
                              "symbol": "NEWCO"
                            }
                          ],
                          "symbol": "OLDCO"
                        },
                        "event_id": "01KM5CE7CNA84WKP9M7T9BM2EX",
                        "event_type": "reorganization_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "ReverseSplit": {
                    "description": "Example SSE payload delivered when `event_type == reverse_split_corporateaction_event`.",
                    "summary": "Reverse split inserted (non-US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T14:00:00.000000Z",
                        "ca": {
                          "currency": "GBP",
                          "ex_date": "2026-09-01",
                          "id": "7b8c9d0e-1f23-4456-7890-abcdef123456",
                          "new_cusip": "G12345679",
                          "new_isin": "GB0001234568",
                          "new_rate": "1",
                          "old_cusip": "G12345678",
                          "old_isin": "GB0001234567",
                          "old_rate": "20",
                          "payable_date": "2026-09-02",
                          "process_date": "2026-09-01",
                          "record_date": "2026-08-30",
                          "symbol": "EXMP.L"
                        },
                        "event_id": "01KM5CEF44KN9DZNWV9NV456V1",
                        "event_type": "reverse_split_corporateaction_event",
                        "region": "non_us"
                      }
                    ]
                  },
                  "RightsDistribution": {
                    "description": "Example SSE payload delivered when `event_type == rights_distribution_corporateaction_event`.",
                    "summary": "Rights distribution inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T14:30:15.100000Z",
                        "ca": {
                          "currency": "USD",
                          "ex_date": "2026-05-15",
                          "expiration_date": "2026-06-15",
                          "id": "8c9d0e1f-2345-4678-9012-abcdef234567",
                          "new_cusip": "123456790",
                          "new_symbol": "EXMPR",
                          "payable_date": "2026-05-22",
                          "process_date": "2026-05-20",
                          "rate": "0.25",
                          "record_date": "2026-05-18",
                          "source_cusip": "123456789",
                          "source_symbol": "EXMP"
                        },
                        "event_id": "01KM5CEPVKF869Z7RD7EJNP360",
                        "event_type": "rights_distribution_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "SpinOff": {
                    "description": "Example SSE payload delivered when `event_type == spin_off_corporateaction_event`.",
                    "summary": "Spin-off updated (US)",
                    "value": [
                      {
                        "action": "update",
                        "at": "2026-03-20T15:00:22.220000Z",
                        "ca": {
                          "currency": "USD",
                          "ex_date": "2026-04-08",
                          "id": "9d0e1f23-4567-4890-1234-abcdef345678",
                          "new_cusip": "9344D2109",
                          "new_rate": "0.241917",
                          "new_symbol": "WBD",
                          "payable_date": "2026-04-11",
                          "process_date": "2026-04-08",
                          "record_date": "2026-04-05",
                          "source_cusip": "00206R102",
                          "source_rate": "1",
                          "source_symbol": "T"
                        },
                        "event_id": "01KM5CEYK2TRA4S2456P21NJZ0",
                        "event_type": "spin_off_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "StockAndCashMerger": {
                    "description": "Example SSE payload delivered when `event_type == stock_and_cash_merger_corporateaction_event`.",
                    "summary": "Stock-and-cash merger inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T15:30:45.300000Z",
                        "ca": {
                          "acquiree_cusip": "35137L204",
                          "acquiree_rate": "1",
                          "acquiree_symbol": "FOXA",
                          "acquirer_cusip": "254687106",
                          "acquirer_rate": "0.35",
                          "acquirer_symbol": "DIS",
                          "cash_rate": "10.00",
                          "currency": "USD",
                          "effective_date": "2026-05-01",
                          "id": "0e1f2345-6789-4a01-b234-cdef56789012",
                          "payable_date": "2026-05-05",
                          "process_date": "2026-05-01"
                        },
                        "event_id": "01KM5CF6AHE2DGEP087XGX6XDW",
                        "event_type": "stock_and_cash_merger_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "StockDividend": {
                    "description": "Example SSE payload delivered when `event_type == stock_dividend_corporateaction_event`.",
                    "summary": "Stock dividend inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T16:00:00.400000Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "123456789",
                          "ex_date": "2026-05-28",
                          "id": "1f234567-89ab-4c01-d234-ef5678901234",
                          "payable_date": "2026-06-01",
                          "process_date": "2026-06-01",
                          "rate": "0.05",
                          "record_date": "2026-05-30",
                          "symbol": "EXMP"
                        },
                        "event_id": "01KM5CFE200AT1VX7S34MY33YT",
                        "event_type": "stock_dividend_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "StockMerger": {
                    "description": "Example SSE payload delivered when `event_type == stock_merger_corporateaction_event`.",
                    "summary": "Stock merger inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T16:30:11.500000Z",
                        "ca": {
                          "acquiree_cusip": "555666777",
                          "acquiree_rate": "1",
                          "acquiree_symbol": "SMLCO",
                          "acquirer_cusip": "222333444",
                          "acquirer_rate": "0.75",
                          "acquirer_symbol": "BIGCO",
                          "currency": "USD",
                          "effective_date": "2026-07-15",
                          "id": "23456789-abcd-4e01-f234-567890123456",
                          "payable_date": "2026-07-18",
                          "process_date": "2026-07-15"
                        },
                        "event_id": "01KM5CFNSFKSQR5SAEEJ783SWY",
                        "event_type": "stock_merger_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "UnitSplit": {
                    "description": "Example SSE payload delivered when `event_type == unit_split_corporateaction_event`.",
                    "summary": "Unit split inserted (US)",
                    "value": [
                      {
                        "action": "insert",
                        "at": "2026-03-20T17:00:30.600000Z",
                        "ca": {
                          "alternate_cusip": "888999002",
                          "alternate_rate": "0.5",
                          "alternate_symbol": "SPACW",
                          "currency": "USD",
                          "effective_date": "2026-08-01",
                          "id": "3456789a-bcde-4f01-2345-67890abcdef1",
                          "new_cusip": "888999001",
                          "new_rate": "1",
                          "new_symbol": "SPAC",
                          "old_cusip": "888999000",
                          "old_rate": "1",
                          "old_symbol": "SPACU",
                          "payable_date": "2026-08-03",
                          "process_date": "2026-08-01"
                        },
                        "event_id": "01KM5CFXGY9EYPZRTCVJX88FQ8",
                        "event_type": "unit_split_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  },
                  "WorthlessRemoval": {
                    "description": "Example SSE payload delivered when `event_type == worthless_removal_corporateaction_event`.",
                    "summary": "Worthless removal deleted (US)",
                    "value": [
                      {
                        "action": "delete",
                        "at": "2026-03-20T17:30:00.700000Z",
                        "ca": {
                          "currency": "USD",
                          "cusip": "777888999",
                          "id": "456789ab-cdef-4012-3456-7890abcdef12",
                          "process_date": "2026-09-15",
                          "symbol": "DEADCO"
                        },
                        "event_id": "01KM5CG58DTRZ8RKZY3KNYMN3D",
                        "event_type": "worthless_removal_corporateaction_event",
                        "region": "us"
                      }
                    ]
                  }
                },
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/corporate_action_event"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Corporate-action events will now start streaming as long as you keep the connection open.",
            "headers": {
              "X-RateLimit-Limit": {
                "$ref": "#/components/headers/ratelimit_limit"
              },
              "X-RateLimit-Remaining": {
                "$ref": "#/components/headers/ratelimit_remaining"
              },
              "X-RateLimit-Reset": {
                "$ref": "#/components/headers/ratelimit_reset"
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/400"
          },
          "401": {
            "$ref": "#/components/responses/401"
          },
          "403": {
            "$ref": "#/components/responses/403"
          },
          "429": {
            "$ref": "#/components/responses/429"
          },
          "500": {
            "$ref": "#/components/responses/500"
          }
        },
        "security": [
          {
            "apiKey": [],
            "apiSecret": []
          },
          {
            "BasicAuth": []
          }
        ],
        "servers": [
          {
            "description": "Production",
            "url": "https://stream.data.alpaca.markets"
          },
          {
            "description": "Sandbox",
            "url": "https://stream.data.sandbox.alpaca.markets"
          },
          {
            "description": "Staging",
            "url": "https://stream.data.staging-v2.tradetalk.us"
          }
        ],
        "summary": "Subscribe to Corporate Actions Events (SSE)",
        "tags": [
          "Corporate actions"
        ]
      }
    }
  },
  "servers": [
    {
      "description": "Production",
      "url": "https://data.alpaca.markets"
    },
    {
      "description": "Sandbox",
      "url": "https://data.sandbox.alpaca.markets"
    }
  ],
  "tags": [
    {
      "description": "Corporate actions (splits, dividends, etc.).",
      "name": "Corporate actions"
    }
  ]
}
```