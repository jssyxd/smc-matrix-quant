# Latest quotes

Source: https://docs.alpaca.markets/us/reference/optionlatestquotes.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest quotes

The latest multi-quotes endpoint provides the latest bid and ask prices for each given contract symbol.


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
      "option_feed": {
        "description": "The source feed of the data. `opra` is the official OPRA feed, `indicative` is a free indicative feed where trades are delayed and quotes are modified. Default: `opra` if the user has a subscription, otherwise `indicative`.\n",
        "in": "query",
        "name": "feed",
        "schema": {
          "$ref": "#/components/schemas/option_feed"
        }
      },
      "option_symbols": {
        "description": "A comma-separated list of contract symbols with a limit of 100.",
        "example": "AAPL241220C00300000,AAPL240315C00225000",
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
      "option_feed": {
        "default": "opra",
        "enum": [
          "opra",
          "indicative"
        ],
        "type": "string"
      },
      "option_latest_quotes_resp": {
        "properties": {
          "quotes": {
            "additionalProperties": {
              "$ref": "#/components/schemas/option_quote"
            },
            "type": "object"
          }
        },
        "required": [
          "quotes"
        ],
        "type": "object"
      },
      "option_quote": {
        "description": "The best bid and ask information for a given option.\n",
        "examples": [
          {
            "ap": 0.16,
            "as": 669,
            "ax": "w",
            "bp": 0.15,
            "bs": 164,
            "bx": "W",
            "c": "A",
            "t": "2024-02-28T15:30:28.046330624Z"
          }
        ],
        "properties": {
          "ap": {
            "description": "Ask price.",
            "format": "double",
            "type": "number"
          },
          "as": {
            "description": "Ask size.",
            "format": "uint32",
            "type": "integer"
          },
          "ax": {
            "description": "Ask exchange.",
            "type": "string"
          },
          "bp": {
            "description": "Bid price.",
            "format": "double",
            "type": "number"
          },
          "bs": {
            "description": "Bid size.",
            "format": "uint32",
            "type": "integer"
          },
          "bx": {
            "description": "Bid exchange.",
            "type": "string"
          },
          "c": {
            "description": "Quote condition.",
            "type": "string"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
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
    "/v1beta1/options/quotes/latest": {
      "get": {
        "description": "The latest multi-quotes endpoint provides the latest bid and ask prices for each given contract symbol.\n",
        "operationId": "OptionLatestQuotes",
        "parameters": [
          {
            "$ref": "#/components/parameters/option_symbols"
          },
          {
            "$ref": "#/components/parameters/option_feed"
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
                        "AAPL240419P00140000": {
                          "ap": 0.16,
                          "as": 669,
                          "ax": "w",
                          "bp": 0.15,
                          "bs": 164,
                          "bx": "W",
                          "c": "A",
                          "t": "2024-02-28T15:30:28.046330624Z"
                        },
                        "AAPL250321C00190000": {
                          "ap": 17,
                          "as": 622,
                          "ax": "X",
                          "bp": 16.75,
                          "bs": 368,
                          "bx": "X",
                          "c": " ",
                          "t": "2024-02-28T15:47:13.663636224Z"
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/option_latest_quotes_resp"
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
          "Option"
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
      "description": "Endpoints for option data.",
      "name": "Option"
    }
  ]
}
```