# Latest prices

Source: https://docs.alpaca.markets/us/reference/fixedincomelatestprices.md

---
updatedAt: 2026-07-23T07:36:02.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest prices

This endpoint returns the latest prices for the given fixed income securities.


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
      "isins": {
        "description": "A comma-separated list of ISINs with a limit of 1000.",
        "example": "US912797KJ59,US912797KS58,US912797LB15",
        "in": "query",
        "name": "isins",
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
      "fixed_income_latest_prices_resp": {
        "description": "Latest fixed-income prices keyed by ISIN.",
        "examples": [
          {
            "prices": {
              "US912797KJ59": {
                "p": 99.6459,
                "t": "2025-02-14T20:58:00.648Z",
                "ytm": 4.249,
                "ytw": 4.249
              }
            }
          }
        ],
        "properties": {
          "prices": {
            "additionalProperties": {
              "$ref": "#/components/schemas/fixed_income_price"
            },
            "type": "object"
          }
        },
        "required": [
          "prices"
        ],
        "type": "object"
      },
      "fixed_income_price": {
        "description": "The price of the instrument as a percentage of its par value.",
        "examples": [
          {
            "p": 99.6459,
            "t": "2025-02-14T20:58:00.648Z",
            "ytm": 4.249,
            "ytw": 4.249
          }
        ],
        "properties": {
          "p": {
            "description": "Price",
            "format": "double",
            "type": "number"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          },
          "ytm": {
            "description": "Yield to maturity.",
            "format": "double",
            "type": "number"
          },
          "ytw": {
            "description": "Yield to worst.",
            "format": "double",
            "type": "number"
          }
        },
        "required": [
          "t",
          "p"
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
    "/v1beta1/fixed_income/latest/prices": {
      "get": {
        "description": "This endpoint returns the latest prices for the given fixed income securities.\n",
        "operationId": "FixedIncomeLatestPrices",
        "parameters": [
          {
            "$ref": "#/components/parameters/isins"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "prices": {
                    "value": {
                      "prices": {
                        "US912797KJ59": {
                          "p": 99.6459,
                          "t": "2025-02-14T20:58:00.648Z",
                          "ytm": 4.249,
                          "ytw": 4.249
                        },
                        "US912797KS58": {
                          "p": 99.3193,
                          "t": "2025-02-14T20:58:00.648Z",
                          "ytm": 4.2245,
                          "ytw": 4.2245
                        },
                        "US912797LB15": {
                          "p": 98.9927,
                          "t": "2025-02-14T20:58:00.648Z",
                          "ytm": 4.2165,
                          "ytw": 4.2165
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/fixed_income_latest_prices_resp"
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
        "summary": "Latest prices",
        "tags": [
          "Fixed income"
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
      "description": "Endpoints for fixed income data.",
      "name": "Fixed income"
    }
  ]
}
```