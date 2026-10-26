# Subscribe to Trade Events (SSE)

Source: https://docs.alpaca.markets/us/reference/subscribetotradev2sse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Trade Events (SSE)

The Events API provides event push as well as historical queries via SSE (server sent events).

You can listen to events related to trade updates. Most market trades sent during market hours are filled instantly; you can listen to limit order updates through this endpoint.

Historical events are streamed immediately if queried, and updates are pushed as events occur.

Query Params Rules:
- `since` required if `until` specified
- `since_id` required if `until_id` specified
- `since` and `since_id` can't be used at the same time
Behavior:
- if `since` or `since_id` not specified this will not return any historic data
- if `until` or `until_id` reached stream will end (status 200)

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.

---

**Legacy trade events API deprecation**

The legacy v1 trade events endpoint has been fully deprecated and is no longer available. Use `/v2/events/trades` for all trade event integrations.

---

###  Comment messages
According to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.

#####  Slow client

The server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`

##### Internal server error

An error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`

---

**Common events**

These are the events that are the expected results of actions you may have taken by sending API requests.

The meaning of the timestamp field changes for each type; the meanings have been specified here for which types the timestamp field will be present.

- `accepted` Sent when an order is received and accepted by Alpaca
- `pending_new` Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.
- `new` Sent when an order has been routed to exchanges for execution.
- `fill` Sent when your order has been completely filled.
  - timestamp: The time at which the order was filled.
- `partial_fill` Sent when a number of shares less than the total remaining quantity on your order has been filled.
  - timestamp: The time at which the shares were filled.
- `canceled` Sent when your requested cancellation of an order is processed.
  - timestamp: The time at which the order was canceled.
- `expired` Sent when an order has reached the end of its lifespan, as determined by the order's time in force value.
  - timestamp: The time at which the order expired.
- `done_for_day` Sent when the order is done executing for the day, and will not receive further updates until the next trading day.
- `replaced` Sent when your requested replacement of an order is processed.
  - timestamp: The time at which the order was replaced.

**Rarer events**

These are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.

- `rejected` Sent when your order has been rejected.
  - timestamp: The time at which the rejection occurred.
- `held` For multi-leg orders, the secondary orders (stop loss, take profit) will enter this state while waiting to be triggered.
- `stopped` Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.
- `pending_cancel` Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.
- `pending_replace` Sent when the order is awaiting replacement.
- `calculated` Sent when the order has been completed for the day - it is either filled or done_for_day - but remaining settlement calculations are still pending.
- `suspended` Sent when the order has been suspended and is not eligible for trading.
- `order_replace_rejected` Sent when the order replace has been rejected.
- `order_cancel_rejected` Sent when the order cancel has been rejected.
- `trade_bust`: Sent when a previously reported execution has been canceled ("busted") by the upstream exchange.
- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.
- `restated`: Sent when the order is manually modified.

# OpenAPI definition

