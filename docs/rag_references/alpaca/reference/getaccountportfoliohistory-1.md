# Get Account Portfolio History

Source: https://docs.alpaca.markets/us/reference/getaccountportfoliohistory-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Account Portfolio History

Returns timeseries data about equity and profit/loss (P/L) of the account in requested timespan.

# Usage for equity-traders

By default, for `timeframes` less than 1D,  the API returns the data points during market open times, to change this behavior the `intraday_reporting` query can be set to `extended_hours`, to include the premarket and after-hours trading prices.

# Usage for crypto-traders

The API can be used both for crypto and equities trading accounts. By default the API is aiming at the equities trading use-case, however, it can be configured to return data more suited for visualizing crypto portfolios.

For crypto, we recommend setting the following flags:

* `intraday_reporting=continuous`  so that 24/7 graphs are returned
* `pnl_reset=no_reset` so that the Profit And Loss calculation is continuous over the given period of time.

The `timeframe` can only be set to less than 1 day, when the requested `period` is less than  30 days.

# Profit and loss calculation

For profit and loss calculation we are using simple profit and loss to calculate the pnl percentage for a given time:

`pnl_pct = equity/base_value-1`

`base_value` and `base_value_asof` typically corresponds to the first available datapoint and timestamp unless the first data point reflects a zero (0) value. Portfolio value may be zero if the account is new or is not funded as of the beginning of the time period reflected in the chart. If `base_value_asof` is omitted from the response, there are no non-zero values and portfolio has no value for the duration of the requested chart.

# Notes

When `intraday_reporting=continuous`, equity calculations are based on the following prices:

* Between 4:00am and 10:00pm on trading days the valuation will be calculated based on the last trade (extended hours and normal hours respectively).
* After 10:00pm, until the next session open the equities will be valued at their official closing price on the primary exchange.

When `timeframe=1D`, `intraday_reporting` has no effect and the response will only contain entries for days when the market is open.

