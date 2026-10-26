# Get US corporates

Source: https://docs.alpaca.markets/us/reference/uscorporates-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get US corporates

Serves the list of US corporates available at Alpaca. The response is sorted by ISIN.

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
      "call_type": {
        "description": "The type of call on the bond refers to one of a variety of circumstances under which a callable bond may be called.",
        "enum": [
          "ordinary",
          "make_whole",
          "regulatory",
          "special"
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
      "day_count": {
        "description": "The day count convention used to calculate accrued interest.\n\n- `A/360`: calculates the daily interest using a 360-day year and then multiplies that by the actual number of days in each time period.\n- `A/365`: calculates the daily interest using a 365-day year and then multiplies that by the actual number of days in each time period.\n- `30/360`: calculates the daily interest using a 360-day year and then multiplies that by 30 (standardized month).\n- `30/365`: calculates the daily interest using a 365-day year and then multiplies that by 30 (standardized month).\n- `A/A`: calculates the daily interest using the actual number of days in the year and then multiplies that by the actual number of days in each time period.\n- `30E/360`: number of days equals to the actual number of days (for February). If the start date or the end date of the period is the 31st of a month, that date is set to the 30th. The number of days in a year is 360.\n- `B/252`: calculates the daily interest using a 252-business-day year and then multiplies that by the actual number of days in each time period.\n- `A/364`: calculates the daily interest using a 364-day year and then multiplies that by the actual number of days in each time period.\n",
        "enum": [
          "A/360",
          "A/365",
          "30/360",
          "30/365",
          "A/A",
          "30E/360",
          "B/252",
          "A/364"
        ],
        "type": "string"
      },
      "sp_outlook": {
        "description": "A Standard & Poor's rating outlook indicates S&P's view regarding the potential direction of a long-term credit rating over the intermediate term (2 years for investment grade, 1 year for speculative grade)",
        "enum": [
          "positive",
          "negative",
          "developing",
          "stable",
          "not_rated",
          "not_meaningful"
        ],
        "type": "string"
      },
      "us_corporate": {
        "description": "A US corporate",
        "properties": {
          "accrued_interest": {
            "description": "The interest that has accumulated on a bond in dollars per bond between the last interest payment and the present date that has not yet been paid to the bondholder",
            "format": "double",
            "type": "number"
          },
          "bond_status": {
            "$ref": "#/components/schemas/bond_status"
          },
          "call_type": {
            "$ref": "#/components/schemas/call_type"
          },
          "callable": {
            "description": "Whether the bond is callable, meaning the issuer has the right, but not the obligation to redeem the bond - in other words, pay out the bondholder - before its maturity date at a set price (the call price)",
            "type": "boolean"
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
          "convertible": {
            "description": "A flag indicating whether the bond is convertible",
            "type": "boolean"
          },
          "country_domicile": {
            "description": "The country where the corporate is domiciled in the 2-alpha country code format (e.g., US, CA)",
            "type": "string"
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
          "dated_date": {
            "description": "The dated date marks the beginning of the period for which interest starts accruing on the bond",
            "format": "date",
            "type": "string"
          },
          "day_count": {
            "$ref": "#/components/schemas/day_count"
          },
          "description": {
            "description": "Description of the corporate bond",
            "type": "string"
          },
          "description_short": {
            "description": "Short description of the corporate bond",
            "type": "string"
          },
          "first_coupon_date": {
            "description": "The date of the first coupon payment",
            "format": "date",
            "type": "string"
          },
          "fractionable": {
            "description": "Whether the corporate can be traded in fractional amounts",
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
          "issue_minimum_denomination": {
            "description": "The smallest unit of the bond that can be purchased at its initial offering",
            "type": "number"
          },
          "issue_price": {
            "description": "The price at which the bond was originally issued as a percentage of par value",
            "format": "double",
            "type": "number"
          },
          "issue_size": {
            "description": "The total size amount of the bond issue in the issuing currency",
            "type": "number"
          },
          "issuer": {
            "description": "The name of the issuer of the corporate bond",
            "type": "string"
          },
          "last_coupon_date": {
            "description": "The date of the last coupon payment",
            "format": "date",
            "type": "string"
          },
          "liquidity_institutional_aggregate": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to buy or sell (no minimum trading sizes)",
            "type": "number"
          },
          "liquidity_institutional_buy": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to buy (no minimum trading sizes)",
            "type": "number"
          },
          "liquidity_institutional_sell": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to sell (no minimum trading sizes)",
            "type": "number"
          },
          "liquidity_micro_aggregate": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to buy or sell with minimum trading sizes less than or equal to $1,000.00",
            "type": "number"
          },
          "liquidity_micro_buy": {
            "description": "Score (from 1-5 if the bond is priced, or null if the bond is not tradable) reflecting the historical depth of executable liquidity to buy with minimum trading sizes less than or equal to $1,000.00",
            "type": "number"
          },
          "liquidity_micro_sell": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to sell with minimum trading sizes less than or equal to $1,000.00",
            "type": "number"
          },
          "liquidity_retail_aggregate": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to buy or sell with minimum trading sizes less than or equal to 10,000",
            "type": "number"
          },
          "liquidity_retail_buy": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to buy with minimum trading sizes less than or equal to $10,000.00",
            "type": "number"
          },
          "liquidity_retail_sell": {
            "description": "Score (from 1-5 or null if the bond is not priced/tradable) reflecting the historical depth of executable liquidity to sell with minimum trading sizes less than or equal to 10,000",
            "type": "number"
          },
          "marginable": {
            "description": "Whether the corporate is marginable",
            "type": "boolean"
          },
          "maturity_date": {
            "description": "The date on which the bond matures",
            "format": "date",
            "type": "string"
          },
          "next_call_date": {
            "description": "The date of the next possible call on the bond.",
            "format": "date",
            "type": "string"
          },
          "next_call_price": {
            "description": "The price at which a callable bond can be redeemed by the issuer on the next call date, as a percentage of par.",
            "format": "double",
            "type": "number"
          },
          "next_coupon_date": {
            "description": "The date of the next coupon payment",
            "format": "date",
            "type": "string"
          },
          "par_value": {
            "description": "The amount that the issuer of the bond will pay back to the bondholder upon maturity",
            "type": "number"
          },
          "perpetual": {
            "description": "A flag representing whether a bond is perpetual",
            "type": "boolean"
          },
          "puttable": {
            "description": "Whether the bond is puttable, meaning the bondholder has the right, but not the obligation to sell the bond back to the issuer at a set price (the put price) on specified dates before maturity",
            "type": "boolean"
          },
          "reg_s": {
            "description": "Indicates whether the security falls under Regulation S, a rule that provides an exemption from the registration requirements for securities offerings made outside the United States",
            "type": "boolean"
          },
          "reissue_date": {
            "description": "The date on which the corporate was reissued",
            "format": "date",
            "type": "string"
          },
          "reissue_price": {
            "description": "The price at which the corporate was reissued as a percentage of par value",
            "format": "double",
            "type": "number"
          },
          "reissue_size": {
            "description": "The total size amount of the corporate reissue in the issuing currency",
            "type": "number"
          },
          "sector": {
            "description": "The sector of the corporate bond",
            "type": "string"
          },
          "seniority": {
            "description": "The seniority of the corporate bond",
            "type": "string"
          },
          "sp_creditwatch": {
            "description": "S&P's CreditWatch highlights S&P's opinion regarding the potential direction of a short-term or long-term rating",
            "type": "string"
          },
          "sp_creditwatch_date": {
            "description": "The date of the most recent Standard & Poor's CreditWatch for the bond in YYYY-MM-DD format",
            "format": "date",
            "type": "string"
          },
          "sp_outlook": {
            "$ref": "#/components/schemas/sp_outlook"
          },
          "sp_outlook_date": {
            "description": "The date of the most recent Standard & Poor's outlook for the bond in YYYY-MM-DD format",
            "format": "date",
            "type": "string"
          },
          "sp_rating": {
            "description": "Standard & Poor's rating for the bond in the standard AAA - D format",
            "type": "string"
          },
          "sp_rating_date": {
            "description": "The date in the timezone of the issuing country of the most recent Standard & Poor's rating for the bond in YYYY-MM-DD format",
            "format": "date",
            "type": "string"
          },
          "ticker": {
            "description": "The ticker symbol of the corporate",
            "type": "string"
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
          "marginable",
          "fractionable",
          "issue_date",
          "country_domicile",
          "ticker",
          "seniority",
          "issuer",
          "sector",
          "description",
          "description_short",
          "coupon",
          "coupon_type",
          "coupon_frequency",
          "perpetual",
          "day_count",
          "dated_date",
          "issue_size",
          "issue_price",
          "issue_minimum_denomination",
          "par_value",
          "callable",
          "puttable",
          "convertible",
          "reg_s"
        ],
        "type": "object"
      },
      "us_corporates_resp": {
        "properties": {
          "us_corporates": {
            "items": {
              "$ref": "#/components/schemas/us_corporate"
            },
            "type": "array"
          }
        },
        "required": [
          "us_corporates"
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
    "/v1/assets/fixed_income/us_corporates": {
      "get": {
        "description": "Serves the list of US corporates available at Alpaca. The response is sorted by ISIN.",
        "operationId": "UsCorporates",
        "parameters": [
          {
            "in": "query",
            "name": "bond_status",
            "schema": {
              "$ref": "#/components/schemas/bond_status"
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
            "description": "A comma-separated list of tickers with a limit of 1000.",
            "example": "BAC,MSFT",
            "in": "query",
            "name": "tickers",
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
                  "$ref": "#/components/schemas/us_corporates_resp"
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
        "summary": "Get US corporates",
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