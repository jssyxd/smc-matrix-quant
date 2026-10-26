# Get US Market Calendar

Source: https://docs.alpaca.markets/us/reference/legacycalendar.md

---
updatedAt: 2026-04-20T20:39:16.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get US Market Calendar

The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.


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
      "legacy_date_type": {
        "description": "Indicates what start and end mean. Default: TRADING. If TRADING is specified, returns a calendar whose trading date matches start, end. If SETTLEMENT is specified, returns the calendar whose settlement date matches start and end.\n",
        "in": "query",
        "name": "date_type",
        "schema": {
          "enum": [
            "TRADING",
            "SETTLEMENT"
          ],
          "type": "string"
        }
      },
      "legacy_end": {
        "description": "The last date to retrieve data for (inclusive).",
        "in": "query",
        "name": "end",
        "schema": {
          "format": "date-time",
          "type": "string"
        }
      },
      "legacy_start": {
        "description": "The first date to retrieve data for (inclusive).",
        "in": "query",
        "name": "start",
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
      "legacy_calendar_day": {
        "description": "A calendar day.",
        "properties": {
          "close": {
            "description": "The time the market closes at on this date in HH:MM format.",
            "example": "16:00",
            "type": "string"
          },
          "date": {
            "description": "Date string in YYYY-MM-DD format.",
            "example": "2025-01-02",
            "format": "date",
            "type": "string"
          },
          "open": {
            "description": "The time the market opens at on this date in HH:MM format.",
            "example": "09:30",
            "type": "string"
          },
          "session_close": {
            "description": "The time the session closes at on this date in HHMM format.",
            "example": "2000",
            "type": "string"
          },
          "session_open": {
            "description": "The time the session opens at on this date in HHMM format.",
            "example": "0400",
            "type": "string"
          },
          "settlement_date": {
            "description": "Date string in YYYY-MM-DD format. Representing the settlement date for the trade date.",
            "example": "2025-01-03",
            "format": "date",
            "type": "string"
          }
        },
        "required": [
          "date",
          "open",
          "close",
          "session_open",
          "session_close",
          "settlement_date"
        ],
        "type": "object"
      },
      "legacy_public_calendar_resp": {
        "items": {
          "$ref": "#/components/schemas/legacy_calendar_day"
        },
        "type": "array"
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
    "/v2/calendar": {
      "get": {
        "description": "The calendar API serves the full list of market days from 1970 to 2029. It can also be queried by specifying a start and/or end time to narrow down the results. In addition to the dates, the response also contains the specific open and close times for the market days, taking into account early closures.\n",
        "operationId": "LegacyCalendar",
        "parameters": [
          {
            "$ref": "#/components/parameters/legacy_start"
          },
          {
            "$ref": "#/components/parameters/legacy_end"
          },
          {
            "$ref": "#/components/parameters/legacy_date_type"
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/legacy_public_calendar_resp"
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
        "summary": "Get US Market Calendar",
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