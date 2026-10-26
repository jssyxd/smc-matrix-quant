# Historical bars

Source: https://docs.alpaca.markets/us/reference/cryptobars-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical bars

The crypto bars API provides historical aggregates for a list of crypto symbols between the specified dates.


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
      "crypto_historical_loc": {
        "description": "Crypto location from where the historical market data is retrieved.\n- `us`: Alpaca US\n- `us-1`: Kraken US\n- `eu-1`: Kraken EU\n",
        "in": "path",
        "name": "loc",
        "required": true,
        "schema": {
          "$ref": "#/components/schemas/crypto_historical_loc"
        }
      },
      "crypto_symbols": {
        "description": "A comma-separated list of crypto symbols.",
        "example": "BTC/USD,LTC/USD",
        "in": "query",
        "name": "symbols",
        "required": true,
        "schema": {
          "type": "string"
        }
      },
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
      "timeframe": {
        "description": "The timeframe represented by each bar in aggregation.\nYou can use any of the following values:\n - `[1-59]Min` or `[1-59]T`, e.g. `5Min` or `5T` creates 5-minute aggregations\n - `[1-23]Hour` or `[1-23]H`, e.g. `12Hour` or `12H` creates 12-hour aggregations\n - `1Day` or `1D` creates 1-day aggregations\n - `1Week` or `1W` creates 1-week aggregations\n - `[1,2,3,4,6,12]Month` or `[1,2,3,4,6,12]M`, e.g. `3Month` or `3M` creates 3-month aggregations\n",
        "example": "1Min",
        "in": "query",
        "name": "timeframe",
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
      "crypto_bar": {
        "description": "OHLC aggregate of all the trades in a given interval.",
        "examples": [
          {
            "c": 29003,
            "h": 29003,
            "l": 28999,
            "n": 4,
            "o": 28999,
            "t": "2022-05-27T10:18:00Z",
            "v": 0.01,
            "vw": 29001
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
            "format": "double",
            "type": "number"
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
      "crypto_bars_resp": {
        "properties": {
          "bars": {
            "additionalProperties": {
              "items": {
                "$ref": "#/components/schemas/crypto_bar"
              },
              "type": "array"
            },
            "type": "object"
          },
          "next_page_token": {
            "$ref": "#/components/schemas/next_page_token"
          }
        },
        "required": [
          "bars",
          "next_page_token"
        ],
        "type": "object"
      },
      "crypto_historical_loc": {
        "description": "Crypto location from where the historical market data is retrieved.",
        "enum": [
          "us",
          "us-1",
          "us-2",
          "eu-1",
          "bs-1"
        ],
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
    "/v1beta3/crypto/{loc}/bars": {
      "get": {
        "description": "The crypto bars API provides historical aggregates for a list of crypto symbols between the specified dates.\n",
        "operationId": "CryptoBars",
        "parameters": [
          {
            "$ref": "#/components/parameters/crypto_historical_loc"
          },
          {
            "$ref": "#/components/parameters/crypto_symbols"
          },
          {
            "$ref": "#/components/parameters/timeframe"
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
                  "bars": {
                    "value": {
                      "bars": {
                        "BTC/USD": [
                          {
                            "c": 29003,
                            "h": 29003,
                            "l": 28999,
                            "n": 4,
                            "o": 28999,
                            "t": "2022-05-27T10:18:00Z",
                            "v": 0.01,
                            "vw": 29001
                          }
                        ]
                      },
                      "next_page_token": "MTY0MDk0ODkyMzAwMDAwMDAwMHwyNDg0MzE3MQ=="
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/crypto_bars_resp"
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
        "summary": "Historical bars",
        "tags": [
          "Crypto"
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
      "description": "Endpoints for cryptocurrencies.",
      "name": "Crypto"
    }
  ]
}
```