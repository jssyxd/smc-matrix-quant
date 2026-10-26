# Historical rates for currency pairs

Source: https://docs.alpaca.markets/us/reference/rates-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical rates for currency pairs

Get historical forex rates for the given currency pairs in the given time interval and at the given timeframe (snapshot frequency).


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
      "forex_currency_pairs": {
        "in": "query",
        "name": "currency_pairs",
        "required": true,
        "schema": {
          "allOf": [
            {
              "type": "string"
            },
            {
              "$ref": "#/components/schemas/forex_currency_pairs"
            }
          ]
        }
      },
      "forex_timeframe": {
        "in": "query",
        "name": "timeframe",
        "required": false,
        "schema": {
          "$ref": "#/components/schemas/forex_timeframe"
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
      "forex_currency_pairs": {
        "description": "A comma-separated string with currency pairs.",
        "examples": [
          "USDJPY",
          "USDMXN"
        ],
        "type": "string"
      },
      "forex_rate": {
        "description": "A foreign exchange rate between two currencies at a given time.",
        "examples": [
          {
            "ap": 127.763,
            "bp": 127.702,
            "mp": 127.757,
            "t": "2022-04-20T18:23:00Z"
          }
        ],
        "properties": {
          "ap": {
            "description": "The last ask price value of the currency at the end of the timeframe.",
            "format": "double",
            "type": "number"
          },
          "bp": {
            "description": "The last bid price value of the currency at the end of the timeframe.",
            "format": "double",
            "type": "number"
          },
          "mp": {
            "description": "The last mid price value of the currency at the end of the timeframe.",
            "format": "double",
            "type": "number"
          },
          "t": {
            "description": "Timestamp of the rate.",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "bp",
          "mp",
          "ap",
          "t"
        ],
        "type": "object"
      },
      "forex_rates_resp": {
        "properties": {
          "next_page_token": {
            "$ref": "#/components/schemas/next_page_token"
          },
          "rates": {
            "additionalProperties": {
              "items": {
                "$ref": "#/components/schemas/forex_rate"
              },
              "type": "array"
            },
            "type": "object"
          }
        },
        "required": [
          "rates",
          "next_page_token"
        ],
        "type": "object"
      },
      "forex_timeframe": {
        "default": "1Min",
        "description": "The sampling interval of the currency rates. For example, 5S returns forex rates sampled every five seconds.\nYou can use the following values:\n - `5Sec` or `5S`\n - `1Min` or `1T`\n - `1Day` or `1D`\n",
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
    "/v1beta1/forex/rates": {
      "get": {
        "description": "Get historical forex rates for the given currency pairs in the given time interval and at the given timeframe (snapshot frequency).\n",
        "operationId": "Rates",
        "parameters": [
          {
            "$ref": "#/components/parameters/forex_currency_pairs"
          },
          {
            "$ref": "#/components/parameters/forex_timeframe"
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
            "$ref": "#/components/parameters/sort"
          },
          {
            "$ref": "#/components/parameters/page_token"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "USDJPY": {
                    "value": {
                      "next_page_token": "VVNESlBZfDIwMjItMDEtMDNUMDA6MDM6MDBa",
                      "rates": {
                        "USDJPY": [
                          {
                            "ap": 115.18,
                            "bp": 114.192,
                            "mp": 115.144,
                            "t": "2022-01-03T00:01:00Z"
                          },
                          {
                            "ap": 115.185,
                            "bp": 114.189,
                            "mp": 115.138,
                            "t": "2022-01-03T00:02:00Z"
                          },
                          {
                            "ap": 115.148,
                            "bp": 115.122,
                            "mp": 115.131,
                            "t": "2022-01-03T00:03:00Z"
                          }
                        ]
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/forex_rates_resp"
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
            "BasicAuth": []
          },
          {
            "apiKey": [],
            "apiSecret": []
          }
        ],
        "summary": "Historical rates for currency pairs",
        "tags": [
          "Forex"
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
      "description": "Endpoints for forex currency rates.",
      "name": "Forex"
    }
  ]
}
```