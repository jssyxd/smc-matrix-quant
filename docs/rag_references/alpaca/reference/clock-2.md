# Get Market Clock

Source: https://docs.alpaca.markets/us/reference/clock-2.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Market Clock

This API serves information about multiple markets: the current time, if it's a market day, the current phase of the market, etc.


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
      "markets": {
        "description": "Comma-separated list of markets. Available market codes by region:\n\n**United States**\n- `BMO`: Bank of Montreal. US banking calendar (US operations).\n- `BNYM`: The Bank of New York Mellon. US banking calendar.\n- `BOATS`: Blue Ocean Alternative Trading System. US overnight trading.\n- `IEX`: Investors Exchange. US equities.\n- `IEXG`: Investors Exchange. US equities.\n- `NASDAQ`: National Association of Securities Dealers Automated Quotations. US equities.\n- `NYSE`: New York Stock Exchange. US equities.\n- `OCEA`: BlueOcean ATS. US overnight trading.\n- `OPRA`: Options Price Reporting Authority. US options.\n- `OTC`: Over-The-Counter. US OTC equities.\n- `OTCM`: OTC Markets. US OTC equities.\n- `SIFMA`: Securities Industry and Financial Markets Association. US bonds.\n- `XNAS`: NASDAQ. US equities.\n- `XNYS`: New York Stock Exchange. US equities.\n\n**Europe**\n- `CEUX`: Cboe CEUX Europe. European equities (Cboe Netherlands).\n- `CHIX`: Cboe CHIX Europe. European equities (Cboe UK).\n- `ISE`: Euronext Dublin. Irish equities.\n- `LSE`: London Stock Exchange. UK equities.\n- `MTA`: Euronext Milan. Italian equities.\n- `MTAA`: Euronext Milan. Italian equities.\n- `XAMS`: Euronext Amsterdam. Dutch equities.\n- `XBRU`: Euronext Brussels. Belgian equities.\n- `XDUB`: Euronext Dublin. Irish equities.\n- `XETR`: Frankfurt Stock Exchange. German equities.\n- `XETRA`: Frankfurt Stock Exchange. German equities.\n- `XLIS`: Euronext Lisbon. Portuguese equities.\n- `XLON`: London Stock Exchange. UK equities.\n- `XPAR`: Euronext Paris. French equities.\n\n**Asia & Middle East**\n- `HKEX`: Hong Kong Stock Exchange. Hong Kong equities.\n- `JPX`: Japan Exchange Group. Japanese equities.\n- `TADAWUL`: Saudi Stock Exchange. Saudi equities.\n- `XHKG`: Hong Kong Stock Exchange. Hong Kong equities.\n- `XSAU`: Saudi Stock Exchange. Saudi equities.\n- `XTKS`: Japan Exchange Group. Japanese equities.\n",
        "example": "NYSE,LSE",
        "in": "query",
        "name": "markets",
        "schema": {
          "type": "string"
        }
      },
      "time": {
        "description": "Instead of the current time, use this time for the clock.",
        "in": "query",
        "name": "time",
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
        "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on Slack or on the Community Forum.\n"
      }
    },
    "schemas": {
      "bic": {
        "description": "Business Identifier Code (BIC/SWIFT).",
        "example": "IRVTUS3NXXX",
        "maxLength": 11,
        "minLength": 11,
        "pattern": "^[A-Z0-9]{11}$",
        "type": "string"
      },
      "clock": {
        "properties": {
          "is_market_day": {
            "description": "Whether the clock is on a market day.",
            "type": "boolean"
          },
          "market": {
            "$ref": "#/components/schemas/public_market"
          },
          "next_market_close": {
            "description": "Next market close timestamp",
            "format": "date-time",
            "type": "string"
          },
          "next_market_open": {
            "description": "Next market open timestamp",
            "format": "date-time",
            "type": "string"
          },
          "phase": {
            "$ref": "#/components/schemas/phase"
          },
          "phase_until": {
            "description": "The end of the current phase.",
            "format": "date-time",
            "type": "string"
          },
          "timestamp": {
            "description": "The time on the clock.",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "market",
          "timestamp",
          "is_market_day",
          "next_market_open",
          "next_market_close",
          "phase",
          "phase_until"
        ],
        "type": "object"
      },
      "clock_resp": {
        "description": "Clock response.",
        "properties": {
          "clocks": {
            "items": {
              "$ref": "#/components/schemas/clock"
            },
            "type": "array"
          }
        },
        "required": [
          "clocks"
        ],
        "type": "object"
      },
      "market_acronym": {
        "description": "The acronym of the market.",
        "example": "NYSE",
        "type": "string"
      },
      "market_name": {
        "description": "The full name of the market.",
        "example": "New York Stock Exchange",
        "type": "string"
      },
      "market_timezone": {
        "description": "The timezone of the market.",
        "example": "America/New_York",
        "type": "string"
      },
      "mic": {
        "description": "Market identifier code (ISO 10383).",
        "example": "XNYS",
        "maxLength": 4,
        "minLength": 4,
        "pattern": "^[A-Z0-9]{4}$",
        "type": "string"
      },
      "phase": {
        "enum": [
          "closed",
          "pre",
          "core",
          "lunch",
          "post"
        ],
        "type": "string"
      },
      "public_market": {
        "description": "A market.",
        "properties": {
          "acronym": {
            "$ref": "#/components/schemas/market_acronym"
          },
          "bic": {
            "$ref": "#/components/schemas/bic"
          },
          "mic": {
            "$ref": "#/components/schemas/mic"
          },
          "name": {
            "$ref": "#/components/schemas/market_name"
          },
          "timezone": {
            "$ref": "#/components/schemas/market_timezone"
          }
        },
        "required": [
          "acronym",
          "name",
          "timezone"
        ],
        "type": "object"
      }
    },
    "securitySchemes": {
      "BasicAuth": {
        "scheme": "basic",
        "type": "http"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Open brokerage accounts, enable stock, options and crypto trading. Manage the ongoing user experience and brokerage customer lifecycle with the Alpaca Broker API",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Broker API",
    "version": "1.1.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v2/clock": {
      "get": {
        "description": "This API serves information about multiple markets: the current time, if it's a market day, the current phase of the market, etc.\n",
        "operationId": "Clock",
        "parameters": [
          {
            "$ref": "#/components/parameters/markets"
          },
          {
            "$ref": "#/components/parameters/time"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/clock_resp"
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
          "429": {
            "$ref": "#/components/responses/429"
          },
          "500": {
            "$ref": "#/components/responses/500"
          }
        },
        "summary": "Get Market Clock",
        "tags": [
          "Calendar"
        ]
      }
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ],
  "servers": [
    {
      "description": "Sandbox endpoint",
      "url": "https://broker-api.sandbox.alpaca.markets"
    },
    {
      "description": "Production endpoint",
      "url": "https://broker-api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Calendar"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```