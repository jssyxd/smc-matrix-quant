# Latest bars

Source: https://docs.alpaca.markets/us/reference/cryptolatestbars-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest bars

The latest multi-bars endpoint returns the latest minute-aggregated historical bar data for each of the crypto symbols provided.


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
      "crypto_latest_loc": {
        "description": "Crypto location from where the latest market data is retrieved.\n- `us`: Alpaca US\n- `us-1`: Kraken US\n- `eu-1`: Kraken EU\n",
        "in": "path",
        "name": "loc",
        "required": true,
        "schema": {
          "$ref": "#/components/schemas/crypto_latest_loc"
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
      "crypto_latest_bars_resp": {
        "properties": {
          "bars": {
            "additionalProperties": {
              "$ref": "#/components/schemas/crypto_bar"
            },
            "type": "object"
          }
        },
        "required": [
          "bars"
        ],
        "type": "object"
      },
      "crypto_latest_loc": {
        "description": "Crypto location from where the latest market data is retrieved.",
        "enum": [
          "us",
          "us-1",
          "us-2",
          "eu-1",
          "bs-1"
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
    "/v1beta3/crypto/{loc}/latest/bars": {
      "get": {
        "description": "The latest multi-bars endpoint returns the latest minute-aggregated historical bar data for each of the crypto symbols provided.\n",
        "operationId": "CryptoLatestBars",
        "parameters": [
          {
            "$ref": "#/components/parameters/crypto_latest_loc"
          },
          {
            "$ref": "#/components/parameters/crypto_symbols"
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
                        "BTC/USD": {
                          "c": 29003,
                          "h": 29003,
                          "l": 28999,
                          "n": 4,
                          "o": 28999,
                          "t": "2022-05-27T10:18:00Z",
                          "v": 0.01,
                          "vw": 29001
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/crypto_latest_bars_resp"
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
        "summary": "Latest bars",
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