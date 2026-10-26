# Replace an Order

Source: https://docs.alpaca.markets/us/reference/replaceorderforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Replace an Order

Replaces a single order with updated parameters. Each parameter overrides the corresponding attribute of the existing order. The other attributes remain the same as the existing order.

A success return code from a replaced order does NOT guarantee the existing open order has been replaced. If the existing open order is filled before the replacing (new) order reaches the execution venue, the replacing (new) order is rejected, and these events are sent in the trade_updates stream channel found [here](https://docs.alpaca.markets/reference/subscribetotradev2sse).

While an order is being replaced, the account's buying power is reduced by the larger of the two orders that have been placed (the old order being replaced, and the newly placed order to replace it). If you are replacing a buy entry order with a higher limit price than the original order, the buying power is calculated based on the newly placed order. If you are replacing it with a lower limit price, the buying power is calculated based on the old order.

Note: Order cannot be replaced when the status is `accepted`, `pending_new`, `pending_cancel` or `pending_replace`.

Note: Notional orders for non-IPO asset classes cannot be replaced. Any attempt to modify a non-IPO notional order via this endpoint will be rejected; cancel it and submit a new one instead.

Note: IPO indications of interest (`asset_class: "ipo"`) **are** notional and **can** be replaced via this endpoint by providing a new `notional` value. `qty` and `notional` are mutually exclusive on a single replace request.

Note that submitting DMA orders (using `advanced_instructions` with `algorithm: DMA`) is only available for partners/correspondents who have been enabled for DMA.

# OpenAPI definition

```json
{
  "components": {
    "examples": {
      "EquityOrderResponse": {
        "value": {
          "asset_class": "us_equity",
          "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
          "canceled_at": null,
          "client_order_id": "5680c4bc-9ac1-4a12-a44c-df427ba53032",
          "created_at": "2023-12-12T22:31:24.668464435Z",
          "expired_at": null,
          "extended_hours": false,
          "failed_at": null,
          "filled_at": null,
          "filled_avg_price": null,
          "filled_qty": "0",
          "hwm": null,
          "id": "7b08df51-c1ac-453c-99f9-323a5f075f0d",
          "legs": null,
          "limit_price": "150",
          "notional": null,
          "order_class": "",
          "order_type": "limit",
          "qty": "2",
          "replaced_at": null,
          "replaced_by": null,
          "replaces": null,
          "side": "buy",
          "source": null,
          "status": "accepted",
          "stop_price": null,
          "submitted_at": "2023-12-12T22:31:24.577215743Z",
          "subtag": null,
          "symbol": "AAPL",
          "time_in_force": "gtc",
          "trail_percent": null,
          "trail_price": null,
          "type": "limit",
          "updated_at": "2023-12-12T22:31:24.668464435Z"
        }
      },
      "IPOOrderResponse": {
        "value": {
          "asset_class": "ipo",
          "asset_id": "9b6c7c1a-9eb2-4d4a-8a3a-1bf4c1d5cbaa",
          "canceled_at": null,
          "client_order_id": "0b3a90b6-6b5c-4d83-8c0e-9b3eaf4a8d11",
          "created_at": "2025-09-15T13:30:42.117344821Z",
          "expired_at": null,
          "extended_hours": false,
          "failed_at": null,
          "filled_at": null,
          "filled_avg_price": null,
          "filled_qty": "0",
          "hwm": null,
          "id": "5e2a8f1a-9c10-4d3a-8c64-7f59c1d18c11",
          "legs": null,
          "limit_price": null,
          "notional": "500",
          "order_class": "",
          "order_type": "market",
          "qty": null,
          "replaced_at": null,
          "replaced_by": null,
          "replaces": null,
          "side": "buy",
          "source": null,
          "status": "accepted",
          "stop_price": null,
          "submitted_at": "2025-09-15T13:30:42.094518219Z",
          "subtag": null,
          "symbol": "FI111225",
          "time_in_force": "gtc",
          "trail_percent": null,
          "trail_price": null,
          "type": "market",
          "updated_at": "2025-09-15T13:30:42.117344821Z"
        }
      },
      "OptionOrderResponse": {
        "value": {
          "asset_class": "us_option",
          "asset_id": "98359ef7-5124-49f3-85ea-5cf02df6defa",
          "canceled_at": null,
          "client_order_id": "58cd43a7-029e-457e-b77f-cd4f61f00f2a",
          "created_at": "2023-12-12T21:35:49.102449524Z",
          "expired_at": null,
          "extended_hours": false,
          "failed_at": null,
          "filled_at": null,
          "filled_avg_price": null,
          "filled_qty": "0",
          "hwm": null,
          "id": "30a077fa-96f6-4f20-a052-4b921ee2f243",
          "legs": null,
          "limit_price": "10",
          "notional": null,
          "order_class": "simple",
          "order_type": "limit",
          "qty": "2",
          "replaced_at": null,
          "replaced_by": null,
          "replaces": null,
          "side": "buy",
          "source": null,
          "status": "pending_new",
          "stop_price": null,
          "submitted_at": "2023-12-12T21:35:49.056332248Z",
          "subtag": null,
          "symbol": "AAPL250620C00100000",
          "time_in_force": "day",
          "trail_percent": null,
          "trail_price": null,
          "type": "limit",
          "updated_at": "2023-12-12T21:35:49.102504673Z"
        }
      }
    },
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
      },
      "OrderID": {
        "description": "Order identifier.",
        "in": "path",
        "name": "order_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
    "responses": {
      "BadRequest": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "Malformed input."
      },
      "NotFound": {
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Error"
            }
          }
        },
        "description": "Resource does not exist."
      }
    },
    "schemas": {
      "AdvancedInstructions": {
        "description": "Advanced instructions for Direct Market Access (DMA) routing. When `algorithm` is `DMA`,\nthe order is routed directly to the exchange specified in `destination`. Note that this feature is only\navailable to partners/correspondents who have been enabled for DMA.",
        "examples": [
          {
            "algorithm": "DMA",
            "destination": "IEX",
            "display_qty": "100"
          }
        ],
        "properties": {
          "algorithm": {
            "description": "The advanced routing algorithm to use for the order. Only `DMA` (Direct Market Access) is supported.",
            "enum": [
              "DMA"
            ],
            "example": "DMA",
            "type": "string"
          },
          "destination": {
            "description": "Target exchange for order execution. Required when `algorithm` is `DMA`.",
            "enum": [
              "IEX",
              "MEMX"
            ],
            "example": "IEX",
            "type": "string"
          },
          "display_qty": {
            "description": "Maximum shares displayed on the exchange at any time. Must be in round lot increments.",
            "example": "100",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "AdvancedInstructions",
        "type": "object"
      },
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
      },
      "UpdateOrderRequest": {
        "description": "Represents the fields that are editable in an order replace/update call.\n\nNote: client_order_id is currently not editable on its own, one of the other fields must be changed at the same time to effectively replace the order.\n\nNote: `qty` and `notional` are mutually exclusive on a single replace request. `notional` is only valid for IPO indications of interest (`asset_class: \"ipo\"`); non-IPO notional orders cannot be replaced at all.",
        "properties": {
          "advanced_instructions": {
            "$ref": "#/components/schemas/AdvancedInstructions"
          },
          "client_order_id": {
            "description": "A unique identifier for the new order. Automatically generated if not sent. (<= 128 characters)",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "maxLength": 128,
            "type": "string"
          },
          "limit_price": {
            "description": "Required if original order's `type` field was `limit` or `stop_limit`.\nIn case of `mleg`, the limit_price parameter is expressed with the following notation:\n- A positive value indicates a debit, representing a cost or payment to be made.\n- A negative value signifies a credit, reflecting an amount to be received.",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "notional": {
            "description": "New notional (dollar amount) for the order. Only valid for IPO indications of interest (`asset_class: \"ipo\"`); will be rejected for any other asset class.\nMutually exclusive with `qty` on the same replace request.",
            "example": "750",
            "format": "decimal",
            "type": "string"
          },
          "qty": {
            "description": "You can only patch full shares for now.\n\nQty of equity fractional orders are not allowed to change. Non-IPO notional orders cannot be replaced at all - no fields (qty, limit_price, stop_price, etc.) can be modified; cancel and resubmit instead.\nIn case of multi-leg orders represents the number of units to trade of this strategy.",
            "example": "4",
            "format": "decimal",
            "type": "string"
          },
          "stop_price": {
            "description": "Required if original order's `type` field was stop or stop_limit",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "time_in_force": {
            "$ref": "#/components/schemas/TimeInForce"
          },
          "trail": {
            "description": "The new value of the trail_price or trail_percent",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          }
        },
        "title": "OrderUpdateRequest",
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
    "/v1/trading/accounts/{account_id}/orders/{order_id}": {
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        },
        {
          "$ref": "#/components/parameters/OrderID"
        }
      ],
      "patch": {
        "description": "Replaces a single order with updated parameters. Each parameter overrides the corresponding attribute of the existing order. The other attributes remain the same as the existing order.\n\nA success return code from a replaced order does NOT guarantee the existing open order has been replaced. If the existing open order is filled before the replacing (new) order reaches the execution venue, the replacing (new) order is rejected, and these events are sent in the trade_updates stream channel found [here](https://docs.alpaca.markets/reference/subscribetotradev2sse).\n\nWhile an order is being replaced, the account's buying power is reduced by the larger of the two orders that have been placed (the old order being replaced, and the newly placed order to replace it). If you are replacing a buy entry order with a higher limit price than the original order, the buying power is calculated based on the newly placed order. If you are replacing it with a lower limit price, the buying power is calculated based on the old order.\n\nNote: Order cannot be replaced when the status is `accepted`, `pending_new`, `pending_cancel` or `pending_replace`.\n\nNote: Notional orders for non-IPO asset classes cannot be replaced. Any attempt to modify a non-IPO notional order via this endpoint will be rejected; cancel it and submit a new one instead.\n\nNote: IPO indications of interest (`asset_class: \"ipo\"`) **are** notional and **can** be replaced via this endpoint by providing a new `notional` value. `qty` and `notional` are mutually exclusive on a single replace request.\n\nNote that submitting DMA orders (using `advanced_instructions` with `algorithm: DMA`) is only available for partners/correspondents who have been enabled for DMA.",
        "operationId": "replaceOrderForAccount",
        "requestBody": {
          "content": {
            "application/json": {
              "examples": {
                "Equity": {
                  "summary": "Increase qty and limit price on an equity order",
                  "value": {
                    "limit_price": "155",
                    "qty": "4",
                    "time_in_force": "gtc"
                  }
                },
                "IPO": {
                  "summary": "Update notional on an IPO indication of interest",
                  "value": {
                    "notional": "750"
                  }
                },
                "Options": {
                  "summary": "Adjust an option order's limit price",
                  "value": {
                    "limit_price": "11.25",
                    "time_in_force": "day"
                  }
                }
              },
              "schema": {
                "$ref": "#/components/schemas/UpdateOrderRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "Equity": {
                    "$ref": "#/components/examples/EquityOrderResponse"
                  },
                  "IPO": {
                    "$ref": "#/components/examples/IPOOrderResponse"
                  },
                  "Options": {
                    "$ref": "#/components/examples/OptionOrderResponse"
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              }
            },
            "description": "A new Order object with a new order_id"
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "403": {
            "description": "Buying power or shares are not sufficient"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          }
        },
        "summary": "Replace an Order",
        "tags": [
          "Trading"
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
      "name": "Trading"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```