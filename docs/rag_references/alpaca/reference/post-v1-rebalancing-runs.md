# Create Run

Source: https://docs.alpaca.markets/us/reference/post-v1-rebalancing-runs.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create Run

Creates a rebalance run.

Omit `weights` or provide an empty array to create a subscription-driven run using the account's active subscription. Provide a non-empty `weights` array to create a manual one-off run. A manual run is rejected if the account already has an active subscription.

The determination of a run's orders and the execution of a run take place during normal market hours. Runs can be initiated outside normal market hours but remain `QUEUED` until normal market hours.

Only one run in a non-terminal status is allowed at any time.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
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
    "/v1/rebalancing/runs": {
      "post": {
        "description": "Creates a rebalance run.\n\nOmit `weights` or provide an empty array to create a subscription-driven run using the account's active subscription. Provide a non-empty `weights` array to create a manual one-off run. A manual run is rejected if the account already has an active subscription.\n\nThe determination of a run's orders and the execution of a run take place during normal market hours. Runs can be initiated outside normal market hours but remain `QUEUED` until normal market hours.\n\nOnly one run in a non-terminal status is allowed at any time.",
        "operationId": "post-v1-rebalancing-runs",
        "requestBody": {
          "content": {
            "application/json": {
              "examples": {
                "manualRun": {
                  "summary": "Manual one-off rebalance run",
                  "value": {
                    "account_id": "bf2b0f93-f296-4276-a9cf-288586cf4fb7",
                    "type": "full_rebalance",
                    "weights": [
                      {
                        "percent": "35",
                        "symbol": "AAPL",
                        "type": "asset"
                      },
                      {
                        "percent": "20",
                        "symbol": "TSLA",
                        "type": "asset"
                      },
                      {
                        "percent": "45",
                        "symbol": "SPY",
                        "type": "asset"
                      }
                    ]
                  }
                },
                "subscriptionRun": {
                  "summary": "Subscription-driven rebalance run",
                  "value": {
                    "account_id": "bf2b0f93-f296-4276-a9cf-288586cf4fb7",
                    "type": "full_rebalance"
                  }
                }
              },
              "schema": {
                "properties": {
                  "account_id": {
                    "description": "The account to create the run for.",
                    "format": "uuid",
                    "type": "string"
                  },
                  "amount": {
                    "description": "Optional decimal amount used by the run. JSON strings and numbers are accepted.",
                    "type": [
                      "string",
                      "number",
                      "null"
                    ]
                  },
                  "type": {
                    "description": "The kind of rebalance run to create.",
                    "enum": [
                      "full_rebalance",
                      "invest_cash"
                    ],
                    "type": "string"
                  },
                  "weights": {
                    "description": "Asset allocation weights. Omit this field or provide an empty array to use the account's active subscription. Provide a non-empty array to create a manual one-off run. A manual run is rejected if the account already has an active subscription.",
                    "items": {
                      "$ref": "#/components/schemas/PortfolioWeightRequest"
                    },
                    "type": "array"
                  }
                },
                "required": [
                  "account_id",
                  "type"
                ],
                "type": "object"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "OK"
          }
        },
        "summary": "Create Run",
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