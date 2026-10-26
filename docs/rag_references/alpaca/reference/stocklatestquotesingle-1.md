# Latest quote (single symbol)

Source: https://docs.alpaca.markets/us/reference/stocklatestquotesingle-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest quote (single symbol)

The latest quote endpoint provides the latest best bid and ask prices for a given ticker symbol.


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
      "stock_latest_quotes_resp_single": {
        "properties": {
          "currency": {
            "type": "string"
          },
          "quote": {
            "$ref": "#/components/schemas/stock_quote"
          },
          "symbol": {
            "type": "string"
          }
        },
        "required": [
          "quote",
          "symbol"
        ],
        "type": "object"
      },
      "stock_quote": {
        "description": "The best bid and ask information for a given security.",
        "examples": [
          {
            "ap": 387.7,
            "as": 1,
            "ax": "C",
            "bp": 387.67,
            "bs": 1,
            "bx": "N",
            "c": [
              "R"
            ],
            "t": "2021-02-06T13:35:08.946977536Z",
            "z": "C"
          }
        ],
        "properties": {
          "ap": {
            "description": "Ask price. 0 means the security has no active ask.",
            "format": "double",
            "type": "number"
          },
          "as": {
            "description": "Ask size in shares (round lots prior to November 3, 2025).",
            "format": "uint32",
            "type": "integer"
          },
          "ax": {
            "description": "Ask exchange. See `v2/stocks/meta/exchanges` for more details.",
            "type": "string"
          },
          "bp": {
            "description": "Bid price. 0 means the security has no active bid.",
            "format": "double",
            "type": "number"
          },
          "bs": {
            "description": "Bid size in shares (round lots prior to November 3, 2025).",
            "format": "uint32",
            "type": "integer"
          },
          "bx": {
            "description": "Bid exchange. See `v2/stocks/meta/exchanges` for more details.",
            "type": "string"
          },
          "c": {
            "description": "Condition flags. See `v2/stocks/meta/conditions/quote` for more details. If the array contains one flag, it applies to both the bid and ask. If the array contains two flags, the first one applies to the bid and the second one to the ask.\n",
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          },
          "z": {
            "$ref": "#/components/schemas/stock_tape"
          }
        },
        "required": [
          "t",
          "bx",
          "bp",
          "bs",
          "ap",
          "as",
          "ax",
          "c",
          "z"
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
    "/v2/stocks/{symbol}/quotes/latest": {
      "get": {
        "description": "The latest quote endpoint provides the latest best bid and ask prices for a given ticker symbol.\n",
        "operationId": "StockLatestQuoteSingle",
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
                  "quotes": {
                    "value": {
                      "quote": {
                        "ap": 172.7,
                        "as": 1,
                        "ax": "Q",
                        "bp": 172.6,
                        "bs": 2,
                        "bx": "Q",
                        "c": [
                          "R"
                        ],
                        "t": "2022-08-17T10:09:34.055031265Z",
                        "z": "C"
                      },
                      "symbol": "AAPL"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/stock_latest_quotes_resp_single"
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
        "summary": "Latest quote (single symbol)",
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