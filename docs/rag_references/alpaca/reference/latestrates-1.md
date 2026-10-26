# Latest rates for currency pairs

Source: https://docs.alpaca.markets/us/reference/latestrates-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest rates for currency pairs

Get the latest forex rates for the given currency pairs.


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
      "forex_latest_rates_resp": {
        "description": "The response object of the latest forex rates.",
        "properties": {
          "rates": {
            "additionalProperties": {
              "$ref": "#/components/schemas/forex_rate"
            },
            "type": "object"
          }
        },
        "required": [
          "rates"
        ],
        "type": "object"
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
    "/v1beta1/forex/latest/rates": {
      "get": {
        "description": "Get the latest forex rates for the given currency pairs.\n",
        "operationId": "LatestRates",
        "parameters": [
          {
            "$ref": "#/components/parameters/forex_currency_pairs"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "USDJPY": {
                    "value": {
                      "rates": {
                        "USDJPY": {
                          "ap": 128.112,
                          "bp": 127.752,
                          "mp": 127.779,
                          "t": "2022-05-20T05:38:41.311530885Z"
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/forex_latest_rates_resp"
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
        "summary": "Latest rates for currency pairs",
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