```json
{
  "components": {
    "examples": {
      "TradeUpdateEventV2MultilegOptionsFill": {
        "value": {
          "account_id": "529248ad-c4cc-4a50-bea4-6bfd2953f83a",
          "at": "2025-01-14T16:05:51.872012Z",
          "event": "fill",
          "event_id": "01G112NTT0XAXKDZK3AABK68TH",
          "legs": [
            {
              "execution_id": "ccf7d1dc-78e1-4eb5-92c6-5c86b2bcca8f",
              "order_id": "8d58279f-7dc8-415f-8495-32f394935509",
              "price": "0.04",
              "qty": "1",
              "symbol": "AAPL250117P00200000",
              "timestamp": "2025-01-14T16:05:51.867802561Z"
            },
            {
              "execution_id": "06f94555-6db7-4059-a4c4-0b993084ccd0",
              "order_id": "8b0e2cff-eace-4e6a-8810-cad42c63df59",
              "price": "0.03",
              "qty": "1",
              "symbol": "AAPL250117C00250000",
              "timestamp": "2025-01-14T16:05:51.867813051Z"
            }
          ],
          "order": {
            "asset_class": "",
            "asset_id": "00000000-0000-0000-0000-000000000000",
            "cancel_requested_at": null,
            "canceled_at": null,
            "client_order_id": "9d2f39de-adae-4dae-a67e-838bf21fb5ae",
            "created_at": "2025-01-14T16:05:51.79424769Z",
            "expired_at": null,
            "extended_hours": false,
            "failed_at": null,
            "filled_at": "2025-01-14T16:05:51.867813051Z",
            "filled_avg_price": "0.07",
            "filled_qty": "1",
            "hwm": null,
            "id": "8af45a94-0b35-4053-ad4e-716c6783fcc9",
            "legs": [
              {
                "asset_class": "us_option",
                "asset_id": "8d1ba989-d98b-4551-889f-4647c2e86e20",
                "cancel_requested_at": null,
                "canceled_at": null,
                "client_order_id": "9c5ce763-bd6f-41eb-b1b1-ed2c0b99d268",
                "created_at": "2025-01-14T16:05:51.79424769Z",
                "expired_at": null,
                "expires_at": "2025-01-14T21:00:00Z",
                "extended_hours": false,
                "failed_at": null,
                "filled_at": "2025-01-14T16:05:51.867802561Z",
                "filled_avg_price": "0.04",
                "filled_qty": "1",
                "hwm": null,
                "id": "8d58279f-7dc8-415f-8495-32f394935509",
                "legs": null,
                "limit_price": null,
                "notional": null,
                "order_class": "mleg",
                "order_type": "",
                "position_intent": "buy_to_open",
                "qty": "1",
                "ratio_qty": "1",
                "replaced_at": null,
                "replaced_by": null,
                "replaces": null,
                "side": "buy",
                "status": "filled",
                "stop_price": null,
                "submitted_at": "2025-01-14T16:05:51.800245966Z",
                "symbol": "AAPL250117P00200000",
                "time_in_force": "day",
                "trail_percent": null,
                "trail_price": null,
                "type": "",
                "updated_at": "2025-01-14T16:05:51.869810922Z"
              },
              {
                "asset_class": "us_option",
                "asset_id": "e9f8c9ba-de7c-4e51-9eef-629f4cb79049",
                "cancel_requested_at": null,
                "canceled_at": null,
                "client_order_id": "9cda9826-8fd5-4c01-8ee1-30c5286e2387",
                "created_at": "2025-01-14T16:05:51.79424769Z",
                "expired_at": null,
                "expires_at": "2025-01-14T21:00:00Z",
                "extended_hours": false,
                "failed_at": null,
                "filled_at": "2025-01-14T16:05:51.867813051Z",
                "filled_avg_price": "0.03",
                "filled_qty": "1",
                "hwm": null,
                "id": "8b0e2cff-eace-4e6a-8810-cad42c63df59",
                "legs": null,
                "limit_price": null,
                "notional": null,
                "order_class": "mleg",
                "order_type": "",
                "position_intent": "buy_to_open",
                "qty": "1",
                "ratio_qty": "1",
                "replaced_at": null,
                "replaced_by": null,
                "replaces": null,
                "side": "buy",
                "status": "filled",
                "stop_price": null,
                "submitted_at": "2025-01-14T16:05:51.802310606Z",
                "symbol": "AAPL250117C00250000",
                "time_in_force": "day",
                "trail_percent": null,
                "trail_price": null,
                "type": "",
                "updated_at": "2025-01-14T16:05:51.870879612Z"
              }
            ],
            "limit_price": "0.6",
            "notional": null,
            "order_class": "mleg",
            "order_type": "limit",
            "position_intent": "",
            "qty": "1",
            "replaced_at": null,
            "replaced_by": null,
            "replaces": null,
            "side": "buy",
            "status": "filled",
            "stop_price": null,
            "submitted_at": "2025-01-14T16:05:51.802310606Z",
            "symbol": "",
            "time_in_force": "day",
            "trail_percent": null,
            "trail_price": null,
            "type": "limit",
            "updated_at": "2025-01-14T16:05:51.870937762Z"
          },
          "position_qtys": {
            "AAPL250117C00250000": "1",
            "AAPL250117P00200000": "1"
          },
          "price": "0.07",
          "qty": "1",
          "timestamp": "2025-01-14T16:05:51.867813051Z"
        }
      },
      "TradeUpdateEventV2New": {
        "value": {
          "account_id": "529248ad-c4cc-4a50-bea4-6bfd2953f83a",
          "at": "2022-04-19T14:12:30.656741Z",
          "event": "new",
          "event_id": "01G112NTT0XAXKDZK3AABK68TH",
          "execution_id": "7e544af3-3104-4e1a-8cbc-dab2624949ff",
          "order": {
            "asset_class": "us_equity",
            "asset_id": "a4778bc8-fad1-47b7-87fe-d5cde10d43f4",
            "cancel_requested_at": null,
            "canceled_at": null,
            "client_order_id": "6d873193-dac6-4f72-8e13-c57853a9339d",
            "commission": "1",
            "created_at": "2022-04-19T10:12:30.57117938-04:00",
            "expired_at": null,
            "expires_at": "2022-04-19T21:00:00Z",
            "extended_hours": false,
            "failed_at": null,
            "filled_at": null,
            "filled_avg_price": null,
            "filled_qty": "0",
            "hwm": null,
            "id": "edada91a-8b55-4916-a153-8c7a9817e708",
            "legs": null,
            "limit_price": "700",
            "notional": null,
            "order_class": "",
            "order_type": "limit",
            "position_intent": "buy_to_open",
            "qty": "4",
            "replaced_at": null,
            "replaced_by": null,
            "replaces": null,
            "side": "buy",
            "status": "new",
            "stop_price": null,
            "submitted_at": "2022-04-19T10:12:30.403135025-04:00",
            "symbol": "TSLA",
            "time_in_force": "day",
            "trail_percent": null,
            "trail_price": null,
            "type": "limit",
            "updated_at": "2022-04-19T10:12:30.609783218-04:00"
          },
          "previous_execution_id": "aeb60660-412f-4537-8d1f-1101b3fc8f64",
          "timestamp": "2022-04-19T14:12:30.602193534Z"
        }
      }
    },
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
      "TradeUpdateEventType": {
        "description": "**Common events**\n\nThese are the events that are the expected results of actions you may have taken by sending API requests.\n\nThe meaning of the `timestamp` field changes for each type; the meanings have been specified here for which types the\ntimestamp field will be present.\n\n- `accepted`: Sent when an order is received and accepted by Alpaca.\n- `new`: Sent when an order has been routed to exchanges for execution.\n- `fill`: Sent when your order has been completely filled.\n  - `timestamp`: The time at which the order was filled.\n- `partial_fill`: Sent when a number of shares less than the total remaining quantity on your order has been filled.\n  - `timestamp`: The time at which the shares were filled.\n- `canceled`: Sent when the order transitions to the `canceled` state. This can be triggered by a user-submitted cancel request, by Alpaca as part of automated processing (e.g. corporate-action sweeps, aged-GTC expiration, overnight-session lifecycle), or by an upstream execution venue. When Alpaca populates a machine-readable cause, it is exposed on the top-level `reason` field — see the `reason` property on `TradeUpdateEventV2` for known values (e.g. `CORPORATE_ACTION`).\n  - `timestamp`: The time at which the order was canceled.\n- `expired`: Sent when an order has reached the end of its lifespan, as determined by the order's time in force value.\n  - `timestamp`: The time at which the order expired.\n- `done_for_day`: Sent when the order is done executing for the day, and will not receive further updates until the next trading day.\n- `replaced`: Sent when your requested replacement of an order is processed.\n  - `timestamp`: The time at which the order was replaced.\n\n**Rarer events**\n\nThese are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.\n\n- `rejected`: Sent when your order has been rejected.\n  - `timestamp`: The time at which the rejection occurred.\n- `pending_new`: Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.\n- `stopped`: Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.\n- `pending_cancel`: Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.\n- `pending_replace`: Sent when the order is awaiting replacement.\n- `calculated`: Sent when the order has been completed for the day - it is either `filled` or `done_for_day` - but remaining settlement calculations are still pending.\n- `suspended`: Sent when the order has been suspended and is not eligible for trading.\n- `order_replace_rejected`: Sent when the order replace has been rejected.\n- `order_cancel_rejected`: Sent when the order cancel has been rejected.\n- `trade_bust`: Sent when a previously reported execution has been canceled (\"busted\") by the upstream exchange.\n- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.\n- `restated`: Sent when the order is manually modified.\n",
        "enum": [
          "new",
          "fill",
          "partial_fill",
          "canceled",
          "expired",
          "done_for_day",
          "replaced",
          "rejected",
          "pending_new",
          "accepted",
          "stopped",
          "pending_cancel",
          "pending_replace",
          "calculated",
          "suspended",
          "order_replace_rejected",
          "order_cancel_rejected",
          "trade_bust",
          "trade_correct"
        ],
        "type": "string"
      },
      "TradeUpdateEventV2": {
        "description": "Represents an update to an order/trade, sent over the events streaming api.",
        "properties": {
          "account_id": {
            "description": "Account UUID",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "at": {
            "description": "Timestamp of event",
            "format": "date-time",
            "minLength": 1,
            "type": "string"
          },
          "event": {
            "$ref": "#/components/schemas/TradeUpdateEventType"
          },
          "event_id": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "execution_id": {
            "description": "Corresponding execution of an order. If an order gets filled over two executions (a partial_fill for example), you will receive two events with different IDs.\nNot present for `MultilegOptions`\n",
            "format": "uui",
            "type": "string"
          },
          "legs": {
            "description": "Only present when event is for `MultilegOptions`. Represents filled qty/price of legs.\n",
            "items": {
              "$ref": "#/components/schemas/TradeUpdateEventV2Leg"
            },
            "type": "array"
          },
          "order": {
            "$ref": "#/components/schemas/Order"
          },
          "position_qty": {
            "description": "Only present when event is either `fill` or `partial_fill` other than `MultilegOptions`. The size of your total position, after this fill event, in shares. Positive for long positions, negative for short positions.\n",
            "type": "string"
          },
          "position_qtys": {
            "description": "Only present when event is either `fill` or `partial_fill` for `MultilegOptions`. The size of your total position, after this fill event, in shares. Positive for long positions, negative for short positions.\n",
            "type": "string"
          },
          "previous_execution_id": {
            "description": "ID of the original execution that was busted or corrected (present only in trade_bust and trade_correct events).",
            "format": "uuid",
            "type": "string"
          },
          "price": {
            "description": "Only present when event is either `fill` or `partial_fill`. The average price per share at which the order was filled.",
            "type": "string"
          },
          "qty": {
            "description": "Only present when event is either `fill`, `partial_fill`, `trade_bust` and `trade_correct`. The amount of shares this Trade order was for. <br /> For `trade_bust` events, the qty field may be negative, representing a reversal of the original quantity.",
            "type": "string"
          },
          "reason": {
            "description": "Machine-readable code that explains **why** the event occurred. Only present when a reason applies; omitted from routine lifecycle events such as `new`, `fill`, and `partial_fill`.\n\nKnown values:\n\n| Value | Event(s) | Meaning |\n| --- | --- | --- |\n| `CORPORATE_ACTION` | `canceled` | Alpaca canceled the order internally because the underlying is scheduled for a mandatory corporate action other than a cash dividend (e.g. reverse split, symbol/CUSIP change, merger, liquidation). Emitted by the overnight-session lifecycle and, where enabled by Alpaca, the daytime GTC corporate-action sweep. Not emitted when the cancel is routed to the upstream venue instead (e.g. day-session, `extended_hours=false`, agency- or mixed-capacity orders); those `canceled` events carry the venue's own text in `reason` if any. |\n| `TOO_LATE_TO_CANCEL` | `order_cancel_rejected`, `order_replace_rejected` | The cancel or replace request arrived after the order had already reached a terminal state (typically `filled`). |\n| `TRADE_BUST` | `trade_bust` | Alpaca operations replayed or synthesized a bust of a previously reported execution. Busts that originate from the upstream venue surface the venue's own text in `reason` (or omit it entirely), so consumers should not rely on `TRADE_BUST` alone to identify all busts — key on the `event` field (`trade_bust`) for that. |\n\nFree-form strings may also appear in `reason`. In particular, `canceled`, `trade_bust`, and `trade_correct` events originating from the upstream venue carry the venue's own text field (when the venue provides one) rather than an Alpaca-defined code. Consumers should tolerate unknown values and, where they need to distinguish cases, key on `event` first and use `reason` as a secondary hint.\n",
            "example": "CORPORATE_ACTION",
            "type": [
              "string",
              "null"
            ]
          },
          "settle_date": {
            "description": "Settlement date of the trade in format `YYYY-MM-DD` for `fill` and `partial_fill` events",
            "example": "2026-03-03",
            "format": "date",
            "type": "string"
          },
          "swap_rate": {
            "description": "Only present for `local currency trading account` or `crypto asset trade` when event is either `fill` or `partial_fill`. The swap rate at which the current trade was filled.",
            "type": "string"
          },
          "timestamp": {
            "description": "Has various different meanings depending on the value of `event`, please see the [Trading Events](https://alpaca.markets/docs/api-references/broker-api/events/#trade-events)\nEnum in the documentation or the TradeUpdateEventType model for more details on when it means different things.\n",
            "format": "date-time",
            "type": "string"
          }
        },
        "title": "TradeUpdateEvent",
        "type": "object"
      },
      "TradeUpdateEventV2Leg": {
        "description": "Represents filled qty/price of legs.",
        "properties": {
          "execution_id": {
            "description": "Corresponding execution of an order. If an order gets filled over two executions (a partial_fill for example), you will receive two events with different IDs.",
            "format": "uuid",
            "type": "string"
          },
          "order_id": {
            "description": "Order UUID",
            "format": "uuid",
            "minLength": 1,
            "type": "string"
          },
          "price": {
            "description": "The average price per share for this event.",
            "type": "string"
          },
          "qty": {
            "description": "The amount of shares filled for this event",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol of an asset",
            "type": "string"
          },
          "timestamp": {
            "description": "Timestamp of this event leg\n",
            "format": "date-time",
            "type": "string"
          }
        },
        "title": "TradeUpdateEventV2Leg",
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
    "/v2/events/trades": {
      "get": {
        "description": "The Events API provides event push as well as historical queries via SSE (server sent events).\n\nYou can listen to events related to trade updates. Most market trades sent during market hours are filled instantly; you can listen to limit order updates through this endpoint.\n\nHistorical events are streamed immediately if queried, and updates are pushed as events occur.\n\nQuery Params Rules:\n- `since` required if `until` specified\n- `since_id` required if `until_id` specified\n- `since` and `since_id` can't be used at the same time\nBehavior:\n- if `since` or `since_id` not specified this will not return any historic data\n- if `until` or `until_id` reached stream will end (status 200)\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n\n---\n\n**Legacy trade events API deprecation**\n\nThe legacy v1 trade events endpoint has been fully deprecated and is no longer available. Use `/v2/events/trades` for all trade event integrations.\n\n---\n\n###  Comment messages\nAccording to the SSE specification, any line that starts with a colon is a comment which does not contain data.  It is typically a free text that does not follow any data schema. A few examples mentioned below for comment messages.\n\n#####  Slow client\n\nThe server sends a comment when the client is not consuming messages fast enough. Example: `: you are reading too slowly, dropped 10000 messages`\n\n##### Internal server error\n\nAn error message is sent as a comment when the server closes the connection on an internal server error (only sent by the v2 and v2beta1 endpoints). Example: `: internal server error`\n\n---\n\n**Common events**\n\nThese are the events that are the expected results of actions you may have taken by sending API requests.\n\nThe meaning of the timestamp field changes for each type; the meanings have been specified here for which types the timestamp field will be present.\n\n- `accepted` Sent when an order is received and accepted by Alpaca\n- `pending_new` Sent when the order has been received by Alpaca and routed to the exchanges, but has not yet been accepted for execution.\n- `new` Sent when an order has been routed to exchanges for execution.\n- `fill` Sent when your order has been completely filled.\n  - timestamp: The time at which the order was filled.\n- `partial_fill` Sent when a number of shares less than the total remaining quantity on your order has been filled.\n  - timestamp: The time at which the shares were filled.\n- `canceled` Sent when your requested cancellation of an order is processed.\n  - timestamp: The time at which the order was canceled.\n- `expired` Sent when an order has reached the end of its lifespan, as determined by the order's time in force value.\n  - timestamp: The time at which the order expired.\n- `done_for_day` Sent when the order is done executing for the day, and will not receive further updates until the next trading day.\n- `replaced` Sent when your requested replacement of an order is processed.\n  - timestamp: The time at which the order was replaced.\n\n**Rarer events**\n\nThese are events that may rarely be sent due to unexpected circumstances on the exchanges. It is unlikely you will need to design your code around them, but you may still wish to account for the possibility that they will occur.\n\n- `rejected` Sent when your order has been rejected.\n  - timestamp: The time at which the rejection occurred.\n- `held` For multi-leg orders, the secondary orders (stop loss, take profit) will enter this state while waiting to be triggered.\n- `stopped` Sent when your order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, but has not yet occurred.\n- `pending_cancel` Sent when the order is awaiting cancellation. Most cancellations will occur without the order entering this state.\n- `pending_replace` Sent when the order is awaiting replacement.\n- `calculated` Sent when the order has been completed for the day - it is either filled or done_for_day - but remaining settlement calculations are still pending.\n- `suspended` Sent when the order has been suspended and is not eligible for trading.\n- `order_replace_rejected` Sent when the order replace has been rejected.\n- `order_cancel_rejected` Sent when the order cancel has been rejected.\n- `trade_bust`: Sent when a previously reported execution has been canceled (\"busted\") by the upstream exchange.\n- `trade_correct`: Sent when a previously reported trade has been corrected. For example, the exchange may have updated the price, quantity, or another execution parameter after the trade was initially reported.\n- `restated`: Sent when the order is manually modified.",
        "operationId": "subscribeToTradeV2SSE",
        "parameters": [
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "since",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "until",
            "schema": {
              "format": "date",
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
                "examples": {
                  "MultilegOptions-fill": {
                    "$ref": "#/components/examples/TradeUpdateEventV2MultilegOptionsFill"
                  },
                  "new": {
                    "$ref": "#/components/examples/TradeUpdateEventV2New"
                  }
                },
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/TradeUpdateEventV2"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to Trade Events (SSE)",
        "tags": [
          "Events",
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
    },
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