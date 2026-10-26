# Latest quotes

Source: https://docs.alpaca.markets/us/reference/fixedincomelatestquotes.md

---
updatedAt: 2026-06-03T08:19:09.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest quotes

This endpoint returns the latest quotes for the given fixed income securities.


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
      "trade_size": {
        "description": "Filters to best bid/ask where the minimum trade size is less than or equal to the given numeric value. For any negative value the best bid/ask will be returned for the smallest trade size on either side.\n",
        "in": "query",
        "name": "trade_size",
        "required": false,
        "schema": {
          "format": "int32",
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
      "fixed_income_latest_quotes_resp": {
        "description": "Latest fixed-income best bid and ask quotes keyed by ISIN.",
        "examples": [
          {
            "quotes": {
              "US912797SX61": {
                "ams": 1000,
                "ap": 99.91958333,
                "as": 1000000,
                "aytm": 2.226923,
                "aytw": 2.226923,
                "bms": 1000,
                "bp": 99.81091667,
                "bs": 1000000,
                "bytm": 5.236154,
                "bytw": 5.236154,
                "t": "2026-05-21T06:56:01.882466873Z"
              }
            }
          }
        ],
        "properties": {
          "quotes": {
            "additionalProperties": {
              "$ref": "#/components/schemas/fixed_income_quote"
            },
            "type": "object"
          }
        },
        "required": [
          "quotes"
        ],
        "type": "object"
      },
      "fixed_income_quote": {
        "description": "The best bid and ask information for a given fixed income security. A value of 0 means there is no active bid or ask for that field.\n",
        "examples": [
          {
            "ams": 1000,
            "ap": 99.91958333,
            "as": 1000000,
            "aytm": 2.226923,
            "aytw": 2.226923,
            "bms": 1000,
            "bp": 99.81091667,
            "bs": 1000000,
            "bytm": 5.236154,
            "bytw": 5.236154,
            "t": "2026-05-21T06:56:01.882466873Z"
          }
        ],
        "properties": {
          "ams": {
            "description": "Best ask minimum trade size in par value.",
            "format": "int64",
            "type": "integer"
          },
          "ap": {
            "description": "Best ask price. 0 means there is no active ask.",
            "format": "double",
            "type": "number"
          },
          "as": {
            "description": "Best ask size in par value. 0 means there is no active ask.",
            "format": "int64",
            "type": "integer"
          },
          "aytm": {
            "description": "Best ask yield to maturity.",
            "format": "double",
            "type": "number"
          },
          "aytw": {
            "description": "Best ask yield to worst.",
            "format": "double",
            "type": "number"
          },
          "bms": {
            "description": "Best bid minimum trade size in par value.",
            "format": "int64",
            "type": "integer"
          },
          "bp": {
            "description": "Best bid price. 0 means there is no active bid.",
            "format": "double",
            "type": "number"
          },
          "bs": {
            "description": "Best bid size in par value. 0 means there is no active bid.",
            "format": "int64",
            "type": "integer"
          },
          "bytm": {
            "description": "Best bid yield to maturity.",
            "format": "double",
            "type": "number"
          },
          "bytw": {
            "description": "Best bid yield to worst.",
            "format": "double",
            "type": "number"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          }
        },
        "required": [
          "t",
          "bp",
          "bs",
          "bms",
          "bytm",
          "bytw",
          "ap",
          "as",
          "ams",
          "aytm",
          "aytw"
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
    "/v1beta1/fixed_income/latest/quotes": {
      "get": {
        "description": "This endpoint returns the latest quotes for the given fixed income securities.\n",
        "operationId": "FixedIncomeLatestQuotes",
        "parameters": [
          {
            "description": "A comma-separated list of ISINs with a limit of 100.",
            "example": "US912797SX61,US912810SK51",
            "in": "query",
            "name": "isins",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "$ref": "#/components/parameters/trade_size"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "quotes": {
                    "value": {
                      "quotes": {
                        "US912797SX61": {
                          "ams": 1000,
                          "ap": 99.91958333,
                          "as": 1000000,
                          "aytm": 2.226923,
                          "aytw": 2.226923,
                          "bms": 1000,
                          "bp": 99.81091667,
                          "bs": 1000000,
                          "bytm": 5.236154,
                          "bytw": 5.236154,
                          "t": "2026-05-21T06:56:01.882466873Z"
                        },
                        "US912810SK51": {
                          "ams": 1000,
                          "ap": 63.06436526,
                          "as": 1000000,
                          "aytm": 5.08819,
                          "aytw": 5.08819,
                          "bms": 1000,
                          "bp": 60.60009769,
                          "bs": 1000000,
                          "bytm": 5.338343,
                          "bytw": 5.338343,
                          "t": "2026-05-21T07:27:53.683424845Z"
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/fixed_income_latest_quotes_resp"
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
        "summary": "Latest quotes",
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