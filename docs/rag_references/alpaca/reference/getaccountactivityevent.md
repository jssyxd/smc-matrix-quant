# Get a single activity (V2) event by event_id ULID.

Source: https://docs.alpaca.markets/us/reference/getaccountactivityevent.md

---
updatedAt: 2026-05-13T18:47:47.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get a single activity (V2) event by event_id ULID.

Returns a single account activity (V2) event for the specified account by ULID `event_id`, delivered as a server-sent event message.

This is the single-event counterpart to the `subscribeToActivitiesSSE` streaming endpoint, intended for re-fetching an individual activity that was previously observed on the activities stream.

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
    "schemas": {
      "AcatcActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonAcatActivityV2"
          }
        ],
        "description": "Automated customer account transfer service (cash)",
        "type": "object"
      },
      "AcatsActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonAcatActivityV2"
          },
          {
            "properties": {
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Automated customer account transfer service (stock)",
        "type": "object"
      },
      "ActivityEventV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ActivityEventV2CommonFields"
          },
          {
            "properties": {
              "details": {
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/ActivityV2DetailTRD"
                  },
                  {
                    "$ref": "#/components/schemas/ActivityV2DetailNTA"
                  }
                ]
              }
            },
            "required": [
              "details"
            ],
            "type": "object"
          }
        ],
        "description": "Represents an account activity, sent over the Event Streaming API.",
        "title": "ActivityEventV2",
        "type": "object"
      },
      "ActivityEventV2CommonFields": {
        "description": "Represents the common fields for all Activity V2 Events",
        "properties": {
          "account_id": {
            "description": "Account UUID",
            "format": "uuid",
            "type": "string"
          },
          "activity_subtype": {
            "description": "Sub category for activity type, if any",
            "type": "string"
          },
          "activity_type": {
            "description": "The type of the activity, which can be trade or any of the non trade activities",
            "type": "string"
          },
          "at": {
            "description": "Timestamp of event",
            "format": "date-time",
            "minLength": 1,
            "type": "string"
          },
          "currency": {
            "description": "Currency code in ISO format",
            "type": "string"
          },
          "event_id": {
            "description": "Lexically sortable, monotonically increasing character string",
            "format": "ulid",
            "type": "string"
          },
          "executed_at": {
            "description": "Execution time for the activity event",
            "format": "date-time",
            "minLength": 1,
            "type": "string"
          },
          "net_amount": {
            "description": "The net amount of money (positive or negative) associated with the activity",
            "format": "decimal",
            "type": "string"
          },
          "previous_id": {
            "description": "Previous ID is presented if this activity corrects or cancels a previous trade or non trade activity. It contains execution_id or trns_id respectively",
            "format": "uuid",
            "type": "string"
          },
          "price": {
            "description": "The price of the security involved with the activity",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "The quantity of the security involved with the activity",
            "format": "decimal",
            "type": "string"
          },
          "ref_id": {
            "description": "The unique identifier for the activity. For trades, the execution_id is used, for other activities the trns_id is used.",
            "format": "uuid",
            "type": "string"
          },
          "settle_date": {
            "description": "Date when the activity settled",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "status": {
            "description": "Status of the activity",
            "type": "string"
          },
          "swap_fee_bps": {
            "description": "Currency conversion fee rate base-point in case of local currency activity",
            "format": "decimal",
            "type": "string"
          },
          "swap_rate": {
            "description": "Conversion rate for local currency activities",
            "format": "decimal",
            "type": "string"
          }
        },
        "required": [
          "account_id",
          "at",
          "event_id",
          "activity_type",
          "executed_at",
          "status",
          "settle_date",
          "currency",
          "ref_id"
        ],
        "type": "object"
      },
      "ActivityV2DetailNTA": {
        "oneOf": [
          {
            "$ref": "#/components/schemas/DIVSPDActivityV2"
          },
          {
            "$ref": "#/components/schemas/CDIVActivityV2"
          },
          {
            "$ref": "#/components/schemas/SDIVActivityV2"
          },
          {
            "$ref": "#/components/schemas/CGDActivityV2"
          },
          {
            "$ref": "#/components/schemas/ForwardSplitActivityV2"
          },
          {
            "$ref": "#/components/schemas/ReverseSplitActivityV2"
          },
          {
            "$ref": "#/components/schemas/UnitSplitActivityV2"
          },
          {
            "$ref": "#/components/schemas/SpinoffActivityV2"
          },
          {
            "$ref": "#/components/schemas/MAActivityV2"
          },
          {
            "$ref": "#/components/schemas/NCActivityV2"
          },
          {
            "$ref": "#/components/schemas/FixedIncomeRedemptionActivityV2"
          },
          {
            "$ref": "#/components/schemas/FixedIncomeInterestActivityV2"
          },
          {
            "$ref": "#/components/schemas/REOActivityV2"
          },
          {
            "$ref": "#/components/schemas/RightsDistributionActivityV2"
          },
          {
            "$ref": "#/components/schemas/RightsSubscriptionElectionActivityV2"
          },
          {
            "$ref": "#/components/schemas/TenderOfferActivityV2"
          },
          {
            "$ref": "#/components/schemas/ExchangeOfferActivityV2"
          },
          {
            "$ref": "#/components/schemas/WarrantExerciseElectionActivityV2"
          },
          {
            "$ref": "#/components/schemas/WRMActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaCDIVActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaSDIVActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaMAActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaNCActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaSPINActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaFSPLITActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaRSPLITActivityV2"
          },
          {
            "$ref": "#/components/schemas/OpcaUSPLITActivityV2"
          },
          {
            "$ref": "#/components/schemas/OPASNActivityV2"
          },
          {
            "$ref": "#/components/schemas/OPEXCActivityV2"
          },
          {
            "$ref": "#/components/schemas/OPEXPActivityV2"
          },
          {
            "$ref": "#/components/schemas/OPTRDActivityV2"
          },
          {
            "$ref": "#/components/schemas/OPCSHActivityV2"
          },
          {
            "$ref": "#/components/schemas/AcatsActivityV2"
          },
          {
            "$ref": "#/components/schemas/AcatcActivityV2"
          },
          {
            "$ref": "#/components/schemas/FOPTActivityV2"
          },
          {
            "$ref": "#/components/schemas/DIVNRAActivityV2"
          },
          {
            "$ref": "#/components/schemas/DIVWHActivityV2"
          },
          {
            "$ref": "#/components/schemas/JNLSActivityV2"
          },
          {
            "$ref": "#/components/schemas/JNLCActivityV2"
          },
          {
            "$ref": "#/components/schemas/CSWActivityV2"
          },
          {
            "$ref": "#/components/schemas/FEEActivityV2"
          },
          {
            "$ref": "#/components/schemas/MEMActivityV2"
          },
          {
            "$ref": "#/components/schemas/OCTActivityV2"
          }
        ],
        "type": "object"
      },
      "ActivityV2DetailTRD": {
        "description": "Activity details for a fill or partial_fill event",
        "properties": {
          "asset_id": {
            "description": "Asset ID (For options this represents the option contract ID)",
            "format": "uuid",
            "type": "string"
          },
          "client_order_id": {
            "description": "Order ID provided by the customer",
            "type": "string"
          },
          "commission": {
            "description": "Commission to collect from the account holder",
            "format": "decimal",
            "type": "string"
          },
          "cum_qty": {
            "description": "Total filled quantity on the order",
            "format": "decimal",
            "type": "string"
          },
          "cusip": {
            "description": "CUSIP of the security involved with the activity",
            "type": "string"
          },
          "execution_type": {
            "description": "The execution type",
            "enum": [
              "fill",
              "trade_correct",
              "trade_bust"
            ],
            "type": "string"
          },
          "leaves_qty": {
            "description": "Unfilled quantity on the order, when order is filled value could be 0",
            "format": "decimal",
            "type": "string"
          },
          "order_id": {
            "description": "Order ID generated by Alpaca",
            "format": "uuid",
            "type": "string"
          },
          "order_status": {
            "description": "Identifies the current status of the order",
            "type": "string"
          },
          "side": {
            "description": "Represents what side of the transaction an order was on",
            "enum": [
              "buy",
              "sell"
            ],
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the security involved with the activity",
            "type": "string"
          }
        },
        "required": [
          "order_id",
          "side",
          "symbol",
          "asset_id",
          "leaves_qty",
          "cum_qty",
          "order_status",
          "execution_type"
        ],
        "type": "object"
      },
      "CDIVActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonCDIVActivityV2"
          },
          {
            "properties": {
              "cash_payout": {
                "description": "Total cash amount paid",
                "type": "string"
              },
              "entitled_qty": {
                "description": "Quantity of shares entitled to receive the dividend or return of capital",
                "type": "string"
              }
            },
            "required": [
              "entitled_qty",
              "cash_payout"
            ],
            "type": "object"
          }
        ],
        "description": "Cash-dividend related details. Used for both Cash Dividend and Return of Capital.",
        "type": "object"
      },
      "CGDActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "properties": {
              "cash_payout": {
                "description": "Cash amount paid for this leg",
                "type": "string"
              },
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "entitled_qty": {
                "description": "Quantity of shares entitled to receive the capital gains distribution",
                "type": "string"
              },
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "isin": {
                "description": "The ISIN of the security involved with the activity",
                "type": "string"
              },
              "long_term_rate": {
                "description": "Long-term capital gains distribution rate per share, when applicable",
                "type": "string"
              },
              "payable_date": {
                "description": "The payable_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "rate": {
                "description": "Distribution rate per share for this leg (LTCG or STCG)",
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "short_term_rate": {
                "description": "Short-term capital gains distribution rate per share, when applicable",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "entitled_qty",
              "cash_payout",
              "symbol",
              "cusip",
              "rate"
            ],
            "type": "object"
          }
        ],
        "description": "Capital gains distribution. Used for both Long-Term (LTCG) and Short-Term (STCG) sub-types. Each activity represents a single leg; `long_term_rate` and/or `short_term_rate` are populated based on the source event, and `rate` matches the leg's own rate.",
        "type": "object"
      },
      "CSWActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "bank_transaction_id": {
                "description": "The bank transaction's ID",
                "format": "uuid",
                "type": "string"
              }
            },
            "type": "object"
          }
        ],
        "description": "Cash withdrawal",
        "type": "object"
      },
      "CommonAcatActivityV2": {
        "properties": {
          "external_id": {
            "description": "The ID that DTCC assigned to this transfer",
            "type": "string"
          },
          "hold_date": {
            "description": "Hold date when the transfers settle",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "request_id": {
            "description": "The ID for original ACATS request",
            "format": "uuid",
            "type": "string"
          }
        },
        "required": [
          "external_id",
          "request_id"
        ],
        "type": "object"
      },
      "CommonCDIVActivityV2": {
        "properties": {
          "cusip": {
            "description": "The CUSIP of the security involved with the activity",
            "type": "string"
          },
          "due_bill_off_date": {
            "description": "When due bills stop applying for this event",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "due_bill_on_date": {
            "description": "When due bills begin to apply for this event",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "ex_date": {
            "description": "The ex_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "foreign": {
            "description": "Indicates if related to a non-US security. Serialized as the JSON strings `\"true\"` or `\"false\"`, not a JSON boolean.",
            "enum": [
              "true",
              "false"
            ],
            "example": "false",
            "type": "string"
          },
          "isin": {
            "description": "The ISIN of the security involved with the activity",
            "type": "string"
          },
          "payable_date": {
            "description": "The payable_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "rate": {
            "description": "Dividend rate per share",
            "type": "string"
          },
          "record_date": {
            "description": "The record_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "special": {
            "description": "Indicates if this is a special dividend. Serialized as the JSON strings `\"true\"` or `\"false\"`, not a JSON boolean.",
            "enum": [
              "true",
              "false"
            ],
            "example": "false",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the security involved with the activity",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "cusip",
          "rate",
          "foreign",
          "special"
        ],
        "type": "object"
      },
      "CommonCaActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "ca_id": {
                "description": "The unique identifier for this corporate action",
                "format": "uuid",
                "type": "string"
              },
              "position_date": {
                "description": "The position_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "reorg_id": {
                "description": "The reorg identifier, if present in the source corporate action definition",
                "type": "string"
              }
            },
            "required": [
              "position_date"
            ],
            "type": "object"
          }
        ],
        "type": "object"
      },
      "CommonFixedIncomeInterestActivityV2": {
        "description": "Fixed income interest fields (INT/FI). Variants from the same activity type:\n\n- Coupon: `interest_type` is `coupon`. Includes `rate` (no `price` / `accrued_interest_rate`). No `order_id`.\n- Accrued interest on call: `interest_type` is `accrued`. Includes `price` and `accrued_interest_rate` (no `rate`). No `order_id`.\n- Trade accrued: `interest_type` is `accrued`. Includes `order_id` so the interest NTA can be linked to the fill. `parent_id` is set when a parent trade `ref_id` is available.",
        "properties": {
          "accrued_interest_rate": {
            "description": "Accrued interest rate (present for accrued-interest-on-call variants)",
            "format": "decimal",
            "type": "string"
          },
          "cash_payout": {
            "description": "The cash payout for this interest activity",
            "format": "decimal",
            "type": "string"
          },
          "cusip": {
            "description": "The CUSIP of the security involved with the activity",
            "type": "string"
          },
          "entitled_qty": {
            "description": "The entitled quantity (principal / face amount)",
            "example": "1000",
            "type": "string"
          },
          "interest_type": {
            "$ref": "#/components/schemas/FixedIncomeInterestType"
          },
          "isin": {
            "description": "The ISIN of the security involved with the activity",
            "type": "string"
          },
          "order_id": {
            "description": "The order that generated this accrued interest. Present for trade-accrued INT/FI.",
            "example": "257bf308-a6b7-4777-8cf6-00dc441dc4d3",
            "format": "uuid",
            "type": "string"
          },
          "parent_id": {
            "description": "The ref_id of the parent trade this interest is attached to. Present for trade-accrued INT/FI when a parent trade `ref_id` is available.",
            "example": "46aecae1-4629-4bcf-b441-0d8c847a1787",
            "format": "uuid",
            "type": "string"
          },
          "payment_date": {
            "description": "The payment date",
            "format": "date",
            "type": "string"
          },
          "price": {
            "description": "Call price used for accrued-interest-on-call variants",
            "format": "decimal",
            "type": "string"
          },
          "rate": {
            "description": "Coupon rate amount (present for regular coupon payments)",
            "format": "decimal",
            "type": "string"
          },
          "record_date": {
            "description": "The record date",
            "format": "date",
            "type": "string"
          }
        },
        "required": [
          "entitled_qty",
          "cash_payout",
          "cusip",
          "interest_type"
        ],
        "type": "object"
      },
      "CommonJournalActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "journal_id": {
                "description": "The journal's ID",
                "format": "uuid",
                "type": "string"
              }
            },
            "type": "object"
          }
        ],
        "description": "Shared fields for journal non-trade activity records.",
        "type": "object"
      },
      "CommonMAActivityV2": {
        "properties": {
          "acquiree_cusip": {
            "description": "CUSIP of the acquiree",
            "type": "string"
          },
          "acquiree_isin": {
            "description": "ISIN of the acquiree",
            "type": "string"
          },
          "acquiree_rate": {
            "description": "Rate of the acquiree",
            "type": "string"
          },
          "acquiree_symbol": {
            "description": "Symbol of the acquiree",
            "type": "string"
          },
          "acquirer_cusip": {
            "description": "CUSIP of the acquirer",
            "type": "string"
          },
          "acquirer_isin": {
            "description": "ISIN of the acquirer",
            "type": "string"
          },
          "acquirer_rate": {
            "description": "Rate of the acquirer",
            "type": "string"
          },
          "acquirer_symbol": {
            "description": "Symbol of the acquirer",
            "type": "string"
          },
          "effective_date": {
            "description": "When the merger/acquisition becomes effective",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "payable_date": {
            "description": "The payable date",
            "format": "date",
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "acquiree_cusip",
          "acquiree_symbol",
          "effective_date",
          "payable_date"
        ],
        "type": "object"
      },
      "CommonNCActivityV2": {
        "properties": {
          "new_cusip": {
            "description": "New CUSIP for the name change",
            "type": "string"
          },
          "new_symbol": {
            "description": "New symbol for the name change",
            "type": "string"
          },
          "old_cusip": {
            "description": "Old CUSIP for the name change",
            "type": "string"
          },
          "old_symbol": {
            "description": "Old symbol for the name change",
            "type": "string"
          }
        },
        "required": [
          "old_cusip",
          "old_symbol",
          "new_cusip",
          "new_symbol"
        ],
        "type": "object"
      },
      "CommonNTAActivityV2": {
        "description": "Shared fields for non-trade (NTA) activity records.",
        "properties": {
          "group_id": {
            "description": "Optional group ID which can help grouping together related activities",
            "format": "uuid",
            "type": "string"
          },
          "system_date": {
            "description": "The date when the activity was booked",
            "format": "date",
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "system_date"
        ],
        "type": "object"
      },
      "CommonOPCAActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "properties": {
              "new_contract_symbol": {
                "description": "The new contract symbol",
                "type": "string"
              },
              "new_qty": {
                "description": "used when the old contract's quantity is not equal to the new contract's quantity. Mutually exclusive with 'qty'.",
                "type": "string"
              },
              "old_contract_symbol": {
                "description": "The old contract symbol",
                "type": "string"
              },
              "old_qty": {
                "description": "used when the old contract's quantity is not equal to the new contract's quantity. Mutually exclusive with 'qty'.",
                "type": "string"
              },
              "qty": {
                "description": "used when the old contract's quantity is equal to the new contract's quantity. Mutually exclusive with 'old_qty' and 'new_qty'",
                "type": "string"
              }
            },
            "required": [
              "old_contract_symbol",
              "new_contract_symbol"
            ],
            "type": "object"
          }
        ],
        "type": "object"
      },
      "CommonOptionsActivityV2": {
        "allOf": [
          {
            "description": "Shared fields for option-related non-trade activity records.",
            "properties": {
              "contract_symbol": {
                "description": "The contract symbol of the security involved with the activity",
                "type": "string"
              },
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "group_id"
            ],
            "type": "object"
          },
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          }
        ]
      },
      "CommonREOActivityV2": {
        "description": "Reorganization (REO) activity sub-types:\n- **REOS**: Stock only (1 or more stock legs)\n- **REOC**: Cash only (one cash leg)\n- **REOSC**: Stock and cash",
        "properties": {
          "cash_payout": {
            "description": "Cash payout amount",
            "format": "decimal",
            "type": "string"
          },
          "cash_rate": {
            "description": "Cash rate per share",
            "format": "decimal",
            "type": "string"
          },
          "cusip": {
            "description": "CUSIP received on this stock leg",
            "type": "string"
          },
          "effective_date": {
            "description": "Effective date of the reorganization",
            "format": "date",
            "type": "string"
          },
          "isin": {
            "description": "ISIN received on this stock leg",
            "type": "string"
          },
          "new_rate": {
            "description": "New ratio for this stock leg",
            "format": "decimal",
            "type": "string"
          },
          "payable_date": {
            "description": "Payable date of the reorganization",
            "format": "date",
            "type": "string"
          },
          "qty": {
            "description": "Quantity received on this stock leg",
            "format": "decimal",
            "type": "string"
          },
          "removed_qty": {
            "description": "Positive quantity removed from the source position",
            "format": "decimal",
            "type": "string"
          },
          "source_cusip": {
            "description": "CUSIP of the source security",
            "type": "string"
          },
          "source_isin": {
            "description": "ISIN of the source security",
            "type": "string"
          },
          "source_qty": {
            "description": "Source position quantity",
            "format": "decimal",
            "type": "string"
          },
          "source_rate": {
            "description": "Source ratio for this stock leg",
            "format": "decimal",
            "type": "string"
          },
          "source_symbol": {
            "description": "Symbol of the source security",
            "example": "CEPT",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol received on this stock leg",
            "example": "SECZ",
            "type": "string"
          }
        },
        "required": [
          "source_symbol",
          "source_cusip",
          "payable_date"
        ],
        "type": "object"
      },
      "CommonSDIVActivityV2": {
        "properties": {
          "cusip": {
            "description": "The CUSIP of the security involved with the activity",
            "type": "string"
          },
          "ex_date": {
            "description": "The ex_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "isin": {
            "description": "The ISIN of the security involved with the activity",
            "type": "string"
          },
          "payable_date": {
            "description": "The payable_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "rate": {
            "description": "Dividend rate per share",
            "type": "string"
          },
          "record_date": {
            "description": "The record_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the security involved with the activity",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "cusip",
          "rate"
        ],
        "type": "object"
      },
      "CommonSpinoffActivityV2": {
        "properties": {
          "due_bill_redemption_date": {
            "description": "When due bills related to the spinoff are redeemed",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "ex_date": {
            "description": "The ex_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "new_cusip": {
            "description": "CUSIP of the new security",
            "type": "string"
          },
          "new_isin": {
            "description": "ISIN of the new security",
            "type": "string"
          },
          "new_price": {
            "description": "Market price of new shares after the spinoff",
            "type": "string"
          },
          "new_rate": {
            "description": "Ratio of new shares received",
            "type": "string"
          },
          "new_symbol": {
            "description": "Symbol of the new security",
            "type": "string"
          },
          "payable_date": {
            "description": "The payable_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "record_date": {
            "description": "The record_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          },
          "source_cusip": {
            "description": "CUSIP of the parent security",
            "type": "string"
          },
          "source_isin": {
            "description": "ISIN of the parent security",
            "type": "string"
          },
          "source_price": {
            "description": "Market price of parent shares before the spinoff",
            "type": "string"
          },
          "source_rate": {
            "description": "Ratio of parent shares",
            "type": "string"
          },
          "source_symbol": {
            "description": "Symbol of the parent security",
            "type": "string"
          }
        },
        "required": [
          "source_cusip",
          "source_symbol",
          "source_rate",
          "source_price",
          "new_cusip",
          "new_symbol",
          "new_rate",
          "new_price"
        ],
        "type": "object"
      },
      "CommonSplitActivityV2": {
        "properties": {
          "new_cusip": {
            "description": "CUSIP of the new security after the split",
            "type": "string"
          },
          "new_isin": {
            "description": "ISIN of the new security after the split",
            "type": "string"
          },
          "new_rate": {
            "description": "Ratio of new shares received",
            "type": "string"
          },
          "old_cusip": {
            "description": "CUSIP of the old security before the split",
            "type": "string"
          },
          "old_isin": {
            "description": "ISIN of the old security before the split",
            "type": "string"
          },
          "old_rate": {
            "description": "Ratio of old shares exchanged",
            "type": "string"
          },
          "payable_date": {
            "description": "The payable_date for this corporate action",
            "format": "date",
            "minLength": 1,
            "type": "string"
          }
        },
        "required": [
          "old_cusip",
          "new_cusip",
          "old_rate",
          "new_rate"
        ],
        "type": "object"
      },
      "CommonSplitStockActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSplitActivityV2"
          },
          {
            "properties": {
              "new_qty": {
                "description": "The new quantity after the split",
                "type": "string"
              },
              "old_qty": {
                "description": "The old quantity before the split",
                "type": "string"
              }
            },
            "required": [
              "old_qty",
              "new_qty"
            ],
            "type": "object"
          }
        ],
        "type": "object"
      },
      "CommonVOFSubtypeActivityV2": {
        "properties": {
          "new_cusip": {
            "description": "CUSIP of the new security",
            "type": "string"
          },
          "new_symbol": {
            "description": "Symbol of the new security",
            "type": "string"
          },
          "source_cusip": {
            "description": "CUSIP of the parent security",
            "type": "string"
          },
          "source_symbol": {
            "description": "Symbol of the parent security",
            "type": "string"
          }
        },
        "required": [
          "source_cusip",
          "source_symbol"
        ],
        "type": "object"
      },
      "DIVNRAActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "parent_id": {
                "description": "The ref_id of the parent dividend",
                "format": "uuid",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              },
              "tax_country": {
                "description": "Tax country used as the primary jurisdiction when determining withholding treatment for the dividend. Other factors may affect the final withholding rate.\nThe value is an [ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html) country code.\n",
                "example": "THA",
                "type": "string"
              },
              "tax_rate": {
                "description": "The tax withholding rate applied to the dividend, represented as a value between 0 and 1",
                "example": "0.15",
                "format": "decimal",
                "type": "string"
              }
            },
            "required": [
              "cusip",
              "symbol",
              "parent_id"
            ],
            "type": "object"
          }
        ],
        "description": "Dividend withholding for non resident aliens",
        "type": "object"
      },
      "DIVSPDActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "properties": {
              "cash_payout": {
                "description": "Total cash amount paid",
                "type": "string"
              },
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "due_bill_off_date": {
                "description": "When due bills stop applying for this event",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "due_bill_on_date": {
                "description": "When due bills begin to apply for this event",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "entitled_qty": {
                "description": "Quantity of shares entitled to receive cash in lieu",
                "type": "string"
              },
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "foreign": {
                "description": "Indicates if related to a non-US security. Serialized as the JSON strings `\"true\"` or `\"false\"`, not a JSON boolean.",
                "enum": [
                  "true",
                  "false"
                ],
                "example": "false",
                "type": "string"
              },
              "isin": {
                "description": "The ISIN of the security involved with the activity",
                "type": "string"
              },
              "payable_date": {
                "description": "The payable_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "rate": {
                "description": "Cash payout per share",
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "special": {
                "description": "Indicates if this is a special dividend. Serialized as the JSON strings `\"true\"` or `\"false\"`, not a JSON boolean.",
                "enum": [
                  "true",
                  "false"
                ],
                "example": "false",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "entitled_qty",
              "cash_payout",
              "symbol",
              "cusip",
              "rate",
              "foreign",
              "special"
            ],
            "type": "object"
          }
        ],
        "description": "Substitute payment in lieu of dividend",
        "type": "object"
      },
      "DIVWHActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "isin": {
                "description": "The ISIN of the security involved with the activity",
                "type": "string"
              },
              "parent_id": {
                "description": "The ref_id of the parent dividend",
                "format": "uuid",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "cusip",
              "symbol",
              "parent_id"
            ],
            "type": "object"
          }
        ],
        "description": "Dividend tax withholding (e.g. foreign withholding on global securities)",
        "type": "object"
      },
      "ExchangeOfferActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonVOFSubtypeActivityV2"
          }
        ],
        "type": "object"
      },
      "FEEActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "parent_id": {
                "description": "The parent transaction's ID",
                "format": "uuid",
                "type": "string"
              }
            },
            "required": [
              "parent_id"
            ],
            "type": "object"
          }
        ],
        "description": "Fee",
        "type": "object"
      },
      "FOPTActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "contra": {
                "description": "Contra for the transfer",
                "type": "string"
              },
              "external_id": {
                "description": "External ID of the transfer",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "external_id",
              "contra",
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Free-of-payment (FOP) transfers",
        "type": "object"
      },
      "FixedIncomeInterestActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonFixedIncomeInterestActivityV2"
          }
        ],
        "description": "Fixed income interest (INT/FI)",
        "type": "object"
      },
      "FixedIncomeInterestType": {
        "description": "Distinguishes coupon payments from accrued interest on INT/FI activities.",
        "enum": [
          "coupon",
          "accrued"
        ],
        "example": "accrued",
        "title": "FixedIncomeInterestType",
        "type": "string"
      },
      "FixedIncomeRedemptionActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "ca_id": {
                "description": "The unique identifier for this corporate action",
                "type": "string"
              },
              "cash_payout": {
                "description": "The cash payout",
                "type": "string"
              },
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "payment_date": {
                "description": "The payment date",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "qty": {
                "description": "Quantity for the redemption",
                "type": "string"
              }
            },
            "required": [
              "ca_id",
              "payment_date",
              "cusip",
              "qty",
              "cash_payout"
            ],
            "type": "object"
          }
        ],
        "description": "Redemption",
        "type": "object"
      },
      "ForwardSplitActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonSplitStockActivityV2"
          },
          {
            "properties": {
              "due_bill_redemption_date": {
                "description": "When due bills related to the split are redeemed",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security being split",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Forward stock split",
        "type": "object"
      },
      "JNLCActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonJournalActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Journal entry (cash)",
        "type": "object"
      },
      "JNLSActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonJournalActivityV2"
          },
          {
            "properties": {
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Journal entry (stock)",
        "type": "object"
      },
      "MAActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonMAActivityV2"
          },
          {
            "properties": {
              "acquiree_qty": {
                "description": "Quantity of the acquiree",
                "type": "string"
              },
              "acquirer_qty": {
                "description": "Quantity of the acquirer",
                "type": "string"
              },
              "cash_payout": {
                "description": "The cash payout",
                "type": "string"
              },
              "cash_rate": {
                "description": "The cash rate",
                "type": "string"
              }
            },
            "required": [
              "acquiree_qty"
            ],
            "type": "object"
          }
        ],
        "description": "Merger and acquisition",
        "type": "object"
      },
      "MEMActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "transfer_id": {
                "description": "The transfer's ID",
                "format": "uuid",
                "type": "string"
              }
            },
            "required": [
              "transfer_id"
            ],
            "type": "object"
          }
        ],
        "description": "Instant funding memopost",
        "type": "object"
      },
      "NCActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonNCActivityV2"
          },
          {
            "properties": {
              "position_qty": {
                "description": "The position quantity",
                "type": "string"
              }
            },
            "required": [
              "position_qty"
            ],
            "type": "object"
          }
        ],
        "description": "Name change",
        "type": "object"
      },
      "OCTActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "properties": {
              "symbol": {
                "description": "The symbol of the asset involved with the on chain transaction",
                "type": "string"
              },
              "transfer_id": {
                "description": "The transfer ID of the associated deposit or withdrawal",
                "format": "uuid",
                "type": "string"
              }
            },
            "required": [
              "transfer_id",
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "On chain transaction (blockchain deposit/withdrawal)",
        "type": "object"
      },
      "OPASNActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOptionsActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Option assignment",
        "type": "object"
      },
      "OPCSHActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOptionsActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Option cash deliverable for non-standard contracts",
        "type": "object"
      },
      "OPEXCActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOptionsActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Option exercise",
        "type": "object"
      },
      "OPEXPActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOptionsActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Option expiry",
        "type": "object"
      },
      "OPTRDActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOptionsActivityV2"
          },
          {
            "type": "object"
          }
        ],
        "description": "Trading activity that is paired with the assignment/exercise",
        "type": "object"
      },
      "OpcaCDIVActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonCDIVActivityV2"
          }
        ],
        "description": "Options corporate action of cash dividend or return of capital",
        "type": "object"
      },
      "OpcaFSPLITActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSplitActivityV2"
          },
          {
            "properties": {
              "due_bill_redemption_date": {
                "description": "When due bills related to the split are redeemed",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Options corporate action of forward-splits",
        "type": "object"
      },
      "OpcaMAActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonMAActivityV2"
          }
        ],
        "description": "Options corporate action of Mergers & Acquisitions",
        "type": "object"
      },
      "OpcaNCActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonNCActivityV2"
          }
        ],
        "description": "Options corporate action of name changes",
        "type": "object"
      },
      "OpcaRSPLITActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSplitActivityV2"
          },
          {
            "properties": {
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "new_symbol": {
                "description": "Symbol of the new security after the split",
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Options corporate action of reverse-splits",
        "type": "object"
      },
      "OpcaSDIVActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSDIVActivityV2"
          }
        ],
        "description": "Options corporate action of stock dividend",
        "type": "object"
      },
      "OpcaSPINActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSpinoffActivityV2"
          }
        ],
        "description": "Options corporate action of spin-offs",
        "type": "object"
      },
      "OpcaUSPLITActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonOPCAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSplitActivityV2"
          },
          {
            "properties": {
              "alternate_cusip": {
                "description": "CUSIP for the alternate security after the split",
                "type": "string"
              },
              "alternate_rate": {
                "description": "Ratio of alternate shares received",
                "type": "string"
              },
              "alternate_symbol": {
                "description": "Symbol for the alternate security after the split",
                "type": "string"
              },
              "effective_date": {
                "description": "When the unit split becomes effective",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "new_symbol": {
                "description": "Symbol of the new security after the unit split",
                "type": "string"
              },
              "old_symbol": {
                "description": "The old symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "old_symbol",
              "new_symbol",
              "alternate_cusip",
              "alternate_symbol",
              "alternate_rate",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "Options corporate action of unit-splits",
        "type": "object"
      },
      "REOActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonREOActivityV2"
          }
        ],
        "description": "Reorganization (REO)",
        "type": "object"
      },
      "ReverseSplitActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonSplitStockActivityV2"
          },
          {
            "properties": {
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "new_symbol": {
                "description": "Symbol of the new security after the split",
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "symbol"
            ],
            "type": "object"
          }
        ],
        "description": "Reverse stock split",
        "type": "object"
      },
      "RightsDistributionActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "properties": {
              "ex_date": {
                "description": "The ex_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "expiration_date": {
                "description": "The expiration date for the rights distribution",
                "format": "date",
                "type": "string"
              },
              "new_cusip": {
                "description": "The new CUSIP",
                "type": "string"
              },
              "new_qty": {
                "description": "The new quantity",
                "type": "string"
              },
              "new_symbol": {
                "description": "The new symbol",
                "type": "string"
              },
              "payable_date": {
                "description": "The payable_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "rate": {
                "description": "The rate for the rights distribution",
                "type": "string"
              },
              "record_date": {
                "description": "The record_date for this corporate action",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "source_cusip": {
                "description": "The source CUSIP",
                "type": "string"
              },
              "source_qty": {
                "description": "The source quantity",
                "type": "string"
              },
              "source_symbol": {
                "description": "The source symbol",
                "type": "string"
              }
            },
            "required": [
              "source_cusip",
              "source_symbol",
              "source_qty",
              "new_cusip",
              "new_symbol",
              "new_qty",
              "rate"
            ],
            "type": "object"
          }
        ],
        "description": "Rights distribution",
        "type": "object"
      },
      "RightsSubscriptionElectionActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonVOFSubtypeActivityV2"
          }
        ],
        "type": "object"
      },
      "SDIVActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSDIVActivityV2"
          },
          {
            "properties": {
              "entitled_qty": {
                "description": "Quantity of shares entitled to receive the dividend",
                "type": "string"
              },
              "new_qty": {
                "description": "The total number of shares after the dividend",
                "type": "string"
              },
              "paid_qty": {
                "description": "The paid quantity",
                "type": "string"
              }
            },
            "required": [
              "entitled_qty",
              "paid_qty",
              "new_qty"
            ],
            "type": "object"
          }
        ],
        "description": "Stock dividend",
        "type": "object"
      },
      "SpinoffActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonSpinoffActivityV2"
          },
          {
            "properties": {
              "new_qty": {
                "description": "The new quantity",
                "type": "string"
              },
              "source_qty": {
                "description": "The source quantity",
                "type": "string"
              }
            },
            "required": [
              "source_qty",
              "new_qty"
            ],
            "type": "object"
          }
        ],
        "description": "Spinoff",
        "type": "object"
      },
      "TenderOfferActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonVOFSubtypeActivityV2"
          }
        ],
        "type": "object"
      },
      "UnitSplitActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonSplitStockActivityV2"
          },
          {
            "properties": {
              "alternate_cusip": {
                "description": "CUSIP for the alternate security after the split",
                "type": "string"
              },
              "alternate_isin": {
                "description": "ISIN for the alternate security after the split",
                "type": "string"
              },
              "alternate_qty": {
                "description": "Quantity of alternate shares received",
                "type": "string"
              },
              "alternate_rate": {
                "description": "Ratio of alternate shares received",
                "type": "string"
              },
              "alternate_symbol": {
                "description": "Symbol for the alternate security after the split",
                "type": "string"
              },
              "effective_date": {
                "description": "When the unit split becomes effective",
                "format": "date",
                "minLength": 1,
                "type": "string"
              },
              "new_symbol": {
                "description": "Symbol of the new security after the split",
                "type": "string"
              },
              "old_symbol": {
                "description": "Symbol of the old security before the split",
                "type": "string"
              }
            },
            "required": [
              "old_symbol",
              "new_symbol",
              "alternate_cusip",
              "alternate_symbol",
              "alternate_rate",
              "alternate_qty",
              "effective_date"
            ],
            "type": "object"
          }
        ],
        "description": "Unit split",
        "type": "object"
      },
      "WRMActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonCaActivityV2"
          },
          {
            "properties": {
              "cusip": {
                "description": "The CUSIP of the security involved with the activity",
                "type": "string"
              },
              "isin": {
                "description": "The ISIN of the security involved with the activity",
                "type": "string"
              },
              "removed_qty": {
                "description": "The removed quantity",
                "type": "string"
              },
              "symbol": {
                "description": "The symbol of the security involved with the activity",
                "type": "string"
              }
            },
            "required": [
              "cusip",
              "symbol",
              "removed_qty"
            ],
            "type": "object"
          }
        ],
        "description": "Worthless Removal",
        "type": "object"
      },
      "WarrantExerciseElectionActivityV2": {
        "allOf": [
          {
            "$ref": "#/components/schemas/CommonNTAActivityV2"
          },
          {
            "$ref": "#/components/schemas/CommonVOFSubtypeActivityV2"
          }
        ],
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
    "/v2beta1/accounts/{account_id}/events/activities/{event_id}": {
      "get": {
        "description": "Returns a single account activity (V2) event for the specified account by ULID `event_id`, delivered as a server-sent event message.\n\nThis is the single-event counterpart to the `subscribeToActivitiesSSE` streaming endpoint, intended for re-fetching an individual activity that was previously observed on the activities stream.",
        "operationId": "getAccountActivityEvent",
        "responses": {
          "200": {
            "content": {
              "text/event-stream": {
                "schema": {
                  "$ref": "#/components/schemas/ActivityEventV2"
                }
              }
            },
            "description": "Returns a single activity v2 event, identified by the provided event_id  ULID."
          }
        },
        "summary": "Get a single activity (V2) event by event_id ULID.",
        "tags": [
          "Accounts"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        },
        {
          "description": "The ULID that uniquely identifies the activity event.",
          "in": "path",
          "name": "event_id",
          "required": true,
          "schema": {
            "format": "ulid",
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
      "name": "Accounts"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```