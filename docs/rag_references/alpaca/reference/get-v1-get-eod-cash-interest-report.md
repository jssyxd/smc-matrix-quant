# Retrieve EOD Cash Interest Details

Source: https://docs.alpaca.markets/us/reference/get-v1-get-eod-cash-interest-report.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve EOD Cash Interest Details

This API retrieves a list of cash interest details for the given date(s) for a single account or all accounts. End-of-day (EOD) details are typically accessible after 8:00pm Eastern Time (ET) and reflect that day's ending state across cash balances, accrued interest, accrued fees, as well as additional ancillary details.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "DailyCashInterest": {
        "properties": {
          "account_accrued_interest": {
            "example": "1.2152",
            "format": "decimal",
            "type": "string"
          },
          "account_id": {
            "example": "02e5c5ba-36d2-467a-8699-81dc24271291",
            "format": "uuid",
            "type": "string"
          },
          "account_rate_bps": {
            "example": 423,
            "type": "integer"
          },
          "apr_tier_id": {
            "example": "13d149c8-d620-43e0-978b-88af8abb2ef1",
            "format": "uuid",
            "type": "string"
          },
          "apr_tier_name": {
            "example": "gold",
            "type": "string"
          },
          "cash_balance": {
            "example": "10485.76",
            "format": "decimal",
            "type": "string"
          },
          "correspondent_fee": {
            "example": "0.0718",
            "format": "decimal",
            "type": "string"
          },
          "correspondent_rate_bps": {
            "example": 25,
            "type": "integer"
          },
          "currency": {
            "example": "USD",
            "type": "string"
          },
          "date": {
            "example": "2024-09-27",
            "format": "date",
            "type": "string"
          }
        },
        "type": "object"
      },
      "EoDCashInterestReportResponse": {
        "properties": {
          "interest": {
            "items": {
              "$ref": "#/components/schemas/DailyCashInterest"
            },
            "type": "array"
          },
          "next_page_token": {
            "example": "293639be-8807-423f-b00d-68c781e8bb56",
            "type": [
              "string",
              "null"
            ]
          }
        },
        "type": "object"
      },
      "Error": {
        "properties": {
          "code": {
            "type": "number"
          },
          "message": {
            "type": "string"
          }
        },
        "required": [
          "code",
          "message"
        ],
        "title": "Error",
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
    "/v1/reporting/eod/cash_interest": {
      "get": {
        "description": "This API retrieves a list of cash interest details for the given date(s) for a single account or all accounts. End-of-day (EOD) details are typically accessible after 8:00pm Eastern Time (ET) and reflect that day's ending state across cash balances, accrued interest, accrued fees, as well as additional ancillary details.",
        "operationId": "get-v1-get-eod-cash-interest-report",
        "parameters": [
          {
            "description": "Account globally unique identifier. If not provided, the report will be generated for all accounts.",
            "in": "query",
            "name": "account_id",
            "required": false,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "A date in the format YYYY-MM-DD. If not provided, the report will be generated for the most recent date this report is available.",
            "in": "query",
            "name": "date",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "A date in the format YYYY-MM-DD, valid only if account_id is provided and date is not provided. If not provided, this will use `before` value. If neither is provided the most recent available date is used for both `before` and `after`.",
            "in": "query",
            "name": "after",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "A date in the format YYYY-MM-DD, valid only if account_id is provided and date is not provided. If not provided, this will use the most recent available date.",
            "in": "query",
            "name": "before",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "The direction to use for sorting responses, either `asc` or `desc`. Only valid for account_id queries, for which only sorting by date is supported. Defaults to `desc`.",
            "in": "query",
            "name": "direction",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The page size, used for paginating responses. Defaults to 1000, with a maximum of 10,000.",
            "in": "query",
            "name": "page_size",
            "required": false,
            "schema": {
              "default": 1000,
              "maximum": 10000,
              "minimum": 1,
              "type": "integer"
            }
          },
          {
            "description": "A token used to retrieve the next page for paginated queries. If provided the response will begin at the next page of the results for the response from which the `next_page_token` is used.",
            "in": "query",
            "name": "page_token",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/EoDCashInterestReportResponse"
                }
              }
            },
            "description": "Successful response, returns a list of daily interest accruals and an optional next page token."
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "A client error occurred. Please check the provided request parameters and try again."
          },
          "401": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Unauthorized. Please check your API key and try again."
          },
          "429": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Too many requests. Please wait a moment and try again."
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "A server error occurred. Please contact Alpaca."
          }
        },
        "summary": "Retrieve EOD Cash Interest Details",
        "tags": [
          "Reporting",
          "Cash Interest"
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
      "name": "Reporting"
    },
    {
      "name": "Cash Interest"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```