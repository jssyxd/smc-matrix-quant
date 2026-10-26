# Latest trade (single symbol)

Source: https://docs.alpaca.markets/us/reference/stocklatesttradesingle-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest trade (single symbol)

The latest trade endpoint provides the latest trade for the given ticker symbol.

Trades with any conditions that causes them to not update the bar price are excluded. For example a trade with condition `I` (odd lot) will never appear on this endpoint. You can find the complete list of excluded conditions in [this FAQ](https://docs.alpaca.markets/docs/market-data-faq#how-are-bars-aggregated).

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
      "stock_currency": {
        "description": "The currency of all prices in ISO 4217 format. Default: USD.\n",
        "in": "query",
        "name": "currency",
        "schema": {
          "type": "string"
        }
      },
      "stock_latest_feed": {
        "description": "The source feed of the data.\n\n - `sip`: all US exchanges\n - `iex`: Investors EXchange\n - `delayed_sip`: SIP with a 15 minute delay\n - `boats`: Blue Ocean, overnight US trading data\n - `overnight`: derived overnight US trading data\n - `otc`: over-the-counter exchanges\n\nDefault: `sip` if the user has the unlimited subscription, otherwise `iex`.\n",
        "in": "query",
        "name": "feed",
        "schema": {
          "$ref": "#/components/schemas/stock_latest_feed"
        }
      },
      "stock_symbol": {
        "description": "The symbol to query.",
        "example": "AAPL",
        "in": "path",
        "name": "symbol",
        "required": true,
        "schema": {
          "type": "string"
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
      "stock_latest_feed": {
        "enum": [
          "delayed_sip",
          "iex",
          "otc",
          "sip",
          "boats",
          "overnight"
        ],
        "type": "string"
      },
      "stock_latest_trades_resp_single": {
        "properties": {
          "currency": {
            "type": "string"
          },
          "symbol": {
            "type": "string"
          },
          "trade": {
            "$ref": "#/components/schemas/stock_trade"
          }
        },
        "required": [
          "trade",
          "symbol"
        ],
        "type": "object"
      },
      "stock_tape": {
        "description": "- A: New York Stock Exchange\n- B: NYSE Arca, Bats, IEX and other regional exchanges\n- C: NASDAQ\n- N: Overnight\n- O: OTC\n",
        "enum": [
          "A",
          "B",
          "C",
          "N",
          "O"
        ],
        "type": "string"
      },
      "stock_trade": {
        "description": "A stock trade.",
        "examples": [
          {
            "c": [
              "@",
              "T"
            ],
            "i": 1,
            "p": 178.26,
            "s": 246,
            "t": "2022-01-03T09:00:00.086175744Z",
            "x": "P",
            "z": "C"
          }
        ],
        "properties": {
          "c": {
            "description": "Condition flags. See `v2/stocks/meta/conditions/trade` for more details.",
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "i": {
            "description": "Trade ID sent by the exchange.",
            "format": "uint64",
            "type": "integer"
          },
          "p": {
            "description": "Trade price.",
            "format": "double",
            "type": "number"
          },
          "s": {
            "description": "Trade size.",
            "format": "uint32",
            "type": "integer"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          },
          "u": {
            "description": "Update to the trade. This field is optional, if it's missing, the trade is valid. Otherwise, it can have these values:\n - canceled: indicates that the trade has been canceled\n - incorrect: indicates that the trade has been corrected and the given trade is no longer valid\n - corrected: indicates that this trade is the correction of a previous (incorrect) trade\n",
            "type": "string"
          },
          "x": {
            "description": "Exchange code. See `v2/stocks/meta/exchanges` for more details.",
            "type": "string"
          },
          "z": {
            "$ref": "#/components/schemas/stock_tape"
          }
        },
        "required": [
          "t",
          "i",
          "x",
          "p",
          "s",
          "c",
          "z"
        ],
        "type": "object"
      },
      "timestamp": {
        "description": "Timestamp in RFC-3339 format with nanosecond precision.",
        "format": "date-time",
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
    "/v2/stocks/{symbol}/trades/latest": {
      "get": {
        "description": "The latest trade endpoint provides the latest trade for the given ticker symbol.\n\nTrades with any conditions that causes them to not update the bar price are excluded. For example a trade with condition `I` (odd lot) will never appear on this endpoint. You can find the complete list of excluded conditions in [this FAQ](https://docs.alpaca.markets/docs/market-data-faq#how-are-bars-aggregated).",
        "operationId": "StockLatestTradeSingle",
        "parameters": [
          {
            "$ref": "#/components/parameters/stock_symbol"
          },
          {
            "$ref": "#/components/parameters/stock_latest_feed"
          },
          {
            "$ref": "#/components/parameters/stock_currency"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "trade": {
                    "value": {
                      "symbol": "AAPL",
                      "trade": {
                        "c": [
                          "@",
                          "T"
                        ],
                        "i": 689,
                        "p": 172.6,
                        "s": 100,
                        "t": "2022-08-17T09:53:16.845580544Z",
                        "x": "P",
                        "z": "C"
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/stock_latest_trades_resp_single"
                }
              }
            },
            "description": "OK",
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
        "summary": "Latest trade (single symbol)",
        "tags": [
          "Stock"
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
      "description": "Endpoints for stocks.",
      "name": "Stock"
    }
  ]
}
```