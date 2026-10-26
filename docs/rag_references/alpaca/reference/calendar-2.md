# Get Market Calendar

Source: https://docs.alpaca.markets/us/reference/calendar-2.md

---
updatedAt: 2026-04-20T20:39:16.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Market Calendar

This endpoint returns the market calendar.

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
        "description": "The last date to retrieve data for (inclusive). Default: one week from the start date.\n",
        "example": "2030-01-01",
        "in": "query",
        "name": "end",
        "required": false,
        "schema": {
          "format": "date",
          "type": "string"
        }
      },
      "market": {
        "description": "The market identifier. MIC, BIC, or acronym.\n\nAvailable market codes by region:\n\n**United States**\n- `BMO`: Bank of Montreal. US banking calendar (US operations).\n- `BNYM`: The Bank of New York Mellon. US banking calendar.\n- `BOATS`: Blue Ocean Alternative Trading System. US overnight trading.\n- `IEX`: Investors Exchange. US equities.\n- `IEXG`: Investors Exchange. US equities.\n- `NASDAQ`: National Association of Securities Dealers Automated Quotations. US equities.\n- `NYSE`: New York Stock Exchange. US equities.\n- `OCEA`: BlueOcean ATS. US overnight trading.\n- `OPRA`: Options Price Reporting Authority. US options.\n- `OTC`: Over-The-Counter. US OTC equities.\n- `OTCM`: OTC Markets. US OTC equities.\n- `SIFMA`: Securities Industry and Financial Markets Association. US bonds.\n- `XNAS`: NASDAQ. US equities.\n- `XNYS`: New York Stock Exchange. US equities.\n\n**Europe**\n- `CEUX`: Cboe CEUX Europe. European equities (Cboe Netherlands).\n- `CHIX`: Cboe CHIX Europe. European equities (Cboe UK).\n- `ISE`: Euronext Dublin. Irish equities.\n- `LSE`: London Stock Exchange. UK equities.\n- `MTA`: Euronext Milan. Italian equities.\n- `MTAA`: Euronext Milan. Italian equities.\n- `XAMS`: Euronext Amsterdam. Dutch equities.\n- `XBRU`: Euronext Brussels. Belgian equities.\n- `XDUB`: Euronext Dublin. Irish equities.\n- `XETR`: Frankfurt Stock Exchange. German equities.\n- `XETRA`: Frankfurt Stock Exchange. German equities.\n- `XLIS`: Euronext Lisbon. Portuguese equities.\n- `XLON`: London Stock Exchange. UK equities.\n- `XPAR`: Euronext Paris. French equities.\n\n**Asia & Middle East**\n- `HKEX`: Hong Kong Stock Exchange. Hong Kong equities.\n- `JPX`: Japan Exchange Group. Japanese equities.\n- `TADAWUL`: Saudi Stock Exchange. Saudi equities.\n- `XHKG`: Hong Kong Stock Exchange. Hong Kong equities.\n- `XSAU`: Saudi Stock Exchange. Saudi equities.\n- `XTKS`: Japan Exchange Group. Japanese equities.\n",
        "in": "path",
        "name": "market",
        "required": true,
        "schema": {
          "$ref": "#/components/schemas/market"
        }
      },
      "start": {
        "description": "The first date to retrieve data for (inclusive). Default: today.\n",
        "example": "2025-01-01",
        "in": "query",
        "name": "start",
        "required": false,
        "schema": {
          "format": "date",
          "type": "string"
        }
      },
      "timezone": {
        "description": "Timezone of the times. Default: the timezone of the market.\n",
        "in": "query",
        "name": "timezone",
        "required": false,
        "schema": {
          "enum": [
            "UTC"
          ],
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
      "calendar_day": {
        "description": "A calendar day.",
        "properties": {
          "core_end": {
            "description": "The end time of the core market session.",
            "example": "2025-01-02T16:00:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "core_start": {
            "description": "The start time of the core market session.",
            "example": "2025-01-02T09:30:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "date": {
            "description": "The date of the calendar day.",
            "example": "2025-01-02",
            "format": "date",
            "type": "string"
          },
          "lunch_end": {
            "description": "The end time of the lunch session.",
            "format": "date-time",
            "type": "string"
          },
          "lunch_start": {
            "description": "The start time of the lunch session.",
            "format": "date-time",
            "type": "string"
          },
          "post_end": {
            "description": "The end time of the after-hours session.",
            "example": "2025-01-02T20:00:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "post_start": {
            "description": "The start time of the after-hours session.",
            "example": "2025-01-02T16:00:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "pre_end": {
            "description": "The end time of the pre-market session.",
            "example": "2025-01-02T09:30:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "pre_start": {
            "description": "The start time of the pre-market session.",
            "example": "2025-01-02T04:00:00-05:00",
            "format": "date-time",
            "type": "string"
          },
          "settlement_date": {
            "description": "The settlement date.",
            "example": "2025-01-03",
            "format": "date",
            "type": "string"
          }
        },
        "required": [
          "date",
          "core_start",
          "core_end"
        ],
        "type": "object"
      },
      "market": {
        "description": "The market identifier (MIC, BIC, or acronym).",
        "enum": [
          "BMO",
          "BNYM",
          "BOATS",
          "CEUX",
          "CHIX",
          "HKEX",
          "IEX",
          "IEXG",
          "ISE",
          "LSE",
          "MTA",
          "MTAA",
          "NASDAQ",
          "NYSE",
          "OCEA",
          "OPRA",
          "OTC",
          "OTCM",
          "SIFMA",
          "TADAWUL",
          "XAMS",
          "XBRU",
          "XDUB",
          "XETR",
          "XETRA",
          "XHKG",
          "XLIS",
          "XLON",
          "XNAS",
          "XNYS",
          "XPAR",
          "XSAU"
        ],
        "type": "string"
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
      "public_calendar_resp": {
        "description": "Calendar response.",
        "properties": {
          "calendar": {
            "description": "The market calendar.",
            "items": {
              "$ref": "#/components/schemas/calendar_day"
            },
            "type": "array"
          },
          "market": {
            "$ref": "#/components/schemas/public_market"
          }
        },
        "required": [
          "market",
          "calendar"
        ],
        "type": "object"
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
      "API_Key": {
        "description": "",
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "API_Secret": {
        "description": "",
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
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Trading API",
    "version": "2.0.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v3/calendar/{market}": {
      "get": {
        "description": "This endpoint returns the market calendar.",
        "operationId": "Calendar",
        "parameters": [
          {
            "$ref": "#/components/parameters/market"
          },
          {
            "$ref": "#/components/parameters/start"
          },
          {
            "$ref": "#/components/parameters/end"
          },
          {
            "$ref": "#/components/parameters/timezone"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/public_calendar_resp"
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
        "summary": "Get Market Calendar",
        "tags": [
          "Calendar"
        ]
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "servers": [
    {
      "description": "Paper",
      "url": "https://paper-api.alpaca.markets"
    },
    {
      "description": "Live",
      "url": "https://api.alpaca.markets"
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