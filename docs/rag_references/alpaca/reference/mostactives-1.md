# Most active stocks

Source: https://docs.alpaca.markets/us/reference/mostactives-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Most active stocks

Returns the most active stocks by volume or trade count based on real time SIP data. By default, returns the top 10 symbols by volume.


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
      "most_actives_by": {
        "description": "The metric used for ranking the most active stocks.",
        "in": "query",
        "name": "by",
        "required": false,
        "schema": {
          "default": "volume",
          "enum": [
            "volume",
            "trades"
          ],
          "type": "string"
        }
      },
      "most_actives_top": {
        "description": "The number of top most active stocks to fetch per day.",
        "in": "query",
        "name": "top",
        "required": false,
        "schema": {
          "default": 10,
          "format": "int32",
          "maximum": 100,
          "minimum": 1,
          "type": "integer"
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
      "most_active": {
        "description": "A stock that is most active by either volume or trade count.",
        "examples": [
          {
            "symbol": "AAPL",
            "trade_count": 639626,
            "volume": 122709184
          }
        ],
        "properties": {
          "symbol": {
            "type": "string"
          },
          "trade_count": {
            "description": "Cumulative trade count for the current trading day.",
            "format": "int64",
            "type": "integer"
          },
          "volume": {
            "description": "Cumulative volume for the current trading day.",
            "format": "int64",
            "type": "integer"
          }
        },
        "required": [
          "symbol",
          "volume",
          "trade_count"
        ],
        "type": "object"
      },
      "most_actives_resp": {
        "properties": {
          "last_updated": {
            "description": "Time when the most actives were last computed. Formatted as a RFC-3339 date-time with nanosecond precision.\n",
            "type": "string"
          },
          "most_actives": {
            "description": "List of top N most active symbols.",
            "items": {
              "$ref": "#/components/schemas/most_active"
            },
            "type": "array"
          }
        },
        "required": [
          "most_actives",
          "last_updated"
        ],
        "type": "object"
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
    "/v1beta1/screener/stocks/most-actives": {
      "get": {
        "description": "Returns the most active stocks by volume or trade count based on real time SIP data. By default, returns the top 10 symbols by volume.\n",
        "operationId": "MostActives",
        "parameters": [
          {
            "$ref": "#/components/parameters/most_actives_by"
          },
          {
            "$ref": "#/components/parameters/most_actives_top"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/most_actives_resp"
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
        "summary": "Most active stocks",
        "tags": [
          "Screener"
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
      "description": "Endpoints for most active stocks and top movers.",
      "name": "Screener"
    }
  ]
}
```