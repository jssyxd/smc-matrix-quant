# List FPSL Loans

Source: https://docs.alpaca.markets/us/reference/get-v1-list-fpsl-loans.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List FPSL Loans

Returns a list of all FPSL loans that match the specified filter criteria, ordered in ascending order by `date`, `account_number`, and `symbol`. Each entry represents a loan of a `symbol` on a given `date`, made on behalf of the specified `account_number`.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "FPSLError": {
        "description": "FPSL API error response",
        "properties": {
          "message": {
            "example": "Internal Server Error",
            "type": "string"
          }
        },
        "type": "object"
      },
      "FPSLInterest": {
        "description": "The interest's details.\nPlease note that the object might not be set if interest has not yet been calculated for the loan.\nAdditionally, interest details may be adjusted retroactively at any time until interests are finalized for the month.\nThe loan's changed `updated_at` field can indicate such an adjustment.\n",
        "properties": {
          "customer": {
            "description": "The interest accrued by the customer for this loan.",
            "example": 1.23,
            "format": "double",
            "type": "number"
          },
          "partner": {
            "description": "The interest accrued by the partner for this loan.",
            "example": 1.65,
            "format": "double",
            "type": "number"
          }
        },
        "required": [
          "customer",
          "partner"
        ],
        "type": "object"
      },
      "FPSLLoan": {
        "description": "A loan of a security by an account on a date.",
        "properties": {
          "account_id": {
            "description": "Account's ID at Alpaca",
            "example": "06d83e79-5bea-4ce9-a362-a25251a700ec",
            "type": "string"
          },
          "account_number": {
            "description": "Account's number at Alpaca",
            "example": "286873545",
            "type": "string"
          },
          "collateral": {
            "description": "The collateral posted for the loan.",
            "example": 1161.015,
            "format": "double",
            "type": "number"
          },
          "correspondent": {
            "description": "Account's correspondent",
            "example": "LPCA",
            "type": "string"
          },
          "date": {
            "example": "2006-01-02",
            "format": "date",
            "type": "string"
          },
          "interest": {
            "$ref": "#/components/schemas/FPSLInterest"
          },
          "market_value": {
            "description": "The total market value of the shares on loan.",
            "example": 1138.25,
            "format": "double",
            "type": "number"
          },
          "quantity": {
            "description": "The number of shares in the loan. This may be less than the total number of eligible shares held by the account.",
            "example": 5,
            "format": "int64",
            "type": "integer"
          },
          "symbol": {
            "description": "Stock/Ticker symbol of a stock or security",
            "example": "AAPL",
            "type": "string"
          },
          "updated_at": {
            "description": "Timestamp of the last update to this loan in RFC-3339 format with microsecond precision with timezone.\nAn updated value may indicate adjusted interest values.\n",
            "example": "2025-03-21T15:54:19.857034+01:00",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "date",
          "account_id",
          "account_number",
          "correspondent",
          "symbol",
          "quantity",
          "market_value",
          "collateral"
        ],
        "type": "object"
      },
      "ListFPSLLoansResponse": {
        "description": "Response to a successful request for a list of FPSL loans.\n",
        "properties": {
          "loans": {
            "description": "All FPSL loans matching the filter criteria",
            "items": {
              "$ref": "#/components/schemas/FPSLLoan"
            },
            "type": "array"
          },
          "next_page_token": {
            "description": "The token to use to retrieve the next page of results. If `null`, there are no more pages.\n",
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [
          "loans",
          "next_page_token"
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
    "/v1/fpsl/loans": {
      "get": {
        "description": "Returns a list of all FPSL loans that match the specified filter criteria, ordered in ascending order by `date`, `account_number`, and `symbol`. Each entry represents a loan of a `symbol` on a given `date`, made on behalf of the specified `account_number`.",
        "operationId": "get-v1-list-fpsl-loans",
        "parameters": [
          {
            "description": "The account identifier",
            "in": "query",
            "name": "account_id",
            "required": false,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "Filter loans after or on this start date.",
            "in": "query",
            "name": "start",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Filter loans before this end date.",
            "in": "query",
            "name": "end",
            "required": false,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "The pagination token used to continue retrieving results. This value is returned in certain responses when additional data is available, typically due to a response size limit.",
            "in": "query",
            "name": "page_token",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The maximum number of data points to return in the response page.",
            "in": "query",
            "name": "limit",
            "required": false,
            "schema": {
              "default": 1000,
              "maximum": 10000,
              "minimum": 1,
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ListFPSLLoansResponse"
                }
              }
            },
            "description": "Returns a list of FPSL loans for the account, or an empty list if no loans are found."
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FPSLError"
                }
              }
            },
            "description": "One of the request parameters is invalid. See the returned message for details."
          },
          "401": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FPSLError"
                }
              }
            },
            "description": "Authentication headers are missing or invalid. Make sure you authenticate your request with a valid API key."
          },
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FPSLError"
                }
              }
            },
            "description": "User has no access to a resource."
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FPSLError"
                }
              }
            },
            "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on Slack or on the Community Forum."
          }
        },
        "summary": "List FPSL Loans",
        "tags": [
          "FPSL Program"
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
      "name": "FPSL Program"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```