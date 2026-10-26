# Retrieve Account Activities

Source: https://docs.alpaca.markets/us/reference/getaccountactivities.md

---
updatedAt: 2026-05-27T17:58:38.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Account Activities

Returns a list of activities

Notes:
* Pagination is handled using the `page_token` and `page_size` parameters.
* `page_token` represents the ID of the last item on your current page of results.
   For example, if the ID of the last activity in your first response is `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you would pass that value as `page_token` to retrieve the next page of results.

* If specified with a `direction` of `desc`, for example, the results will end before the activity with the specified ID.
* If specified with a `direction` of `asc`, results will begin with the activity immediately after the one specified.
* `page_size` is the maximum number of entries to return in the response.
* If `date` is not specified, the default and maximum value is 100.
* If `date` is specified, the default behavior is to return all results, and there is no maximum page size.

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "Direction": {
        "description": "The chronological order of response based on the submission time. asc or desc. Defaults to desc.",
        "in": "query",
        "name": "direction",
        "schema": {
          "enum": [
            "asc",
            "desc"
          ],
          "example": "desc",
          "type": "string"
        }
      }
    },
    "schemas": {
      "Activity": {
        "allOf": [
          {
            "properties": {
              "account_id": {
                "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
                "format": "uuid",
                "type": "string"
              },
              "activity_type": {
                "$ref": "#/components/schemas/ActivityType"
              },
              "id": {
                "example": "20220208125959696::88b5f678-fef5-447b-af15-f21e367e6d8c",
                "type": "string"
              }
            },
            "type": "object"
          },
          {
            "oneOf": [
              {
                "$ref": "#/components/schemas/TradeActivity"
              },
              {
                "$ref": "#/components/schemas/NonTradeActivity"
              }
            ]
          }
        ],
        "description": "Base for activity types",
        "required": [
          "id",
          "activity_type"
        ],
        "title": "Activity"
      },
      "ActivitySubType": {
        "description": "Represents a more specific classification to the `activity_type`.\nThis field is optional and may not always be populated, depending on the activity type and the available data.\nEach `activity_type` has a set of valid `activity_sub_type` values.\n\nFull mapping of `activity_type` to `activity_sub_type`:\n\n- **CGD**: Capital Gains Distribution activity sub-types:\n  - **LTCG**: Long-Term Capital Gain\n  - **STCG**: Short-Term Capital Gain\n\n- **DIV**: Dividend activity sub-types:\n  - **CDIV**: Cash Dividend\n  - **ROC**: Return of Capital\n  - **SDIV**: Stock Dividend\n  - **SPD**: Substitute Payment In Lieu Of Dividend\n\n- **FEE**: Fee-related activity sub-types:\n  - **REG**: Regulatory Fee\n  - **TAF**: Trading Activity Fee\n  - **LCT**: Local Currency Trading Fee\n  - **ORF**: Options Regulatory Fee\n  - **OCC**: Options Clearing Corporation Fee\n  - **NRC**: Non-Retail Commission Fee\n  - **NRV**: Non-Retail Venue Fee\n  - **COM**: Commission\n  - **CAT**: Consolidated Audit Trail Fee\n\n- **INT**: Interest-related activity sub-types:\n  - **MGN**: Margin Interest\n  - **CDT**: Credit Interest\n  - **SWP**: Sweep Interest\n  - **QII**: Qualified Interest\n  - **FI**: Fixed Income Interest (coupon or accrued)\n\n- **MA**: Merger and Acquisition activity sub-types:\n  - **CMA**: Cash Merger\n  - **SMA**: Stock Merger\n  - **SCMA**: Stock & Cash Merger\n\n- **NC**: Name Change activity sub types\n  - **SNC**: Symbol Name Change\n  - **CNC**: CUSIP Name Change\n  - **SCNC**: Symbol & CUSIP Name Change\n\n- **OPCA**: Option Corporate Action activity sub-types:\n  - **DIV.CDIV**: Cash Dividend\n  - **DIV.ROC**: Return of Capital\n  - **DIV.SDIV**: Stock Dividend\n  - **MA.CMA**: Cash Merger\n  - **MA.SMA**: Stock Merger\n  - **MA.SCMA**: Stock & Cash Merger\n  - **NC.CNC**: CUSIP Name Change\n  - **NC.SNC**: Symbol Name Change\n  - **NC.SCNC**: Symbol & CUSIP Name Change\n  - **SPIN**: Spin-off\n  - **SPLIT.FSPLIT**: Forward Stock Split\n  - **SPLIT.RSPLIT**: Reverse Stock Split\n  - **SPLIT.USPLIT**: Unit Split\n\n- **REO**: Reorganization activity sub-types:\n  - **REOS**: Stock only (1 or more stock legs)\n  - **REOC**: Cash only (one cash leg)\n  - **REOSC**: Stock and cash\n\n- **REORG**: Activity sub-types:\n  - **WRM**: Worthless Removal\n\n- **SPLIT**: Stock Split activity sub-types:\n  - **FSPLIT**: Forward Stock Split\n  - **RSPLIT**: Reverse Stock Split\n  - **USPLIT**: Unit Split\n\n- **VOF**: Voluntary Offering activity sub-types:\n  - **VTND**: Tender Offer\n  - **VWRT**: Warrant Exercise\n  - **VRGT**: Rights Offer\n  - **VEXH**: Exchange Offer\n\n- **WH**: Withholding activity sub-types:\n  - **SWH**: State Withholding\n  - **FWH**: Federal Withholding\n  - **SLWH**: Sales Withholding",
        "title": "ActivitySubType",
        "type": "string"
      },
      "ActivityType": {
        "description": "Represents the various kinds of activity.\n\nTradeActivity's will always have the type `FILL`\n\n- **FILL**\n  Order Fills (Partial/Full)\n- **ACATC**\n  ACATS IN/OUT (Cash)\n- **ACATS**\n  ACATS IN/OUT (Securities)\n- **CGD**\n  Capital Gains Distribution\n- **CIL**\n  Cash in Lieu of Stock\n- **CSD**\n  Cash Disbursement (+)\n- **CSW**\n  Cash Withdrawable\n- **DIV**\n  Dividend\n- **DIVCGL**\n  Dividend (Capital Gains Long Term)\n- **DIVCGS**\n  Dividend (Capital Gains Short Term)\n- **DIVNRA**\n  Dividend Adjusted (NRA Withheld)\n- **DIVROC**\n  Dividend Return of Capital\n- **DIVTXEX**\n  Dividend (Tax Exempt)\n- **FEE**\n  REG and TAF Fees\n- **INT**\n  Interest (Credit/Margin)\n- **JNLC**\n  Journal Entry (Cash)\n- **JNLS**\n  Journal Entry (Stock)\n- **OPASN**\n   Option Assignment\n- **OPCA**\n  Option Corporate Action\n- **OPCSH**\n   Option cash deliverable for non-standard contracts\n- **OPEXC**\n  Option Exercise\n- **OPEXP**\n  Option Expiration\n- **OPTRD**\n  Option Trade\n- **MA**\n  Merger/Acquisition\n- **PTC**\n  Pass Thru Change\n- **REO**\n  Reorganization\n- **REORG**\n  Worthless removal CA\n- **SPIN**\n  Stock Spinoff\n- **SPLIT**\n  Stock Split\n- **FOPT**\n  Free of Payment Transfers\n- **OCT**\n  On Chain Transactions (blockchain deposits/withdrawals)",
        "enum": [
          "FILL",
          "ACATC",
          "ACATS",
          "CGD",
          "CIL",
          "CSD",
          "CSW",
          "DIV",
          "DIVCGL",
          "DIVCGS",
          "DIVNRA",
          "DIVROC",
          "DIVTXEX",
          "FEE",
          "INT",
          "JNLC",
          "JNLS",
          "MA",
          "OPASN",
          "OPCA",
          "OPCSH",
          "OPEXC",
          "OPEXP",
          "OPTRD",
          "PTC",
          "REO",
          "REORG",
          "SPIN",
          "SPLIT",
          "FOPT",
          "OCT"
        ],
        "title": "ActivityType",
        "type": "string"
      },
      "NonTradeActivity": {
        "properties": {
          "activity_sub_type": {
            "$ref": "#/components/schemas/ActivitySubType"
          },
          "created_at": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "2021-05-10T14:01:04.650275Z",
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "Currency denomination of the activity. USD by default.",
            "type": "string"
          },
          "cusip": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "037833100",
            "type": "string"
          },
          "date": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "2021-05-21",
            "format": "date",
            "type": "string"
          },
          "description": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "Example description",
            "type": "string"
          },
          "group_id": {
            "description": "ID used to link activities who share a sibling relationship",
            "example": "13d96cf3-1cbe-4632-b2f2-86a9df5a3b9d",
            "format": "uuid",
            "type": "string"
          },
          "net_amount": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "1234",
            "format": "decimal",
            "type": "string"
          },
          "per_share_amount": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "0.38921",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "0.38921",
            "format": "decimal",
            "type": "string"
          },
          "status": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "enum": [
              "executed",
              "correct",
              "canceled"
            ],
            "example": "executed",
            "type": "string"
          },
          "symbol": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "example": "AAPL",
            "type": "string"
          },
          "transfer_id": {
            "description": "The transfer ID of the associated deposit or withdrawal. Populated for `OCT` (On Chain Transactions) activities.",
            "example": "bacddbc5-1a45-4a54-8f6d-c3f2f9d2e2a1",
            "format": "uuid",
            "type": "string"
          }
        },
        "title": "NonTradeActivity",
        "type": "object"
      },
      "OrderSide": {
        "description": "Represents what side of the transaction an order was on. Required for all order classes except for `mleg`.",
        "enum": [
          "buy",
          "sell",
          "buy_minus",
          "sell_plus",
          "sell_short",
          "sell_short_exempt",
          "undisclosed",
          "cross",
          "cross_short"
        ],
        "example": "buy",
        "type": "string"
      },
      "OrderStatus": {
        "enum": [
          "new",
          "partially_filled",
          "filled",
          "done_for_day",
          "canceled",
          "expired",
          "replaced",
          "pending_cancel",
          "pending_replace",
          "accepted",
          "pending_new",
          "accepted_for_bidding",
          "stopped",
          "rejected",
          "suspended",
          "calculated"
        ],
        "example": "filled",
        "type": "string"
      },
      "TradeActivity": {
        "properties": {
          "cum_qty": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "0.9723",
            "format": "decimal",
            "type": "string"
          },
          "leaves_qty": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "0.5123",
            "format": "decimal",
            "type": "string"
          },
          "order_id": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "fe060a1b-5b45-4eba-ba46-c3a3345d8255",
            "format": "uuid",
            "type": "string"
          },
          "order_status": {
            "$ref": "#/components/schemas/OrderStatus"
          },
          "price": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "3.1415",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "0.38921",
            "format": "decimal",
            "type": "string"
          },
          "side": {
            "$ref": "#/components/schemas/OrderSide"
          },
          "symbol": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "AAPL",
            "type": "string"
          },
          "transaction_time": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "example": "2021-05-10T14:01:04.650275Z",
            "format": "date-time",
            "type": "string"
          },
          "type": {
            "description": "Valid only for trading activity types. Null for non-trading activites.",
            "enum": [
              "fill",
              "partial_fill"
            ],
            "example": "fill",
            "type": "string"
          }
        },
        "title": "TradeActivity",
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
    "/v1/accounts/activities": {
      "get": {
        "description": "Returns a list of activities\n\nNotes:\n* Pagination is handled using the `page_token` and `page_size` parameters.\n* `page_token` represents the ID of the last item on your current page of results.\n   For example, if the ID of the last activity in your first response is `20220203000000000::045b3b8d-c566-4bef-b741-2bf598dd6ae7`, you would pass that value as `page_token` to retrieve the next page of results.\n\n* If specified with a `direction` of `desc`, for example, the results will end before the activity with the specified ID.\n* If specified with a `direction` of `asc`, results will begin with the activity immediately after the one specified.\n* `page_size` is the maximum number of entries to return in the response.\n* If `date` is not specified, the default and maximum value is 100.\n* If `date` is specified, the default behavior is to return all results, and there is no maximum page size.",
        "operationId": "getAccountActivities",
        "parameters": [
          {
            "description": "id of a single account to filter by",
            "in": "query",
            "name": "account_id",
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "A comma-separated list of activity types used to filter the results.",
            "explode": false,
            "in": "query",
            "name": "activity_types",
            "schema": {
              "items": {
                "$ref": "#/components/schemas/ActivityType"
              },
              "type": "array"
            },
            "style": "form"
          },
          {
            "description": "The activity category. Cannot be used with \"activity_types\" parameter.",
            "in": "query",
            "name": "category",
            "schema": {
              "enum": [
                "trade_activity",
                "non_trade_activity"
              ],
              "type": "string"
            }
          },
          {
            "description": "Filter activities associated with a specific order. Useful for retrieving the fills that make up a completely filled order.",
            "in": "query",
            "name": "order_id",
            "schema": {
              "example": "fe060a1b-5b45-4eba-ba46-c3a3345d8255",
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "Filter activities by their creation date (created_at), not the activity's settlement date. For non-trade activities such as fees, the creation date is typically the day after the trade date (in UTC). Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported.",
            "in": "query",
            "name": "date",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "Get activities created before this date. Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported.",
            "in": "query",
            "name": "until",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "Get activities created after this date. Both formats YYYY-MM-DD and YYYY-MM-DDTHH:MM:SSZ are supported.",
            "in": "query",
            "name": "after",
            "schema": {
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "$ref": "#/components/parameters/Direction"
          },
          {
            "description": "The maximum number of entries to return in the response.",
            "in": "query",
            "name": "page_size",
            "schema": {
              "default": 100,
              "maximum": 100,
              "minimum": 1,
              "type": "integer"
            }
          },
          {
            "description": "Token used for pagination. Provide the ID of the last activity from the last page to retrieve the next set of results.",
            "in": "query",
            "name": "page_token",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Activity"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Success"
          }
        },
        "summary": "Retrieve Account Activities",
        "tags": [
          "Accounts"
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
      "name": "Accounts"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```