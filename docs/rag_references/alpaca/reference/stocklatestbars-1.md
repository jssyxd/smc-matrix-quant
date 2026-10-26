# Latest bars

Source: https://docs.alpaca.markets/us/reference/stocklatestbars-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest bars

The latest bars endpoint provides the latest minute bar for the given ticker symbols.


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
      "stock_symbols": {
        "description": "A comma-separated list of stock symbols.",
        "example": "AAPL,TSLA",
        "in": "query",
        "name": "symbols",
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
      "stock_bar": {
        "description": "OHLC aggregate of all the trades in a given interval.\n",
        "examples": [
          {
            "c": 178.08,
            "h": 178.34,
            "l": 177.76,
            "n": 1727,
            "o": 178.26,
            "t": "2022-01-03T09:00:00Z",
            "v": 60937,
            "vw": 177.954244
          }
        ],
        "properties": {
          "c": {
            "description": "Closing price.",
            "format": "double",
            "type": "number"
          },
          "h": {
            "description": "High price.",
            "format": "double",
            "type": "number"
          },
          "l": {
            "description": "Low price.",
            "format": "double",
            "type": "number"
          },
          "n": {
            "description": "Trade count in the bar.",
            "format": "int64",
            "type": "integer"
          },
          "o": {
            "description": "Opening price.",
            "format": "double",
            "type": "number"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          },
          "v": {
            "description": "Bar volume.",
            "format": "int64",
            "type": "integer"
          },
          "vw": {
            "description": "Volume weighted average price.",
            "format": "double",
            "type": "number"
          }
        },
        "required": [
          "t",
          "o",
          "h",
          "l",
          "c",
          "v",
          "n",
          "vw"
        ],
        "type": "object"
      },
      "stock_latest_bars_resp": {
        "properties": {
          "bars": {
            "additionalProperties": {
              "$ref": "#/components/schemas/stock_bar"
            },
            "type": "object"
          },
          "currency": {
            "type": "string"
          }
        },
        "required": [
          "bars"
        ],
        "type": "object"
      },
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
    "/v2/stocks/bars/latest": {
      "get": {
        "description": "The latest bars endpoint provides the latest minute bar for the given ticker symbols.\n",
        "operationId": "StockLatestBars",
        "parameters": [
          {
            "$ref": "#/components/parameters/stock_symbols"
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
                  "bars": {
                    "value": {
                      "bars": {
                        "AAPL": {
                          "c": 172.79,
                          "h": 172.81,
                          "l": 172.78,
                          "n": 20,
                          "o": 172.81,
                          "t": "2022-08-17T08:58:00Z",
                          "v": 1002,
                          "vw": 172.791417
                        },
                        "TSLA": {
                          "c": 914.3,
                          "h": 914.3,
                          "l": 914.3,
                          "n": 20,
                          "o": 914.3,
                          "t": "2022-08-17T08:57:00Z",
                          "v": 751,
                          "vw": 914.294634
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/stock_latest_bars_resp"
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
        "summary": "Latest bars",
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