All the cash values returned to two digits. All percentage values are rounded to 4 digits.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "PortfolioHistory": {
        "description": "Timeseries data for equity and profit loss information of the account.",
        "properties": {
          "base_value": {
            "description": "basis in dollar of the profit loss calculation",
            "type": [
              "number",
              "null"
            ]
          },
          "base_value_asof": {
            "description": "If included, then it indicates that the base_value is the account's closing\nequity value at this trading date.\n\nIf not specified, then the baseline calculation is done against the earliest returned data item. This could happen for\naccounts without prior closing balances (e.g. new account) or for queries with 1D timeframes, where the first data point\nis used as a reference point.\n",
            "example": "2023-10-20",
            "format": "date",
            "type": "string"
          },
          "cashflow": {
            "additionalProperties": {
              "items": {
                "type": "number"
              },
              "type": "array"
            },
            "description": "accumulated value in dollar amount as of the end of each time window",
            "type": "object"
          },
          "equity": {
            "description": "equity value of the account in dollar amount as of the end of each time window",
            "items": {
              "type": [
                "number",
                "null"
              ]
            },
            "type": "array"
          },
          "profit_loss": {
            "description": "profit/loss in dollar from the base value",
            "items": {
              "type": [
                "number",
                "null"
              ]
            },
            "type": "array"
          },
          "profit_loss_pct": {
            "description": "profit/loss in percentage from the base value",
            "example": [
              0.001,
              0.002
            ],
            "items": {
              "type": [
                "number",
                "null"
              ]
            },
            "type": "array"
          },
          "timeframe": {
            "description": "time window size of each data element",
            "example": "15Min",
            "type": "string"
          },
          "timestamp": {
            "description": "Time of each data element, left-labeled (the beginning of time window).\n\nThe values returned are in [UNIX epoch format](https://en.wikipedia.org/wiki/Unix_time).\n",
            "items": {
              "type": "integer"
            },
            "type": "array"
          }
        },
        "required": [
          "timestamp",
          "equity",
          "profit_loss",
          "profit_loss_pct",
          "base_value",
          "timeframe"
        ],
        "title": "PortfolioHistory",
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
    "/v2/account/portfolio/history": {
      "get": {
        "description": "Returns timeseries data about equity and profit/loss (P/L) of the account in requested timespan.",
        "operationId": "getAccountPortfolioHistory",
        "parameters": [
          {
            "description": "The duration of the data in `number` + `unit` format, such as 1D, where `unit` can be D for day, W for week, M for month and A for year. Defaults to 1M.\n\nOnly two of `start`, `end` and `period` can be specified at the same time.\n\nFor intraday timeframes (\\<1D) only 30 days or less can be queried, for 1D resolutions there is no such limit, data is available since the\ncreation of the account.\n",
            "in": "query",
            "name": "period",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The resolution of time window. 1Min, 5Min, 15Min, 1H, or 1D. If omitted, 1Min for less than 7 days period,\n15Min for less than 30 days, or otherwise 1D.\n\nFor queries with longer than 30 days of `period`, the system only accepts 1D as `timeframe`.\n",
            "in": "query",
            "name": "timeframe",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "For intraday resolutions (<1D) this specifies which timestamps to return data points for:\n\nAllowed values are:\n- **market_hours**\n\n  Only timestamps for the core equity trading hours are returned (usually 9:30am to 4:00pm, trading days only)\n\n- **extended_hours**\n\n  Returns timestamps for the whole session including extended hours (usually 4:00am to 8:00pm, trading days only)\n\n- **continuous**\n\n  Returns price data points 24/7 (for off-session times too). To calculate the equity values we are using the following prices:\n\n  Between 4:00am and 10:00pm on trading days the valuation will be calculated based on the last trade (extended hours and normal hours respectively).\n\n  After 10:00pm, until the next session open the equities will be valued at their official closing price on the primary exchange.\n",
            "in": "query",
            "name": "intraday_reporting",
            "schema": {
              "default": "market_hours",
              "enum": [
                "market_hours",
                "extended_hours",
                "continuous"
              ],
              "type": "string"
            }
          },
          {
            "description": "The timestamp the data is returned starting from in RFC3339 format (including timezone specification). Defaults to `end` minus `period`\n\nIf provided, the `start` value is always normalized to the `America/New_York` timezone and adjusted to the nearest `timeframe` interval, e.g. seconds are always truncated and the time is rounded backwards to the nearest interval of `1Min`, `5Min`, `15Min`, or `1H`.\n\nIf `timeframe=1D` and `start` is not a valid trading date, find the next available trading date. For example, if `start` occurs on Saturday or Sunday after converting to the America/New_York timezone, `start` is adjusted to the first weekday that is not a market holiday (e.g. Monday).\n\nIf `timeframe` is less than `1D` and `intraday_reporting` is not `continuous`, `start` always reflects the beginning of a market session. If `start` is between midnight and the end (inclusive) of an active trading day, `start` is set to the beginning of the session on the specified day. Otherwise, if `start` occurs outside of the market session, the next available market date is used.\n\nFor example, when `intraday_reporting=market_hours` and `start=2023-10-19T23:59:59-04:00`, the provided `start` date occurs outside of the regular market session. The effective `start` timestamp is adjusted to the beginning of the next session: `2023-10-20T09:30:00-04:00`\n\n`start` may be be combined with one of `end` or `period`.\n\nProviding all of `start`, `end`, and `period` is invalid.\n",
            "in": "query",
            "name": "start",
            "schema": {
              "example": "2021-03-16T18:38:01Z",
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "`pnl_reset` defines how we are calculating the baseline values for Profit And Loss (pnl) for queries with `timeframe` less than 1D (intraday queries).\n\nThe default behavior for intraday queries is that we reset the pnl value to the previous day's closing equity for each **trading** day.\n\nIn case of crypto (given its continuous nature), this might not be desired: specifying \"no_reset\" disables this behavior and all pnl values\nreturned will be relative to the closing equity of the previous trading day.\n\nFor 1D resolution all PnL values are calculated relative to the `base_value`, we are not resetting the base value.\n",
            "in": "query",
            "name": "pnl_reset",
            "schema": {
              "default": "per_day",
              "enum": [
                "no_reset",
                "per_day"
              ],
              "type": "string"
            }
          },
          {
            "description": "The timestamp the data is returned up to in RFC3339 format (including timezone specification). Defaults to the current time.\n\nIf provided, the `end` value is always normalized to the `America/New_York` timezone and adjusted to the nearest `timeframe` interval, e.g. seconds are always truncated and the time is rounded backwards to the nearest interval of `1Min`, `5Min`, `15Min`, or `1H`.\n\nWhen `intraday_reporting` is either `market_hours` or `extended_hours`, the `end` value is adjusted to not occur after session close on the specified day. For example if the `intraday_reporting` is `extended_hours`, and the timestamp specified is `2023-10-19T21:33:00-04:00`, `end` is adjusted to `2023-10-19T20:00:00-04:00`.\n\n`end` may be combined with `start` or `period`.\n\nProviding all of `start`, `end`, and `period` is invalid.\n",
            "in": "query",
            "name": "end",
            "schema": {
              "example": "2021-03-16T18:38:01Z",
              "format": "date-time",
              "type": "string"
            }
          },
          {
            "description": "**deprecated**: Users are strongly advised to **rely on the `intraday_reporting` query parameter** for better control\nof the reporting range.\n\nIf true, include extended hours in the result. This is effective only for timeframe less than 1D.\n",
            "in": "query",
            "name": "extended_hours",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The cashflow activities to include in the report. One of 'ALL', 'NONE', or a comma-separated list of activity types.",
            "examples": {
              "all": {
                "value": "ALL"
              },
              "cash_transfers": {
                "summary": "Include cash movements.",
                "value": "JNLC,CSD,CSW"
              },
              "none": {
                "value": "NONE"
              }
            },
            "in": "query",
            "name": "cashflow_types",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "example-cashflows": {
                    "value": {
                      "base_value": 8413.04,
                      "base_value_asof": "2026-04-06",
                      "cashflow": {
                        "CSD": [
                          9.93,
                          10.13,
                          10.16,
                          0
                        ],
                        "DIV": [
                          0,
                          0,
                          0.63,
                          0
                        ]
                      },
                      "equity": [
                        8425.21,
                        8639.77,
                        8766.1,
                        8835.31
                      ],
                      "profit_loss": [
                        12.17,
                        214.56,
                        126.33,
                        69.21
                      ],
                      "profit_loss_pct": [
                        0.0014,
                        0.0255,
                        0.0146,
                        0.0079
                      ],
                      "timeframe": "1D",
                      "timestamp": [
                        1775606400,
                        1775692800,
                        1775779200,
                        1775865600
                      ]
                    }
                  },
                  "example-intraday-query-15min-1d": {
                    "value": {
                      "base_value": 2774.16,
                      "base_value_asof": "2023-10-18",
                      "cashflow": {
                        "CSD": [
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          100,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0
                        ]
                      },
                      "equity": [
                        2773.79,
                        2769.04,
                        2768.65,
                        2765.11,
                        2763.03,
                        2763.17,
                        2763.17,
                        2763.47,
                        2763.91,
                        2768.13,
                        2774.98,
                        2757.94,
                        2757.65,
                        2774.54,
                        2775.58,
                        2775.28,
                        2767.9,
                        2762.26,
                        2762.56,
                        2756.99,
                        2756.84,
                        2752.43,
                        2752.13,
                        2748.44,
                        2751.23,
                        2747.54,
                        2748.74
                      ],
                      "profit_loss": [
                        -0.37,
                        -5.12,
                        -5.51,
                        -9.05,
                        -11.13,
                        -10.99,
                        -10.99,
                        -10.69,
                        -10.25,
                        -6.03,
                        0.82,
                        -16.22,
                        -16.51,
                        0.38,
                        1.42,
                        1.12,
                        -6.26,
                        -11.9,
                        -11.6,
                        -17.17,
                        -17.32,
                        -21.73,
                        -22.03,
                        -25.72,
                        -22.93,
                        -26.62,
                        -25.42
                      ],
                      "profit_loss_pct": [
                        -0.0001,
                        -0.0018,
                        -0.002,
                        -0.0033,
                        -0.004,
                        -0.004,
                        -0.004,
                        -0.0039,
                        -0.0037,
                        -0.0022,
                        0.0003,
                        -0.0058,
                        -0.006,
                        0.0001,
                        0.0005,
                        0.0004,
                        -0.0023,
                        -0.0043,
                        -0.0042,
                        -0.0062,
                        -0.0062,
                        -0.0078,
                        -0.0079,
                        -0.0093,
                        -0.0083,
                        -0.0096,
                        -0.0092
                      ],
                      "timeframe": "15Min",
                      "timestamp": [
                        1697722200,
                        1697723100,
                        1697724000,
                        1697724900,
                        1697725800,
                        1697726700,
                        1697727600,
                        1697728500,
                        1697729400,
                        1697730300,
                        1697731200,
                        1697732100,
                        1697733000,
                        1697733900,
                        1697734800,
                        1697735700,
                        1697736600,
                        1697737500,
                        1697738400,
                        1697739300,
                        1697740200,
                        1697741100,
                        1697742000,
                        1697742900,
                        1697743800,
                        1697744700,
                        1697745600
                      ]
                    }
                  },
                  "example-query-1d-7d": {
                    "value": {
                      "base_value": 2784.79,
                      "cashflow": {
                        "CSD": [
                          0,
                          0,
                          100,
                          0,
                          0
                        ]
                      },
                      "equity": [
                        2784.79,
                        2794.79,
                        2805.46,
                        2774.16,
                        2748.73
                      ],
                      "profit_loss": [
                        0,
                        10.0022,
                        10.6692,
                        -31.2996,
                        -25.4232
                      ],
                      "profit_loss_pct": [
                        0,
                        0.0035,
                        0.0074,
                        -0.0038,
                        -0.0129
                      ],
                      "timeframe": "1D",
                      "timestamp": [
                        1697241600,
                        1697500800,
                        1697587200,
                        1697673600,
                        1697760000
                      ]
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/PortfolioHistory"
                }
              }
            },
            "description": "Successful response"
          }
        },
        "summary": "Get Account Portfolio History",
        "tags": [
          "Portfolio History"
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
      "name": "Portfolio History"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```