# Get US treasuries

Source: https://docs.alpaca.markets/us/reference/ustreasuries-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get US treasuries

Serves the list of US treasuries available at Alpaca. The response is sorted by ISIN.

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
        "description": "Internal server error. We recommend retrying these later. If the issue persists, please contact us on Slack or on the Community Forum.\n"
      }
    },
    "schemas": {
      "bond_status": {
        "description": "Status of the bond.",
        "enum": [
          "outstanding",
          "matured",
          "pre_issuance"
        ],
        "type": "string"
      },
      "coupon_frequency": {
        "description": "How often the coupon is paid",
        "enum": [
          "annual",
          "semi_annual",
          "quarterly",
          "monthly",
          "zero"
        ],
        "type": "string"
      },
      "coupon_type": {
        "description": "The type of the coupon rate",
        "enum": [
          "fixed",
          "floating",
          "zero"
        ],
        "type": "string"
      },
      "treasury_subtype": {
        "description": "The subtype of the treasury.",
        "enum": [
          "bond",
          "bill",
          "note",
          "strips",
          "tips",
          "floating"
        ],
        "type": "string"
      },
      "us_treasuries_resp": {
        "properties": {
          "us_treasuries": {
            "items": {
              "$ref": "#/components/schemas/us_treasury"
            },
            "type": "array"
          }
        },
        "required": [
          "us_treasuries"
        ],
        "type": "object"
      },
      "us_treasury": {
        "description": "A US treasury",
        "properties": {
          "bond_status": {
            "$ref": "#/components/schemas/bond_status"
          },
          "close_price": {
            "description": "The price of the last transaction of a security before the market closes for normal trading, shown as a percentage of par value",
            "format": "double",
            "type": "number"
          },
          "close_price_date": {
            "description": "The date of the close price",
            "format": "date",
            "type": "string"
          },
          "close_yield_to_maturity": {
            "description": "Yield to maturity of the treasury after the last close",
            "format": "double",
            "type": "number"
          },
          "close_yield_to_worst": {
            "description": "Yield to worst of the treasury after the last close",
            "format": "double",
            "type": "number"
          },
          "coupon": {
            "description": "The annual interest rate paid on the bond as a percentage of par value",
            "format": "double",
            "type": "number"
          },
          "coupon_frequency": {
            "$ref": "#/components/schemas/coupon_frequency"
          },
          "coupon_type": {
            "$ref": "#/components/schemas/coupon_type"
          },
          "cusip": {
            "description": "CUSIP is a nine-character alphanumeric code that uniquely identifies the security",
            "maxLength": 9,
            "minLength": 9,
            "pattern": "^[A-Z0-9]{9}$",
            "type": "string"
          },
          "description": {
            "description": "Description of the treasury",
            "type": "string"
          },
          "description_short": {
            "description": "Short description of the treasury",
            "type": "string"
          },
          "first_coupon_date": {
            "description": "The date of the first coupon payment",
            "format": "date",
            "type": "string"
          },
          "fractionable": {
            "description": "Whether the treasury can be traded in fractional amounts",
            "type": "boolean"
          },
          "isin": {
            "description": "International Securities Identification Number",
            "maxLength": 12,
            "minLength": 12,
            "pattern": "^[A-Z]{2}[A-Z0-9]{9}[0-9]$",
            "type": "string"
          },
          "issue_date": {
            "description": "The date on which the bond was issued",
            "format": "date",
            "type": "string"
          },
          "last_coupon_date": {
            "description": "The date of the last coupon payment",
            "format": "date",
            "type": "string"
          },
          "maturity_date": {
            "description": "The date on which the bond matures",
            "format": "date",
            "type": "string"
          },
          "next_coupon_date": {
            "description": "The date of the next coupon payment",
            "format": "date",
            "type": "string"
          },
          "subtype": {
            "$ref": "#/components/schemas/treasury_subtype"
          },
          "tradable": {
            "description": "Whether the treasury is tradable",
            "type": "boolean"
          }
        },
        "required": [
          "isin",
          "cusip",
          "bond_status",
          "tradable",
          "fractionable",
          "subtype",
          "issue_date",
          "maturity_date",
          "description",
          "description_short",
          "coupon",
          "coupon_type",
          "coupon_frequency"
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
    "/v1/assets/fixed_income/us_treasuries": {
      "get": {
        "description": "Serves the list of US treasuries available at Alpaca. The response is sorted by ISIN.",
        "operationId": "UsTreasuries",
        "parameters": [
          {
            "in": "query",
            "name": "subtype",
            "schema": {
              "$ref": "#/components/schemas/treasury_subtype"
            }
          },
          {
            "in": "query",
            "name": "bond_status",
            "schema": {
              "$ref": "#/components/schemas/bond_status"
            }
          },
          {
            "description": "A comma-separated list of CUSIPs with a limit of 1000.",
            "example": "912810UG1,912797PM3",
            "in": "query",
            "name": "cusips",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "A comma-separated list of ISINs with a limit of 1000.",
            "example": "US912810UG12,US912797PM34",
            "in": "query",
            "name": "isins",
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
                  "$ref": "#/components/schemas/us_treasuries_resp"
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
        "summary": "Get US treasuries",
        "tags": [
          "Assets"
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
      "name": "Assets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```