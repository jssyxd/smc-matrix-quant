# Create Portfolio

Source: https://docs.alpaca.markets/us/reference/post-v1-rebalancing-portfolios.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create Portfolio

Creates a portfolio allocation containing securities and/or cash. Having no rebalancing conditions is allowed but the rebalance event would need to be triggered manually. Portfolios created with API may have multiple rebalance_conditions, but only one of type calendar.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "Portfolio": {
        "properties": {
          "cooldown_days": {
            "description": "Count of calendar days following a rebalance before a subscription is eligible to trigger another rebalance",
            "type": "integer"
          },
          "created_at": {
            "description": "Portfolio creation timestamp",
            "type": "string"
          },
          "description": {
            "description": "Text to describe portfolio",
            "type": "string"
          },
          "id": {
            "description": "Portfolio ID",
            "type": "string"
          },
          "name": {
            "description": "Name of portfolio",
            "type": "string"
          },
          "rebalancing_conditions": {
            "description": "Rebalancing conditions for portfolio",
            "type": "string"
          },
          "status": {
            "description": "Current status of portfolio",
            "enum": [
              "active",
              "inactive",
              "needs_adjustment"
            ],
            "type": "string"
          },
          "updated_at": {
            "description": "Portfolio updated timestamp",
            "type": "string"
          },
          "weights": {
            "description": "Weight configuration to portfolio. Sum of \"percent\" values in the weights array must be 100.00",
            "items": {
              "$ref": "#/components/schemas/PortfolioWeights"
            },
            "type": "array"
          }
        },
        "required": [
          "cooldown_days"
        ],
        "title": "Portfolio",
        "type": "object"
      },
      "PortfolioWeightRequest": {
        "oneOf": [
          {
            "properties": {
              "type": {
                "enum": [
                  "cash"
                ]
              }
            }
          },
          {
            "properties": {
              "symbol": {
                "type": "string"
              },
              "type": {
                "enum": [
                  "asset"
                ]
              }
            },
            "required": [
              "symbol"
            ]
          }
        ],
        "properties": {
          "percent": {
            "description": "Percentage allocated to this weight. Values must be greater than zero, and all supplied weights must total exactly 100.",
            "type": [
              "string",
              "number"
            ]
          },
          "symbol": {
            "description": "Asset symbol. Required and non-null when `type` is `asset`.",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "description": "Type of weight entry in a portfolio.",
            "enum": [
              "cash",
              "asset"
            ],
            "type": "string"
          }
        },
        "required": [
          "type",
          "percent"
        ],
        "title": "PortfolioWeightRequest",
        "type": "object"
      },
      "PortfolioWeights": {
        "properties": {
          "percent": {
            "description": "Percentage allocated to this weight as a decimal string.",
            "type": "string"
          },
          "symbol": {
            "description": "Asset symbol. `null` for cash weights. Always present.",
            "type": [
              "string",
              "null"
            ]
          },
          "type": {
            "description": "Type of weight entry in a portfolio.",
            "enum": [
              "cash",
              "asset"
            ],
            "type": "string"
          }
        },
        "required": [
          "type",
          "symbol",
          "percent"
        ],
        "title": "PortfolioWeights",
        "type": "object"
      },
      "RebalancingConditions": {
        "properties": {
          "day": {
            "description": "Used to specify the rebalancing day for conditions of type = calendar. Only permitted and required for type = calendar. In scenarios when the specified day aligns to a non-trading day, the rebalance will be triggered on the preceding trading day. For type= annually, the value must be passed in MM-DD format. If 02-29 is specified and the current year is not a leap year, the rebalance will occur on the trading day preceding 2/29. For type= quarterly and monthly the value must be an integer between 1 and 31 inclusive. This represents the day of month. For quarterly, rebalancing will trigger on this day in January, March, June, and December. If the specified day is non-existent for the month then the rebalancing will trigger on the preceding trading day. For type = weekly, permitted values are Monday, Tuesday, Wednesday, Thursday, Friday.",
            "type": "string"
          },
          "percent": {
            "description": "Must be a positive value, up to two decimal places. Only permitted and required for type = drift_band. This is the max allowable drift percent from any target weight (+/-)",
            "type": "string"
          },
          "sub_type": {
            "description": "For type = drift_band: absolute or relative. For type = calendar: weekly,monthly, quarterly or annually. For type = on_portfolio_update: there is no subtype",
            "type": "string"
          },
          "type": {
            "description": "Possible values of drift_band, calendar or on_portfolio_update",
            "type": "string"
          }
        },
        "title": "RebalancingConditions",
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
    "/v1/rebalancing/portfolios": {
      "post": {
        "description": "Creates a portfolio allocation containing securities and/or cash. Having no rebalancing conditions is allowed but the rebalance event would need to be triggered manually. Portfolios created with API may have multiple rebalance_conditions, but only one of type calendar.",
        "operationId": "post-v1-rebalancing-portfolios",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "cooldown_days": {
                    "description": "Count of calendar days following a rebalance before a subscription is eligible to trigger another rebalance",
                    "type": "integer"
                  },
                  "description": {
                    "description": "Text to describe portfolio",
                    "type": "string"
                  },
                  "name": {
                    "description": "Name of portfolio",
                    "type": "string"
                  },
                  "rebalance_conditions": {
                    "description": "Rebalancing conditions for portfolio",
                    "items": {
                      "$ref": "#/components/schemas/RebalancingConditions"
                    },
                    "type": "array"
                  },
                  "weights": {
                    "description": "Weight configuration to portfolio. Sum of \"percent\" values in the weights array must be 100.00",
                    "items": {
                      "$ref": "#/components/schemas/PortfolioWeightRequest"
                    },
                    "type": "array"
                  }
                },
                "type": "object"
              }
            }
          },
          "description": ""
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Portfolio"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Create Portfolio",
        "tags": [
          "Rebalancing"
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
      "name": "Rebalancing"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```