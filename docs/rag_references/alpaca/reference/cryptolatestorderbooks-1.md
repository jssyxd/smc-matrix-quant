# Latest orderbook

Source: https://docs.alpaca.markets/us/reference/cryptolatestorderbooks-1.md

---
updatedAt: 2026-05-27T17:58:03.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Latest orderbook

The latest orderbook endpoint returns the latest bid and ask orderbook for the crypto symbols provided.


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
      "crypto_latest_orderbooks_resp": {
        "properties": {
          "orderbooks": {
            "additionalProperties": {
              "$ref": "#/components/schemas/crypto_orderbook"
            },
            "type": "object"
          }
        },
        "required": [
          "orderbooks"
        ],
        "type": "object"
      },
      "crypto_orderbook": {
        "description": "Snapshot of the orderbook.",
        "examples": [
          {
            "a": [
              {
                "p": 20902,
                "s": 0.0097
              },
              {
                "p": 21444,
                "s": 0
              }
            ],
            "b": [
              {
                "p": 20846,
                "s": 0.1902
              },
              {
                "p": 20350,
                "s": 0
              }
            ],
            "t": "2022-06-24T08:00:14.137774336Z"
          }
        ],
        "properties": {
          "a": {
            "items": {
              "$ref": "#/components/schemas/crypto_orderbook_entry"
            },
            "type": "array"
          },
          "b": {
            "items": {
              "$ref": "#/components/schemas/crypto_orderbook_entry"
            },
            "type": "array"
          },
          "t": {
            "$ref": "#/components/schemas/timestamp"
          }
        },
        "required": [
          "t",
          "b",
          "a"
        ],
        "type": "object"
      },
      "crypto_orderbook_entry": {
        "description": "A single entry in a crypto orderbook.",
        "examples": [
          {
            "p": 20846,
            "s": 0.1902
          }
        ],
        "properties": {
          "p": {
            "description": "Price.",
            "format": "double",
            "type": "number"
          },
          "s": {
            "description": "Size.",
            "format": "double",
            "type": "number"
          }
        },
        "required": [
          "p",
          "s"
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
    "/v1beta3/crypto/{loc}/latest/orderbooks": {
      "get": {
        "description": "The latest orderbook endpoint returns the latest bid and ask orderbook for the crypto symbols provided.\n",
        "operationId": "CryptoLatestOrderbooks",
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
                  "orderbooks": {
                    "value": {
                      "orderbooks": {
                        "BTC/USD": {
                          "a": [
                            {
                              "p": 20902,
                              "s": 0.0097
                            },
                            {
                              "p": 21444,
                              "s": 0
                            }
                          ],
                          "b": [
                            {
                              "p": 20846,
                              "s": 0.1902
                            },
                            {
                              "p": 20350,
                              "s": 0
                            }
                          ],
                          "t": "2022-06-24T08:00:14.137774336Z"
                        }
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/crypto_latest_orderbooks_resp"
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
        "summary": "Latest orderbook",
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