# Top market movers

Source: https://docs.alpaca.markets/us/reference/movers-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Top market movers

Returns the top market movers (gainers and losers) based on real time SIP data.
The change for each symbol is calculated from the previous closing price and the latest closing price.

For stocks, the endpoint resets at market open. Until then, it shows the previous market day's movers.
The data is split-adjusted. Only tradable symbols in exchanges are included.

For crypto, the endpoint resets at midnight.

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
      "movers_market_type": {
        "description": "Screen-specific market (stocks or crypto).",
        "in": "path",
        "name": "market_type",
        "required": true,
        "schema": {
          "$ref": "#/components/schemas/market_type"
        }
      },
      "movers_top": {
        "description": "Number of top market movers to fetch (gainers and losers). Will return this number of results for each. By default, 10 gainers and 10 losers.\n",
        "in": "query",
        "name": "top",
        "required": false,
        "schema": {
          "default": 10,
          "format": "int32",
          "maximum": 50,
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
      "market_type": {
        "description": "Market type (stocks or crypto).",
        "enum": [
          "stocks",
          "crypto"
        ],
        "type": "string"
      },
      "mover": {
        "description": "A symbol whose price moved significantly.",
        "examples": [
          {
            "change": 2.46,
            "percent_change": 145.56,
            "price": 4.15,
            "symbol": "AGRI"
          }
        ],
        "properties": {
          "change": {
            "description": "Difference in change for the day.",
            "format": "double",
            "type": "number"
          },
          "percent_change": {
            "description": "Percentage difference change for the day.",
            "format": "double",
            "type": "number"
          },
          "price": {
            "description": "Current price of market moving asset.",
            "format": "double",
            "type": "number"
          },
          "symbol": {
            "description": "Symbol of market moving asset.",
            "type": "string"
          }
        },
        "required": [
          "symbol",
          "percent_change",
          "change",
          "price"
        ],
        "title": "Mover",
        "type": "object"
      },
      "movers_resp": {
        "description": "Contains list of market movers.",
        "properties": {
          "gainers": {
            "description": "List of top N gainers.",
            "items": {
              "$ref": "#/components/schemas/mover"
            },
            "type": "array"
          },
          "last_updated": {
            "description": "Time when the movers were last computed. Formatted as a RFC-3339 date-time with nanosecond precision.\n",
            "type": "string"
          },
          "losers": {
            "description": "List of top N losers.",
            "items": {
              "$ref": "#/components/schemas/mover"
            },
            "type": "array"
          },
          "market_type": {
            "$ref": "#/components/schemas/market_type"
          }
        },
        "required": [
          "gainers",
          "losers",
          "market_type",
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
    "/v1beta1/screener/{market_type}/movers": {
      "get": {
        "description": "Returns the top market movers (gainers and losers) based on real time SIP data.\nThe change for each symbol is calculated from the previous closing price and the latest closing price.\n\nFor stocks, the endpoint resets at market open. Until then, it shows the previous market day's movers.\nThe data is split-adjusted. Only tradable symbols in exchanges are included.\n\nFor crypto, the endpoint resets at midnight.",
        "operationId": "Movers",
        "parameters": [
          {
            "$ref": "#/components/parameters/movers_market_type"
          },
          {
            "$ref": "#/components/parameters/movers_top"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "movers": {
                    "value": {
                      "gainers": [
                        {
                          "change": 2.46,
                          "percent_change": 145.56,
                          "price": 4.15,
                          "symbol": "AGRI"
                        },
                        {
                          "change": 0.03,
                          "percent_change": 85.63,
                          "price": 0.0594,
                          "symbol": "GRCYW"
                        }
                      ],
                      "last_updated": "2022-03-10T17:53:30.088309839Z",
                      "losers": [
                        {
                          "change": -0.26,
                          "percent_change": -63.07,
                          "price": 0.1502,
                          "symbol": "MTACW"
                        },
                        {
                          "change": -3.61,
                          "percent_change": -51.21,
                          "price": 3.435,
                          "symbol": "TIG"
                        }
                      ],
                      "market_type": "stocks"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/movers_resp"
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
        "summary": "Top market movers",
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