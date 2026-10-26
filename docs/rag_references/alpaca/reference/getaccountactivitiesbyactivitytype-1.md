# Retrieve Account Activities of Specific Type

Source: https://docs.alpaca.markets/us/reference/getaccountactivitiesbyactivitytype-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Account Activities of Specific Type

Returns account activity entries for a specific type of activity.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "ActivitySubType": {
        "description": "Represents a more specific classification to the `activity_type`.\nThis field is optional and may not always be populated, depending on the activity type and the available data.\nEach `activity_type` has a set of valid `activity_sub_type` values.\n\nFull mapping of `activity_type` to `activity_sub_type`:\n\n- **CGD**: Capital Gains Distribution activity sub-types:\n  - **LTCG**: Long-Term Capital Gain\n  - **STCG**: Short-Term Capital Gain\n\n- **DIV**: Dividend activity sub-types:\n  - **CDIV**: Cash Dividend\n  - **ROC**: Return of Capital\n  - **SDIV**: Stock Dividend\n  - **SPD**: Substitute Payment In Lieu Of Dividend\n\n- **FEE**: Fee-related activity sub-types:\n  - **REG**: Regulatory Fee\n  - **TAF**: Trading Activity Fee\n  - **LCT**: Local Currency Trading Fee\n  - **ORF**: Options Regulatory Fee\n  - **OCC**: Options Clearing Corporation Fee\n  - **NRC**: Non-Retail Commission Fee\n  - **NRV**: Non-Retail Venue Fee\n  - **COM**: Commission\n  - **CAT**: Consolidated Audit Trail Fee\n\n- **INT**: Interest-related activity sub-types:\n  - **MGN**: Margin Interest\n  - **CDT**: Credit Interest\n  - **SWP**: Sweep Interest\n  - **QII**: Qualified Interest\n  - **FI**: Fixed Income Interest (coupon or accrued)\n\n- **MA**: Merger and Acquisition activity sub-types:\n  - **CMA**: Cash Merger\n  - **SMA**: Stock Merger\n  - **SCMA**: Stock & Cash Merger\n\n- **NC**: Name Change activity sub types\n  - **SNC**: Symbol Name Change\n  - **CNC**: CUSIP Name Change\n  - **SCNC**: Symbol & CUSIP Name Change\n\n- **OPCA**: Option Corporate Action activity sub-types:\n  - **DIV.CDIV**: Cash Dividend\n  - **DIV.ROC**: Return of Capital\n  - **DIV.SDIV**: Stock Dividend\n  - **MA.CMA**: Cash Merger\n  - **MA.SMA**: Stock Merger\n  - **MA.SCMA**: Stock & Cash Merger\n  - **NC.CNC**: CUSIP Name Change\n  - **NC.SNC**: Symbol Name Change\n  - **NC.SCNC**: Symbol & CUSIP Name Change\n  - **SPIN**: Spin-off\n  - **SPLIT.FSPLIT**: Forward Stock Split\n  - **SPLIT.RSPLIT**: Reverse Stock Split\n  - **SPLIT.USPLIT**: Unit Split\n\n- **REO**: Reorganization activity sub-types\n  - **REOS**: Stock only (1 or more stock legs)\n  - **REOC**: Cash only (1 cash leg)\n  - **REOSC**: Stock and cash\n\n- **REORG**: Activity sub-types:\n  - **WRM**: Worthless Removal\n\n- **SPLIT**: Stock Split activity sub-types:\n  - **FSPLIT**: Forward Stock Split\n  - **RSPLIT**: Reverse Stock Split\n  - **USPLIT**: Unit Split\n\n- **VOF**: Voluntary Offering activity sub-types:\n  - **VTND**: Tender Offer\n  - **VWRT**: Warrant Exercise\n  - **VRGT**: Rights Offer\n  - **VEXH**: Exchange Offer\n\n- **WH**: Withholding activity sub-types:\n  - **SWH**: State Withholding\n  - **FWH**: Federal Withholding\n  - **SLWH**: Sales Withholding",
        "title": "ActivitySubType",
        "type": "string"
      },
      "ActivityType": {
        "description": "- FILL\n  Order fills (both partial and full fills)\n\n- TRANS\n  Cash transactions (both CSD and CSW)\n\n- MISC\n  Miscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)\n\n- ACATC\n  ACATS IN/OUT (Cash)\n\n- ACATS\n  ACATS IN/OUT (Securities)\n\n- CFEE\n  Crypto fee\n\n- CGD\n  Capital gains distribution\n\n- CSD\n  Cash deposit(+)\n\n- CSW\n  Cash withdrawal(-)\n\n- DIV\n  Dividends\n\n- DIVCGL\n  Dividend (capital gains long term)\n\n- DIVCGS\n  Dividend (capital gains short term)\n\n- DIVFEE\n  Dividend fee\n\n- DIVFT\n  Dividend adjusted (Foreign Tax Withheld)\n\n- DIVNRA\n  Dividend adjusted (NRA Withheld)\n\n- DIVROC\n  Dividend return of capital\n\n- DIVTW\n  Dividend adjusted (Tefra Withheld)\n\n- DIVTXEX\n  Dividend (tax exempt)\n\n- FEE\n  Fee denominated in USD\n\n- INT\n  Interest (credit/margin)\n\n- INTNRA\n  Interest adjusted (NRA Withheld)\n\n- INTTW\n  Interest adjusted (Tefra Withheld)\n\n- JNL\n  Journal entry\n\n- JNLC\n  Journal entry (cash)\n\n- JNLS\n  Journal entry (stock)\n\n- MA\n  Merger/Acquisition\n\n- NC\n  Name change\n\n- OPASN\n  Option assignment\n\n- OPCA\n  Option corporate action\n\n- OPCSH\n  Option cash deliverable for non-standard contracts\n\n- OPEXC\n  Option exercise\n\n- OPEXP\n  Option expiration\n\n- OPTRD\n  Option trade\n\n- PTC\n  Pass Thru Charge\n\n- PTR\n  Pass Thru Rebate\n\n- REO\n  Reorganization\n\n- REORG\n  Worthless removal CA\n\n- SPIN\n  Stock spinoff\n\n- SPLIT\n  Stock split\n\n- FOPT\n  Free of Payment Transfers\n\n- OCT\n  On chain transactions (blockchain deposits/withdrawals)",
        "enum": [
          "FILL",
          "TRANS",
          "MISC",
          "ACATC",
          "ACATS",
          "CFEE",
          "CGD",
          "CSD",
          "CSW",
          "DIV",
          "DIVCGL",
          "DIVCGS",
          "DIVFEE",
          "DIVFT",
          "DIVNRA",
          "DIVROC",
          "DIVTW",
          "DIVTXEX",
          "FEE",
          "INT",
          "INTNRA",
          "INTTW",
          "JNL",
          "JNLC",
          "JNLS",
          "MA",
          "NC",
          "OPASN",
          "OPCA",
          "OPCSH",
          "OPEXC",
          "OPEXP",
          "OPTRD",
          "PTC",
          "PTR",
          "REO",
          "REORG",
          "SPIN",
          "SPLIT",
          "FOPT",
          "OCT"
        ],
        "examples": [
          "FILL"
        ],
        "title": "ActivityType",
        "type": "string"
      },
      "NonTradeActivities": {
        "examples": [
          {
            "activity_sub_type": "SDIV",
            "activity_type": "DIV",
            "created_at": "2021-05-10T14:01:04.650275Z",
            "currency": "USD",
            "date": "2019-08-01",
            "id": "20190801011955195::5f596936-6f23-4cef-bdf1-3806aae57dbf",
            "net_amount": "1.02",
            "per_share_amount": "0.51",
            "qty": "2",
            "status": "executed",
            "symbol": "T"
          }
        ],
        "properties": {
          "activity_sub_type": {
            "$ref": "#/components/schemas/ActivitySubType"
          },
          "activity_type": {
            "$ref": "#/components/schemas/ActivityType"
          },
          "created_at": {
            "description": "Valid only for non-trading activity types. Null for trading activites.",
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "Currency denomination of the activity (e.g. USD). Included in NTA stream events and activity responses.",
            "example": "USD",
            "type": "string"
          },
          "cusip": {
            "description": "The CUSIP of the security involved with the activity. Not present for all activity types.",
            "type": "string"
          },
          "date": {
            "description": "The date on which the activity occurred or on which the transaction associated with the activity settled.",
            "format": "date-time",
            "type": "string"
          },
          "group_id": {
            "description": "ID used to link activities who share a sibling relationship.",
            "type": "string"
          },
          "id": {
            "description": "An ID for the activity, always in \"::\" format. Can be sent as page_token in requests to facilitate the paging of results.",
            "type": "string"
          },
          "net_amount": {
            "description": "The net amount of money (positive or negative) associated with the activity.",
            "type": "string"
          },
          "per_share_amount": {
            "description": "For dividend activities, the average amount paid per share. Not present for other activity types.",
            "type": "string"
          },
          "qty": {
            "description": "For dividend activities, the number of shares that contributed to the payment. Not present for other activity types.\n",
            "type": "string"
          },
          "status": {
            "description": "The activity status.",
            "enum": [
              "executed",
              "correct",
              "canceled"
            ],
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the security involved with the activity. Not present for all activity types.",
            "type": "string"
          }
        },
        "title": "AccountNonTradeActivities",
        "type": "object"
      },
      "OrderStatus": {
        "description": "An order executed through Alpaca can experience several status changes during its lifecycle. The most common statuses are described in detail below:\n\n- new\n  The order has been received by Alpaca, and routed to exchanges for execution. This is the usual initial state of an order.\n\n- partially_filled\n  The order has been partially filled.\n\n- filled\n  The order has been filled, and no further updates will occur for the order.\n\n- done_for_day\n  The order is done executing for the day, and will not receive further updates until the next trading day.\n\n- canceled\n  The order has been canceled, and no further updates will occur for the order. This can be either due to a cancel request by the user, or the order has been canceled by the exchanges due to its time-in-force.\n\n- expired\n  The order has expired, and no further updates will occur for the order.\n\n- replaced\n  The order was replaced by another order, or was updated due to a market event such as corporate action.\n\n- pending_cancel\n  The order is waiting to be canceled.\n\n- pending_replace\n  The order is waiting to be replaced by another order. The order will reject cancel request while in this state.\n\nLess common states are described below. Note that these states only occur on very rare occasions, and most users will likely never see their orders reach these states:\n\n- accepted\n  The order has been received by Alpaca, but hasn't yet been routed to the execution venue. This could be seen often out side of trading session hours.\n\n- pending_new\n  The order has been received by Alpaca, and routed to the exchanges, but has not yet been accepted for execution. This state only occurs on rare occasions.\n\n- accepted_for_bidding\n  The order has been received by exchanges, and is evaluated for pricing. This state only occurs on rare occasions.\n\n- stopped\n  The order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred. This state only occurs on rare occasions.\n\n- rejected\n  The order has been rejected, and no further updates will occur for the order. This state occurs on rare occasions and may occur based on various conditions decided by the exchanges.\n\n- suspended\n  The order has been suspended, and is not eligible for trading. This state only occurs on rare occasions.\n\n- calculated\n  The order has been completed for the day (either filled or done for day), but remaining settlement calculations are still pending. This state only occurs on rare occasions.\n\n\nAn order may be canceled through the API up until the point it reaches a state of either filled, canceled, or expired.",
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
          "calculated",
          "held"
        ],
        "example": "new",
        "title": "OrderStatus",
        "type": "string"
      },
      "TradingActivities": {
        "examples": [
          {
            "activity_type": "FILL",
            "cum_qty": "2",
            "id": "20220202135509981::2d7be4ff-d1f3-43e9-856a-0f5cf5c5088e",
            "leaves_qty": "0",
            "order_id": "b5abe576-6a8a-49f3-a353-46b72c1ccae9",
            "order_status": "filled",
            "price": "174.78",
            "qty": "2",
            "side": "buy",
            "symbol": "AAPL",
            "transaction_time": "2022-02-02T18:55:09.981482Z",
            "type": "fill"
          }
        ],
        "properties": {
          "activity_type": {
            "$ref": "#/components/schemas/ActivityType"
          },
          "cum_qty": {
            "description": "The cumulative quantity of shares involved in the execution.",
            "type": "string"
          },
          "id": {
            "description": "An id for the activity. Always in \"::\" format. Can be sent as page_token in requests to facilitate the paging of results.",
            "type": "string"
          },
          "leaves_qty": {
            "description": "For partially_filled orders, the quantity of shares that are left to be filled.\n",
            "type": "string"
          },
          "order_id": {
            "description": "The id for the order that filled.",
            "format": "uuid",
            "type": "string"
          },
          "order_status": {
            "$ref": "#/components/schemas/OrderStatus"
          },
          "price": {
            "description": "The per-share price that the trade was executed at.",
            "type": "string"
          },
          "qty": {
            "description": "The number of shares involved in the trade execution.",
            "type": "string"
          },
          "side": {
            "description": "buy or sell",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the security being traded.",
            "example": "AAPL",
            "type": "string"
          },
          "transaction_time": {
            "description": "The time at which the execution occurred.",
            "format": "date-time",
            "type": "string"
          },
          "type": {
            "description": "fill or partial_fill",
            "enum": [
              "fill",
              "partial_fill"
            ],
            "example": "fill",
            "type": "string"
          }
        },
        "title": "AccountTradingActivities",
        "type": "object"
      }
    },
    "securitySchemes": {
      "API_Key": {
        "description": "",
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "API_Secret": {
        "description": "",
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
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Trading API",
    "version": "2.0.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v2/account/activities/{activity_type}": {
      "get": {
        "description": "Returns account activity entries for a specific type of activity.",
        "operationId": "getAccountActivitiesByActivityType",
        "parameters": [
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
            "description": "The chronological order of response based on the activity datetime.",
            "in": "query",
            "name": "direction",
            "schema": {
              "default": "desc",
              "enum": [
                "asc",
                "desc"
              ],
              "example": "desc",
              "type": "string"
            }
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
                    "description": "Will be one of a TradingActivity or NonTradeActivity based on activity_type used in path",
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/TradingActivities"
                      },
                      {
                        "$ref": "#/components/schemas/NonTradeActivities"
                      }
                    ]
                  },
                  "type": "array"
                }
              }
            },
            "description": "returns an array of Account activities"
          }
        },
        "summary": "Retrieve Account Activities of Specific Type",
        "tags": [
          "Account Activities"
        ]
      },
      "parameters": [
        {
          "description": "The activity type you want to view entries for. A list of valid activity types can be found at the bottom of this page.",
          "in": "path",
          "name": "activity_type",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ]
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "servers": [
    {
      "description": "Paper",
      "url": "https://paper-api.alpaca.markets"
    },
    {
      "description": "Live",
      "url": "https://api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Account Activities"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```