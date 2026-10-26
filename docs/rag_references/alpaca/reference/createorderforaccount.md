# Create an Order for an Account

Source: https://docs.alpaca.markets/us/reference/createorderforaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create an Order for an Account

Creating an order for your end customer. Each trading request must pass in the account_id in the URL.

- Note that when submitting crypto orders, `market`, `limit` and `stop_limit` orders are supported while the supported `time_in_force` values are `gtc`, and `ioc`.
- For equities and crypto we accept fractional orders as well with either `notional` or `qty` provided.
- Note that submitting an options order is only available for partners who have been enabled for Options BETA.
- In case of Fixed Income, only `market` and `limit` order types with `day` `time_in_force` are supported, and order replacement is not supported.
Note that submitting Fixed Income orders is only available for partners who have been enabled for Fixed Income.
- Note that submitting DMA orders (using `advanced_instructions` with `algorithm: DMA`) is only available for partners/correspondents who have been enabled for DMA.
- For IPO indications of interest (`asset_class: "ipo"`), the `symbol` is the offering reference returned by [`GET /v1/ipos`](#operation/listIPOOfferings) (e.g. `FI111225`). IPO orders are notional-only (`notional` required, `qty` must be omitted), buy-side, `market` type, and `gtc` time_in_force. Indications of interest can be replaced or canceled while the offering is open via [`PATCH /v1/trading/accounts/{account_id}/orders/{order_id}`](#operation/replaceOrderForAccount) and [`DELETE /v1/trading/accounts/{account_id}/orders/{order_id}`](#operation/deleteOrderForAccount).

# OpenAPI definition

```json
{
  "components": {
    "examples": {
      "CryptoOrderResponse": {
        "value": {
          "asset_class": "crypto",
          "asset_id": "a1733398-6acc-4e92-af24-0d0667f78713",
          "canceled_at": null,
          "client_order_id": "5b5d3d67-06ad-4ffa-af65-a117d0fc5a59",
          "created_at": "2023-12-12T22:36:51.337711497Z",
          "expired_at": null,
          "extended_hours": false,
          "failed_at": null,
          "filled_at": null,
          "filled_avg_price": null,
          "filled_qty": "0",
          "hwm": null,
          "id": "38e482f3-79a8-4f75-a057-f07a1ec6a397",
          "legs": null,
          "limit_price": "2100",
          "notional": null,
          "order_class": "",
          "order_type": "limit",
          "qty": "0.02",
          "replaced_at": null,
          "replaced_by": null,
          "replaces": null,
          "side": "buy",
          "source": null,
          "status": "pending_new",
          "stop_price": null,
          "submitted_at": "2023-12-12T22:36:51.313261061Z",
          "subtag": null,
          "symbol": "ETH/USD",
          "time_in_force": "gtc",
          "trail_percent": null,
          "trail_price": null,
          "type": "limit",
          "updated_at": "2023-12-12T22:36:51.337754768Z"
        }
      },
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
      "MultilegOptionsOrderResponse": {
        "value": {
          "asset_class": "",
          "asset_id": "",
          "canceled_at": null,
          "client_order_id": "646b1fe6-b212-4f54-94c6-429e7bcdee04",
          "created_at": "2024-12-10T16:15:53.677230742Z",
          "expired_at": null,
          "extended_hours": false,
          "failed_at": null,
          "filled_at": "2024-12-10T16:15:53.694Z",
          "filled_avg_price": "1.28",
          "filled_qty": "1",
          "hwm": null,
          "id": "83f37e9f-6b1f-49ed-8fc6-3e6af716323f",
          "legs": [
            {
              "asset_class": "us_option",
              "asset_id": "f0ea14b2-8a49-4e9b-89d1-894c6e518a76",
              "canceled_at": null,
              "client_order_id": "cc8cc104-fe43-476c-b25c-f62650fb73f9",
              "created_at": "2024-12-10T16:15:53.677230742Z",
              "expired_at": null,
              "expires_at": "2024-12-10T21:00:00Z",
              "extended_hours": false,
              "failed_at": null,
              "filled_at": "2024-12-10T16:15:53.694Z",
              "filled_avg_price": "0.43",
              "filled_qty": "3",
              "hwm": null,
              "id": "df4ff24a-c58a-4e37-8b9f-ef32b83a11f2",
              "legs": null,
              "limit_price": null,
              "notional": null,
              "order_class": "mleg",
              "order_type": "",
              "position_intent": "buy_to_open",
              "qty": "3",
              "ratio_qty": "3",
              "replaced_at": null,
              "replaced_by": null,
              "replaces": null,
              "side": "buy",
              "source": null,
              "status": "filled",
              "stop_price": null,
              "submitted_at": "2024-12-10T16:15:53.684952901Z",
              "subtag": null,
              "symbol": "AAPL241213C00250000",
              "time_in_force": "day",
              "trail_percent": null,
              "trail_price": null,
              "type": "",
              "updated_at": "2024-12-10T16:15:53.725091158Z"
            },
            {
              "asset_class": "us_option",
              "asset_id": "f89940db-eeb1-46e6-8f9b-bb1f27a0b395",
              "canceled_at": null,
              "client_order_id": "0bd2d36d-4af2-4dfb-8418-333a5d5026fa",
              "created_at": "2024-12-10T16:15:53.677230742Z",
              "expired_at": null,
              "expires_at": "2024-12-10T21:00:00Z",
              "extended_hours": false,
              "failed_at": null,
              "filled_at": "2024-12-10T16:15:53.694Z",
              "filled_avg_price": "0.01",
              "filled_qty": "1",
              "hwm": null,
              "id": "ecd91110-c34d-4e9d-a7bf-a9c27c40f8b5",
              "legs": null,
              "limit_price": null,
              "notional": null,
              "order_class": "mleg",
              "order_type": "",
              "position_intent": "sell_to_open",
              "qty": "1",
              "ratio_qty": "1",
              "replaced_at": null,
              "replaced_by": null,
              "replaces": null,
              "side": "sell",
              "source": null,
              "status": "filled",
              "stop_price": null,
              "submitted_at": "2024-12-10T16:15:53.684952901Z",
              "subtag": null,
              "symbol": "AAPL241213C00260000",
              "time_in_force": "day",
              "trail_percent": null,
              "trail_price": null,
              "type": "",
              "updated_at": "2024-12-10T16:15:53.708983759Z"
            }
          ],
          "limit_price": "10",
          "notional": null,
          "order_class": "mleg",
          "order_type": "limit",
          "qty": "1",
          "replaced_at": null,
          "replaced_by": null,
          "replaces": null,
          "side": "",
          "source": null,
          "status": "filled",
          "stop_price": null,
          "submitted_at": "2024-12-10T16:15:53.684952901Z",
          "subtag": null,
          "symbol": "",
          "time_in_force": "day",
          "trail_percent": null,
          "trail_price": null,
          "type": "limit",
          "updated_at": "2024-12-10T16:15:53.725139688Z"
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
      "Forbidden": {
        "content": {
          "application/json": {
            "schema": {
              "type": "string"
            }
          }
        },
        "description": "Request is forbidden"
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
      "CreateOrderRequest": {
        "properties": {
          "advanced_instructions": {
            "$ref": "#/components/schemas/AdvancedInstructions"
          },
          "client_order_id": {
            "description": "A unique identifier for the order. Automatically generated if not sent. (<= 128 characters)",
            "example": "eb9e2aaa-f71a-4f51-b5b4-52a6c565dad4",
            "maxLength": 128,
            "type": "string"
          },
          "commission": {
            "description": "The commission you want to collect from the user.",
            "example": "1.0",
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
          "extended_hours": {
            "description": "Defaults to false. If true, order will be eligible for execution in the pre-market, after-hours, and overnight sessions. Only works with type `limit` and time_in_force set to either `day` or `gtc`.",
            "example": false,
            "type": "boolean"
          },
          "instructions": {
            "type": "string"
          },
          "legs": {
            "description": "list of order legs (<= 4)",
            "items": {
              "$ref": "#/components/schemas/MLegOrderLeg"
            },
            "maxItems": 4,
            "type": "array"
          },
          "limit_price": {
            "description": "Required if type is `limit` or `stop_limit`.\n- In case of `mleg`, the limit_price parameter is expressed with the following notation:\n  - A positive value indicates a debit, representing a cost or payment to be made.\n  - A negative value signifies a credit, reflecting an amount to be received.\n- In case of Fied Income, the price is expressed in percentage of par value (face value).\nPrice is always clean price, meaning it does not include accrued interest.",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "notional": {
            "description": "Dollar amount to trade. Cannot work with qty. Only market and limit orders supported with time_in_force = day; Only limit orders for extended hours.",
            "example": "3",
            "format": "decimal",
            "type": "string"
          },
          "order_class": {
            "$ref": "#/components/schemas/OrderClass"
          },
          "position_intent": {
            "$ref": "#/components/schemas/PositionIntent"
          },
          "qty": {
            "description": "- For equities, the number of shares to trade. Can be fractionable for only market and day order types.\n- Required for `mleg` order class, represents the number of units to trade of this strategy.\n- For Fixed Income securities, qty represents the order size in par value (face value).\nFor example, to place an order for 1 bond with a face value of $1,000, provide a qty of 1000.\n",
            "example": "4.124",
            "format": "decimal",
            "type": "string"
          },
          "side": {
            "$ref": "#/components/schemas/OrderSide"
          },
          "source": {
            "type": "string"
          },
          "stop_loss": {
            "description": "Takes in a string/number values for stop_price and limit_price",
            "properties": {
              "limit_price": {
                "example": "3.14",
                "format": "decimal",
                "type": "string"
              },
              "stop_price": {
                "example": "3.14",
                "format": "decimal",
                "type": "string"
              }
            },
            "type": "object"
          },
          "stop_price": {
            "description": "Required if type is stop or stop_limit",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "subtag": {
            "type": "string"
          },
          "swap_fee_bps": {
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol or asset ID to identify the asset to trade. Required for all order classes except for `mleg`.",
            "example": "AAPL",
            "type": "string"
          },
          "take_profit": {
            "description": "Takes in a string/number value for limit_price",
            "properties": {
              "limit_price": {
                "example": "3.14",
                "format": "decimal",
                "type": "string"
              }
            },
            "type": "object"
          },
          "time_in_force": {
            "$ref": "#/components/schemas/TimeInForce"
          },
          "trail_percent": {
            "description": "If type is trailing_stop, then one of trail_price or trail_percent is required",
            "example": "5.0",
            "format": "decimal",
            "type": "string"
          },
          "trail_price": {
            "description": "If type is trailing_stop, then one of trail_price or trail_percent is required",
            "example": "3.14",
            "format": "decimal",
            "type": "string"
          },
          "type": {
            "$ref": "#/components/schemas/OrderType"
          }
        },
        "required": [
          "type",
          "time_in_force"
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
      "MLegOrderLeg": {
        "description": "Represents an individual leg of a multileg options order.",
        "properties": {
          "position_intent": {
            "$ref": "#/components/schemas/PositionIntent"
          },
          "ratio_qty": {
            "description": "proportional quantity of this leg in relation to the overall multileg order qty",
            "example": "1",
            "type": "string"
          },
          "side": {
            "$ref": "#/components/schemas/OrderSide"
          },
          "symbol": {
            "description": "symbol or asset ID to identify the asset to trade",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "ratio_qty"
        ],
        "title": "MLegOrderLeg",
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
    "/v1/trading/accounts/{account_id}/orders": {
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        }
      ],
      "post": {
        "description": "Creating an order for your end customer. Each trading request must pass in the account_id in the URL.\n\n- Note that when submitting crypto orders, `market`, `limit` and `stop_limit` orders are supported while the supported `time_in_force` values are `gtc`, and `ioc`.\n- For equities and crypto we accept fractional orders as well with either `notional` or `qty` provided.\n- Note that submitting an options order is only available for partners who have been enabled for Options BETA.\n- In case of Fixed Income, only `market` and `limit` order types with `day` `time_in_force` are supported, and order replacement is not supported.\nNote that submitting Fixed Income orders is only available for partners who have been enabled for Fixed Income.\n- Note that submitting DMA orders (using `advanced_instructions` with `algorithm: DMA`) is only available for partners/correspondents who have been enabled for DMA.\n- For IPO indications of interest (`asset_class: \"ipo\"`), the `symbol` is the offering reference returned by [`GET /v1/ipos`](#operation/listIPOOfferings) (e.g. `FI111225`). IPO orders are notional-only (`notional` required, `qty` must be omitted), buy-side, `market` type, and `gtc` time_in_force. Indications of interest can be replaced or canceled while the offering is open via [`PATCH /v1/trading/accounts/{account_id}/orders/{order_id}`](#operation/replaceOrderForAccount) and [`DELETE /v1/trading/accounts/{account_id}/orders/{order_id}`](#operation/deleteOrderForAccount).",
        "operationId": "createOrderForAccount",
        "requestBody": {
          "content": {
            "application/json": {
              "examples": {
                "Crypto": {
                  "summary": "Buy a crypto coin",
                  "value": {
                    "limit_price": "2100",
                    "qty": "0.02",
                    "side": "buy",
                    "symbol": "ETH/USD",
                    "time_in_force": "gtc",
                    "type": "limit"
                  }
                },
                "Equity": {
                  "summary": "Buy an equity stock",
                  "value": {
                    "limit_price": "150",
                    "qty": "2",
                    "side": "buy",
                    "symbol": "AAPL",
                    "time_in_force": "gtc",
                    "type": "limit"
                  }
                },
                "FixedIncome": {
                  "summary": "Buy a US Treasury Bill",
                  "value": {
                    "limit_price": "99.15",
                    "qty": "5000",
                    "side": "buy",
                    "symbol": "US912797QN08",
                    "time_in_force": "day",
                    "type": "limit"
                  }
                },
                "IPO": {
                  "summary": "Submit an IPO indication of interest",
                  "value": {
                    "notional": "500",
                    "side": "buy",
                    "symbol": "FI111225",
                    "time_in_force": "gtc",
                    "type": "market"
                  }
                },
                "Options": {
                  "summary": "Buy an option contract (BETA)",
                  "value": {
                    "limit_price": "10",
                    "qty": "2",
                    "side": "buy",
                    "symbol": "AAPL250620C00100000",
                    "time_in_force": "day",
                    "type": "limit"
                  }
                }
              },
              "schema": {
                "$ref": "#/components/schemas/CreateOrderRequest"
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
                  "Crypto": {
                    "$ref": "#/components/examples/CryptoOrderResponse"
                  },
                  "Equity": {
                    "$ref": "#/components/examples/EquityOrderResponse"
                  },
                  "IPO": {
                    "$ref": "#/components/examples/IPOOrderResponse"
                  },
                  "MultilegOptions": {
                    "$ref": "#/components/examples/MultilegOptionsOrderResponse"
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
            "description": "OK"
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "422": {
            "description": "Some parameters are not valid"
          }
        },
        "summary": "Create an Order for an Account",
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