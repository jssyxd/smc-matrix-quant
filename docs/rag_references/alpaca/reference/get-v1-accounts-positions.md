# Bulk Fetch All Accounts Positions

Source: https://docs.alpaca.markets/us/reference/get-v1-accounts-positions.md

---
updatedAt: 2026-05-27T17:58:38.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Bulk Fetch All Accounts Positions

Retrieves a list of the account's open positions.
This endpoint is deprecated and will be removed in the future. Please use the [GET /v1/reporting/eod/positions endpoint](https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions) instead.


# OpenAPI definition

```json
{
  "components": {
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
    "/v1/accounts/positions": {
      "get": {
        "deprecated": true,
        "description": "Retrieves a list of the account's open positions.\nThis endpoint is deprecated and will be removed in the future. Please use the [GET /v1/reporting/eod/positions endpoint](https://docs.alpaca.markets/reference/get-v1-reporting-eod-positions) instead.\n",
        "operationId": "get-v1-accounts-positions",
        "parameters": [
          {
            "description": "The number of the page of the results to be fetched.",
            "in": "query",
            "name": "page",
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "Example 1": {
                    "value": {
                      "as_of": "2022-08-04T16:00:00-04:00",
                      "positions": {
                        "000c8a47-7487-430b-94e1-e628a71cd123": [
                          {
                            "asset_class": "us_equity",
                            "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                            "asset_marginable": true,
                            "avg_entry_price": "172.34",
                            "change_today": "0",
                            "cost_basis": "13.63999992516",
                            "current_price": "166.13",
                            "exchange": "NASDAQ",
                            "lastday_price": "166.13",
                            "market_value": "13.14850404762",
                            "qty": "0.079145874",
                            "qty_available": "0.079145874",
                            "side": "long",
                            "symbol": "AAPL",
                            "unrealized_intraday_pl": "0",
                            "unrealized_intraday_plpc": "0",
                            "unrealized_pl": "-0.49149587754",
                            "unrealized_plpc": "-0.0360334223047464"
                          }
                        ]
                      }
                    }
                  }
                },
                "schema": {
                  "properties": {
                    "as_of": {
                      "format": "date-time",
                      "type": "string"
                    },
                    "positions": {
                      "type": "object"
                    }
                  },
                  "type": "object"
                }
              }
            },
            "description": "The response contains two fields:\n\nasof: the timestamp for which the positions are returned. It is always the last market close\n\npositions: an account-id to position list map, contains the requested page's accounts\nThe positions map is empty for the last page.\n\nNote: when fetching bulk positions, which can take multiple minutes depending on the number of accounts managed have, a market close can happen, and after that a new set of results might be returned. To make sure results are consistent, please always check that the as_of field didn't change during the whole fetching process."
          }
        },
        "summary": "Bulk Fetch All Accounts Positions",
        "tags": [
          "Trading"
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
      "name": "Trading"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```