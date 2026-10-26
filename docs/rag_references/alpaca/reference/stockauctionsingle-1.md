# Historical auctions (single)

Source: https://docs.alpaca.markets/us/reference/stockauctionsingle-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical auctions (single)

The historical auctions endpoint provides auction prices for the given stock symbol between the specified dates.


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
      "end": {
        "description": "The inclusive end of the interval. Format: RFC-3339 or YYYY-MM-DD.\nDefault: the current time if the user has a real-time access for the feed, otherwise 15 minutes before the current time.\n",
        "examples": {
          "RFC-3339 nanosecond": {
            "summary": "RFC-3339 date-time with nanosecond accuracy",
            "value": "2024-01-04T01:02:03.123456789Z"
          },
          "RFC-3339 second": {
            "summary": "RFC-3339 date-time with second accuracy",
            "value": "2024-01-04T00:00:00Z"
          },
          "RFC-3339 with timezone": {
            "summary": "RFC-3339 date-time with time zone",
            "value": "2024-01-04T09:30:00-04:00"
          },
          "date": {
            "summary": "Date",
            "value": "2024-01-04"
          }
        },
        "in": "query",
        "name": "end",
        "required": false,
        "schema": {
          "format": "date-time",
          "type": "string"
        }
      },
      "limit": {
        "description": "The maximum number of data points to return in the response page.\nThe API may return less, even if there are more available data points in the requested interval.\nAlways check the `next_page_token` for more pages.\nThe limit applies to the total number of data points, not per symbol!\n",
        "in": "query",
        "name": "limit",
        "required": false,
        "schema": {
          "default": 1000,
          "maximum": 10000,
          "minimum": 1,
          "type": "integer"
        }
      },
      "page_token": {
        "description": "The pagination token from which to continue. The value to pass here is returned in specific requests when more data is available, usually because of a response result limit.\n",
        "in": "query",
        "name": "page_token",
        "schema": {
          "type": "string"
        }
      },
      "sort": {
        "description": "Sort data in ascending or descending order.",
        "in": "query",
        "name": "sort",
        "schema": {
          "allOf": [
            {
              "type": "string"
            },
            {
              "$ref": "#/components/schemas/sort"
            }
          ]
        }
      },
      "start": {
        "description": "The inclusive start of the interval. Format: RFC-3339 or YYYY-MM-DD.\nDefault: the beginning of the current day, but at least 15 minutes ago if the user doesn't have real-time access for the feed.\n",
        "examples": {
          "RFC-3339 nanosecond": {
            "summary": "RFC-3339 date-time with nanosecond accuracy",
            "value": "2024-01-03T01:02:03.123456789Z"
          },
          "RFC-3339 second": {
            "summary": "RFC-3339 date-time with second accuracy",
            "value": "2024-01-03T00:00:00Z"
          },
          "RFC-3339 with timezone": {
            "summary": "RFC-3339 date-time with time zone",
            "value": "2024-01-03T09:30:00-04:00"
          },
          "date": {
            "summary": "Date",
            "value": "2024-01-03"
          }
        },
        "in": "query",
        "name": "start",
        "required": false,
        "schema": {
          "format": "date-time",
          "type": "string"
        }
      },
      "stock_asof": {
        "description": "The as-of date of the queried stock symbol(s). Format: YYYY-MM-DD. Default: current day.\n\nThis date is used to identify the underlying entity of the provided symbol(s), so that name changes for this entity can be found. Data for past symbol(s) is returned if the query date range spans the name change.\n\nThe special value of \"-\" means symbol mapping is skipped. Data is returned based on the symbol alone without looking up previous names. The same happens if the queried symbol is not found on the given `asof` date.\n\nExample: FB was renamed to META in 2022-06-09. Querying META with an `asof` date after 2022-06-09 will also yield FB data. The data for the FB ticker will be labeled as META because they are considered the same underlying entity as of 2022-06-09. Querying FB with an `asof` date after 2022-06-09 will only return data with the FB ticker, not with META. But with an `asof` date before 2022-06-09, META will also be returned (as FB).\n",
        "in": "query",
        "name": "asof",
        "schema": {
          "type": "string"
        }
      },
      "stock_auction_feed": {
        "description": "Only `sip` is valid for auctions.",
        "in": "query",
        "name": "feed",
        "schema": {
          "$ref": "#/components/schemas/stock_auction_feed"
        }
      },
      "stock_currency": {
        "description": "The currency of all prices in ISO 4217 format. Default: USD.\n",
        "in": "query",
        "name": "currency",
        "schema": {
          "type": "string"
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
      "date": {
        "description": "Date in RFC-3339.",
        "format": "date",
        "type": "string"
      },
      "next_page_token": {
        "description": "Pagination token for the next page.",
        "type": [
          "string",
          "null"
        ]
      },
      "sort": {
        "default": "asc",
        "description": "Sort data in ascending or descending order.",
        "enum": [
          "asc",
          "desc"
        ],
        "type": "string"
      },
      "stock_auction": {
        "description": "An auction\n",
        "examples": [
          {
            "c": "O",
            "p": 135,
            "t": "2022-10-13T13:30:01.688322951Z",
            "x": "Q"
          }
        ],
        "properties": {
          "c": {
            "description": "The condition flag indicating that this is an auction. See `v2/stocks/meta/conditions/trade` for more details.\n",
            "type": "string"
          },
          "p": {
            "description": "Auction price.",
            "format": "double",
            "type": "number"
          },
          "s": {
            "description": "Auction trade size.",
            "format": "int64",
            "type": "integer"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          },
          "x": {
            "description": "Exchange code. See `v2/stocks/meta/exchanges` for more details.",
            "type": "string"
          }
        },
        "required": [
          "t",
          "x",
          "p",
          "c"
        ],
        "type": "object"
      },
      "stock_auction_feed": {
        "default": "sip",
        "type": "string"
      },
      "stock_auctions_resp_single": {
        "properties": {
          "auctions": {
            "items": {
              "$ref": "#/components/schemas/stock_daily_auctions"
            },
            "type": "array"
          },
          "currency": {
            "type": "string"
          },
          "next_page_token": {
            "$ref": "#/components/schemas/next_page_token"
          },
          "symbol": {
            "type": "string"
          }
        },
        "required": [
          "auctions",
          "next_page_token",
          "symbol"
        ],
        "type": "object"
      },
      "stock_daily_auctions": {
        "description": "Opening and closing auction prices for a given day.\n",
        "properties": {
          "c": {
            "description": "Closing auctions. Every price / exchange / condition triplet is only shown once, with its earliest timestamp.",
            "items": {
              "$ref": "#/components/schemas/stock_auction"
            },
            "type": "array"
          },
          "d": {
            "$ref": "#/components/schemas/date"
          },
          "o": {
            "description": "Opening auctions.",
            "items": {
              "$ref": "#/components/schemas/stock_auction"
            },
            "type": "array"
          }
        },
        "required": [
          "d",
          "o",
          "c"
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
    "/v2/stocks/{symbol}/auctions": {
      "get": {
        "description": "The historical auctions endpoint provides auction prices for the given stock symbol between the specified dates.\n",
        "operationId": "StockAuctionSingle",
        "parameters": [
          {
            "$ref": "#/components/parameters/stock_symbol"
          },
          {
            "$ref": "#/components/parameters/start"
          },
          {
            "$ref": "#/components/parameters/end"
          },
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/stock_asof"
          },
          {
            "$ref": "#/components/parameters/stock_auction_feed"
          },
          {
            "$ref": "#/components/parameters/stock_currency"
          },
          {
            "$ref": "#/components/parameters/page_token"
          },
          {
            "$ref": "#/components/parameters/sort"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "auctions": {
                    "value": {
                      "auctions": [
                        {
                          "c": [
                            {
                              "c": "M",
                              "p": 221.7,
                              "t": "2022-10-13T20:00:00.152902912Z",
                              "x": "P"
                            }
                          ],
                          "d": "2022-10-13",
                          "o": [
                            {
                              "c": "Q",
                              "p": 208.37,
                              "t": "2022-10-13T13:30:00.068034304Z",
                              "x": "P"
                            },
                            {
                              "c": "O",
                              "p": 208.49,
                              "t": "2022-10-13T13:30:01.079567733Z",
                              "x": "Q"
                            },
                            {
                              "c": "Q",
                              "p": 208.49,
                              "t": "2022-10-13T13:30:01.090802222Z",
                              "x": "Q"
                            }
                          ]
                        }
                      ],
                      "next_page_token": "MjAyMi0xMC0xM1QyMDowMDowMC4xNTI5MDI5MTJafFA=",
                      "symbol": "TSLA"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/stock_auctions_resp_single"
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
        "summary": "Historical auctions (single)",
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