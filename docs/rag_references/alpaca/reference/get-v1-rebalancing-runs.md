# List All Runs.

Source: https://docs.alpaca.markets/us/reference/get-v1-rebalancing-runs.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List All Runs.

Lists runs.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AssetClass": {
        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, \"crypto\" for cryptocurrencies, and \"ipo\" for IPO indications of interest. This `asset_class: ipo` value is distinct from the assets API `attributes: [\"ipo\"]` flag.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto",
          "ipo"
        ],
        "type": "string"
      },
      "CommissionType": {
        "default": "notional",
        "description": "An enum to select how to interpret the value provided in the commission field.\n\n- notional:\nCharge commission on a per order basis. (When the `commission_type` field is omitted from the order request, this is used as the default).\n\n- qty:\nCharge commission on a per qty/contract basis, pro rated.\n\n- bps:\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\nCommission value in bps can have up to two decimal places.",
        "enum": [
          "notional",
          "qty",
          "bps"
        ],
        "example": "qty",
        "title": "CommissionType",
        "type": "string"
      },
      "NextPageToken": {
        "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
        "example": "MTAwMA==",
        "type": [
          "string",
          "null"
        ]
      },
      "Order": {
        "properties": {
          "asset_class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "asset_id": {
            "description": "The asset ID (For options this represents the option contract ID)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "cancel_requested_at": {
            "description": "Time when cancellation or bust was requested (if applicable)",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "canceled_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "client_order_id": {
            "description": "Client unique order ID",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "maxLength": 128,
            "type": "string"
          },
          "commission": {
            "description": "The dollar value commission for this order.",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "commission_bps": {
            "deprecated": true,
            "description": "**deprecated**: Please use the commission_type = bps instead and set the desired bps value in the `commission` field.\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\n",
            "example": "10",
            "format": "decimal",
            "type": "string"
          },
          "commission_type": {
            "$ref": "#/components/schemas/CommissionType"
          },
          "created_at": {
            "description": "Time when order was entered",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "expired_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "extended_hours": {
            "example": true,
            "type": "boolean"
          },
          "failed_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_at": {
            "description": "Time the order was filled. Can be null if not filled",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_avg_price": {
            "description": "Filled average price. Can be 0 until order is processed in case order is passed outside of market hours",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_qty": {
            "description": "Filled quantity",
            "example": "4.2",
            "format": "decimal",
            "type": "string"
          },
          "hwm": {
            "description": "The highest (lowest) market price seen since the trailing stop order was submitted.",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "id": {
            "description": "Order ID generated by Alpaca",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "legs": {
            "description": "When querying non-simple order_class orders in a nested style, an array of Order entities associated with this order. Otherwise, null.",
            "items": {
              "$ref": "#/components/schemas/OrderLeg"
            },
            "type": [
              "array",
              "null"
            ]
          },
          "limit_price": {
            "description": "Limit price",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "notional": {
            "description": "Ordered notional amount. If entered, qty will be null. Can take up to 2 decimal points.",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "order_class": {
            "$ref": "#/components/schemas/OrderClass"
          },
          "order_type": {
            "$ref": "#/components/schemas/OrderType"
          },
          "position_intent": {
            "$ref": "#/components/schemas/PositionIntent"
          },
          "qty": {
            "description": "Ordered quantity. If entered, notional will be null. Can take up to 2 decimal points.",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "replaced_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "replaced_by": {
            "description": "The order ID that this order was replaced by. (Can be null)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "replaces": {
            "description": "The order ID that this order replaces. (Can be null)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "side": {
            "$ref": "#/components/schemas/OrderSide"
          },
          "status": {
            "$ref": "#/components/schemas/OrderStatus"
          },
          "stop_price": {
            "description": "Stop price",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "submitted_at": {
            "description": "Time the order was submitted for execution or, if not yet submitted the created_at time. Because orders are submitted for execution asynchronous to database updates, at times this may be after the created_at time.",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "swap_fee_bps": {
            "description": "Fee in basis points on top swap rate charged by the correspondent on every order",
            "type": "string"
          },
          "swap_rate": {
            "description": "Swap rate is the exchange rate (without mark-up) used to convert the price into local currency or crypto asset",
            "type": "string"
          },
          "symbol": {
            "description": "The asset symbol",
            "example": "AALP",
            "type": "string"
          },
          "time_in_force": {
            "$ref": "#/components/schemas/TimeInForce"
          },
          "trail_percent": {
            "description": "The percent value away from the high water mark for trailing stop orders.",
            "example": "5.0",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "trail_price": {
            "description": "The dollar value away from the high water mark for trailing stop orders.",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "$ref": "#/components/schemas/OrderType"
          },
          "updated_at": {
            "description": "Time of most recent change to the order",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "usd": {
            "description": "Nested object to encompass the USD equivalent fields for the local currency fields",
            "type": "object"
          }
        },
        "required": [
          "id",
          "symbol"
        ],
        "type": "object"
      },
      "OrderClass": {
        "description": "The order classes supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order classes for each category:\n  - Equity trading: simple (or \"\"), oco, oto, bracket.\n  - Options trading:\n    - simple (or \"\")\n    - mleg (required for multi-leg complex option strategies)\n  - Crypto trading: simple (or \"\").",
        "enum": [
          "simple",
          "bracket",
          "oco",
          "oto",
          "mleg",
          ""
        ],
        "example": "",
        "type": "string"
      },
      "OrderLeg": {
        "properties": {
          "asset_class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "asset_id": {
            "description": "The asset ID (For options this represents the option contract ID)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "canceled_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "client_order_id": {
            "description": "Client unique order ID",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "maxLength": 128,
            "type": "string"
          },
          "commission": {
            "description": "The dollar value commission you want to charge the end user.",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "commission_bps": {
            "deprecated": true,
            "description": "**deprecated**: Please use the commission_type = bps instead and set the desired bps value in the `commission` field.\nThe percent commission you want to charge the end user on the order (expressed in bps). Alpaca will convert the order to a notional amount for purposes of calculating commission.\n",
            "example": "10",
            "format": "decimal",
            "type": "string"
          },
          "commission_type": {
            "$ref": "#/components/schemas/CommissionType"
          },
          "created_at": {
            "description": "Time when order was entered",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "expired_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "extended_hours": {
            "example": true,
            "type": "boolean"
          },
          "failed_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_at": {
            "description": "Time the order was filled. Can be null if not filled",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_avg_price": {
            "description": "Filled average price. Can be 0 until order is processed in case order is passed outside of market hours",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "filled_qty": {
            "description": "Filled quantity",
            "example": "4.2",
            "format": "decimal",
            "type": "string"
          },
          "hwm": {
            "description": "The highest (lowest) market price seen since the trailing stop order was submitted.",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "id": {
            "description": "Order ID generated by Alpaca",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "legs": {
            "description": "Always null for an order leg; legs are not nested beyond one level. An empty array is accepted for generated-client compatibility.",
            "example": null,
            "items": {
              "type": "object"
            },
            "maxItems": 0,
            "type": [
              "array",
              "null"
            ]
          },
          "limit_price": {
            "description": "Limit price",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "notional": {
            "description": "Ordered notional amount. If entered, qty will be null. Can take up to 2 decimal points.",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "order_class": {
            "$ref": "#/components/schemas/OrderClass"
          },
          "order_type": {
            "$ref": "#/components/schemas/OrderType"
          },
          "position_intent": {
            "$ref": "#/components/schemas/PositionIntent"
          },
          "qty": {
            "description": "Ordered quantity. If entered, notional will be null. Can take up to 2 decimal points.",
            "example": "4.2",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "replaced_at": {
            "description": "Can be null",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "replaced_by": {
            "description": "The order ID that this order was replaced by. (Can be null)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "replaces": {
            "description": "The order ID that this order replaces. (Can be null)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "side": {
            "$ref": "#/components/schemas/OrderSide"
          },
          "status": {
            "$ref": "#/components/schemas/OrderStatus"
          },
          "stop_price": {
            "description": "Stop price",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "submitted_at": {
            "description": "Time the order was submitted for execution or, if not yet submitted the created_at time. Because orders are submitted for execution asynchronous to database updates, at times this may be after the created_at time.",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "swap_fee_bps": {
            "description": "Fee in basis points on top swap rate charged by the correspondent on every order",
            "type": "string"
          },
          "swap_rate": {
            "description": "Swap rate is the exchange rate (without mark-up) used to convert the price into local currency or crypto asset",
            "type": "string"
          },
          "symbol": {
            "description": "The asset symbol",
            "example": "AALP",
            "type": "string"
          },
          "time_in_force": {
            "$ref": "#/components/schemas/TimeInForce"
          },
          "trail_percent": {
            "description": "The percent value away from the high water mark for trailing stop orders.",
            "example": "5.0",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "trail_price": {
            "description": "The dollar value away from the high water mark for trailing stop orders.",
            "example": "3.14",
            "format": "decimal",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "$ref": "#/components/schemas/OrderType"
          },
          "updated_at": {
            "description": "Time of most recent change to the order",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "usd": {
            "description": "Nested object to encompass the USD equivalent fields for the local currency fields",
            "type": "object"
          }
        },
        "required": [
          "id",
          "symbol"
        ],
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
      "OrderType": {
        "description": "The order types supported by Alpaca vary based on the order's security type. The following provides a comprehensive breakdown of the supported order types for each category:\n - Equity trading: market, limit, stop, stop_limit, trailing_stop.\n - Options trading: market, limit, stop, stop_limit.\n - Options Multileg trading: market, limit.\n - Crypto trading: market, limit, stop_limit.",
        "enum": [
          "market",
          "limit",
          "stop",
          "stop_limit",
          "trailing_stop"
        ],
        "example": "market",
        "title": "OrderType",
        "type": "string"
      },
      "PortfolioRun": {
        "properties": {
          "account_id": {
            "description": "Account ID for given run",
            "type": "string"
          },
          "canceled_at": {
            "description": "RFC3339 format",
            "type": "string"
          },
          "completed_at": {
            "description": "RFC3339 format",
            "type": "string"
          },
          "failed_orders": {
            "description": "Array of failed orders for this run",
            "items": {
              "$ref": "#/components/schemas/Order"
            },
            "type": "array"
          },
          "id": {
            "description": "Run ID",
            "type": "string"
          },
          "initiated_from": {
            "description": "system or api",
            "enum": [
              "system",
              "api"
            ],
            "type": "string"
          },
          "orders": {
            "description": "Array of executed orders for this run",
            "items": {
              "$ref": "#/components/schemas/Order"
            },
            "type": "array"
          },
          "portfolio_id": {
            "description": "Portfolio ID for given run",
            "type": "string"
          },
          "reason": {
            "description": "Explainer text in case of failed runs",
            "type": "string"
          },
          "skipped_orders": {
            "description": "Array of skipped order for this run",
            "items": {
              "$ref": "#/components/schemas/SkippedOrder"
            },
            "type": "array"
          },
          "status": {
            "$ref": "#/components/schemas/PortfolioRunStatus"
          },
          "type": {
            "description": "full_rebalance or invest_cash",
            "enum": [
              "full_rebalance",
              "invest_cash"
            ],
            "type": "string"
          },
          "updated_at": {
            "description": "RFC3339 format",
            "type": "string"
          },
          "weights": {
            "description": "Considered weighting for this run",
            "items": {
              "$ref": "#/components/schemas/PortfolioWeights"
            },
            "type": "array"
          }
        },
        "title": "PortfolioRun",
        "type": "object"
      },
      "PortfolioRunStatus": {
        "description": "|       Status       | Final |                                 Represented State                                |                                                         Notes                                                        |\n|:------------------:|:-----:|:--------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------:|\n| QUEUED             | No    | The run has been queued, waiting for our system to process it.                   | Runs only executed when the US market is open and there's at least 15 minutes before the market closes.              |\n| IN_PROGRESS        | No    | Portfolio adjustment is in progress.                                             |                                                                                                                      |\n| CANCELED           | Yes   | Portfolio run canceled, before being picked up by Alpaca's background processing |                                                                                                                      |\n| CANCELED_MID_RUN   | Yes   | Portfolio run canceled while executing.                                          | The portfolio's state is in between the pre-run and post-run state, manual remediation or job re-run is recommended. |\n| ERROR              | Yes   | There was an error while rebalancing the portfolio.                              | The portfolio's state is in between the pre-run and post-run state, manual remediation or job re-run is recommended. |\n| TIMEOUT            | Yes   | A timeout occurred while rebalancing the portfolio.                               | The portfolio's state is in between the pre-run and post-run state, manual remediation or job re-run is recommended. |\n| COMPLETED_ADJUSTED | Yes   | The portfolio has been adjusted                                                  | The adjustments have been prepared, but the run details haven't yet updated with the list of resulting orders        |\n| COMPLETED_SUCCESS  | Yes   | The portfolio has been adjusted, run status updated                              |                                                                                                                      |",
        "enum": [
          "QUEUED",
          "IN_PROGRESS",
          "CANCELED",
          "CANCELED_MID_RUN",
          "ERROR",
          "TIMEOUT",
          "COMPLETED_ADJUSTED",
          "COMPLETED_SUCCESS"
        ],
        "title": "PortfolioRunStatus",
        "type": "string"
      },
      "PortfolioWeights": {
        "properties": {
          "percent": {
            "description": "Percentage allocated to this weight as a decimal string.",
            "type": "string"
          },
          "symbol": {
            "description": "Asset symbol. `null` for cash weights. Always present.",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "description": "Type of weight entry in a portfolio.",
            "enum": [
              "cash",
              "asset"
            ],
            "type": "string"
          }
        },
        "required": [
          "type",
          "symbol",
          "percent"
        ],
        "title": "PortfolioWeights",
        "type": "object"
      },
      "PositionIntent": {
        "description": "Represents the desired position strategy.",
        "enum": [
          "buy_to_open",
          "buy_to_close",
          "sell_to_open",
          "sell_to_close"
        ],
        "example": "buy_to_open",
        "title": "PositionIntent",
        "type": "string"
      },
      "SkippedOrder": {
        "description": "Skipped orders model contains information for such orders that the rebalancing engine didn't send to our order system due to some validation issues.",
        "properties": {
          "currency": {
            "description": "Currency of the order",
            "type": "string"
          },
          "notional": {
            "description": "Notional value of the order",
            "type": "string"
          },
          "reason": {
            "description": "Reason for the order being skipped",
            "type": "string"
          },
          "reason_details": {
            "description": "Formatted error message with the cause of the skip",
            "type": "string"
          },
          "side": {
            "description": "Side of the order (buy, sell, sell_short)",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol for which the adjustment was skipped",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "reason",
          "reason_details"
        ],
        "title": "SkippedOrder",
        "type": "object"
      },
      "TimeInForce": {
        "description": "The Time-In-Force values supported by Alpaca vary based on the order's security type. Here is a breakdown of the supported TIFs for each specific security type:\n- Equity trading: day, gtc, opg, cls, ioc, fok.\n- Options trading: day, gtc.\n- Crypto trading: gtc, ioc.\n\nBelow are the descriptions of each TIF:\n- day:\n  A day order is eligible for execution only on the day it is live. By default, the order is only valid during Regular Trading Hours (9:30am - 4:00pm ET). If unfilled after the closing auction, it is automatically canceled. If submitted after the close, it is queued and submitted the following trading day. However, if marked as eligible for extended hours, the order can also execute during supported extended hours.\n\n- gtc:\n  The order is good until canceled. Non-marketable GTC limit orders are subject to price adjustments to offset corporate actions affecting the issue. We do not currently support Do Not Reduce (DNR) orders to opt out of such price adjustments.\n\n- opg:\n  Use this TIF with a market/limit order type to submit \"market on open\" (MOO) and \"limit on open\" (LOO) orders. This order is eligible to execute only in the market opening auction. Any unfilled orders after the open will be cancelled. OPG orders submitted after 9:28am but before 7:00pm ET will be rejected. OPG orders submitted after 7:00pm will be queued and routed to the following day's opening auction. On open/on close orders are routed to the primary exchange. Such orders do not necessarily execute exactly at 9:30am / 4:00pm ET but execute per the exchange's auction rules.\n\n- cls:\n  Use this TIF with a market/limit order type to submit \"market on close\" (MOC) and \"limit on close\" (LOC) orders. This order is eligible to execute only in the market closing auction. Any unfilled orders after the close will be cancelled. CLS orders submitted after 3:50pm but before 7:00pm ET will be rejected. CLS orders submitted after 7:00pm will be queued and routed to the following day's closing auction.\n\n- ioc:\n  An Immediate Or Cancel (IOC) order requires all or part of the order to be executed immediately. Any unfilled portion of the order is canceled. Most market makers who receive IOC orders will attempt to fill the order on a principal basis only, and cancel any unfilled balance. On occasion, this can result in the entire order being cancelled if the market maker does not have any existing inventory of the security in question.\n\n- fok:\n  A Fill or Kill (FOK) order is only executed if the entire order quantity can be filled, otherwise the order is canceled.",
        "enum": [
          "day",
          "gtc",
          "opg",
          "cls",
          "ioc",
          "fok"
        ],
        "example": "gtc",
        "title": "TimeInForce",
        "type": "string"
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
    "/v1/rebalancing/runs": {
      "get": {
        "description": "Lists runs.",
        "operationId": "get-v1-rebalancing-runs",
        "parameters": [
          {
            "description": "Any runs for this account_id will be returned",
            "in": "query",
            "name": "account_id",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Status of portfolio run to filter by",
            "in": "query",
            "name": "status",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Type of portfolio run (full_rebalance, invest_cash)",
            "in": "query",
            "name": "type",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Pagination token",
            "in": "query",
            "name": "page_token",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Max number of runs to return per page",
            "in": "query",
            "name": "limit",
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
                  "properties": {
                    "next_page_token": {
                      "$ref": "#/components/schemas/NextPageToken"
                    },
                    "runs": {
                      "example": [
                        {
                          "account_id": "4db36989-6565-4011-9126-39fe6b3d9bf6",
                          "id": "0f9e8a7b-1c2d-4e3f-9a0b-1c2d3e4f5a6b",
                          "initiated_from": "api",
                          "portfolio_id": "9b2c1d4e-8f7a-4c3b-9d2e-1f0a8b7c6d5e",
                          "status": "COMPLETED_SUCCESS",
                          "type": "full_rebalance",
                          "updated_at": "2025-01-15T16:30:00Z"
                        }
                      ],
                      "items": {
                        "$ref": "#/components/schemas/PortfolioRun"
                      },
                      "type": "array"
                    }
                  },
                  "required": [
                    "runs",
                    "next_page_token"
                  ],
                  "type": "object"
                }
              }
            },
            "description": "The runs which match the query"
          }
        },
        "summary": "List All Runs.",
        "tags": [
          "Rebalancing"
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
      "name": "Rebalancing"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```