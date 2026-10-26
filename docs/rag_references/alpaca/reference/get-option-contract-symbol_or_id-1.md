# Get an option contract by ID or Symbol (BETA)

Source: https://docs.alpaca.markets/us/reference/get-option-contract-symbol_or_id-1.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get an option contract by ID or Symbol (BETA)

Get an option contract by symbol or contract ID. The symbol or id should be passed in as a path parameter.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
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
      },
      "OptionContract": {
        "properties": {
          "close_price": {
            "description": "The close price of the option contract.",
            "example": "148.38",
            "type": "string"
          },
          "close_price_date": {
            "description": "The date of the close price data.",
            "example": "2023-12-11",
            "format": "date",
            "type": "string"
          },
          "deliverables": {
            "description": "Represents the deliverables tied to the option contract. While standard contracts entail a single deliverable, non-standard ones can encompass multiple deliverables, each potentially customized with distinct parameters.\nThis array is included in the list contracts response only if the query parameter show_deliverables=true is provided.\n",
            "items": {
              "$ref": "#/components/schemas/OptionDeliverable"
            },
            "type": "array"
          },
          "expiration_date": {
            "description": "The expiration date of the option contract.",
            "example": "2025-06-20",
            "format": "date",
            "type": "string"
          },
          "id": {
            "description": "The unique identifier of the option contract.",
            "example": "98359ef7-5124-49f3-85ea-5cf02df6defa",
            "type": "string"
          },
          "multiplier": {
            "description": "The multiplier of the option contract is crucial for calculating both the trade premium and the extended strike price. In standard contracts, the multiplier is always set to 100.\nFor instance, if a contract is traded at $1.50 and the multiplier is 100, the total amount debited when buying the contract would be $150.00.\nSimilarly, when exercising a call contract, the total cost will be equal to the strike price times the multiplier.",
            "example": "100",
            "type": "string"
          },
          "name": {
            "description": "The name of the option contract.",
            "example": "AAPL Jun 20 2025 100 Call",
            "type": "string"
          },
          "open_interest": {
            "description": "The open interest of the option contract.",
            "example": "237",
            "type": "string"
          },
          "open_interest_date": {
            "description": "The date of the open interest data.",
            "example": "2023-12-11",
            "format": "date",
            "type": "string"
          },
          "ppind": {
            "description": "The ppind (Penny Program Indicator) field indicates whether an option contract is eligible for penny price increments,\nwith `true` meaning it is part of the Penny Program and `false` meaning it is not.",
            "example": true,
            "type": "boolean"
          },
          "root_symbol": {
            "description": "The root symbol of the option contract.",
            "example": "AAPL",
            "type": "string"
          },
          "size": {
            "description": "Represents the number of underlying shares to be delivered in case the contract is exercised/assigned. For standard contracts, this is always 100.\nThis field should **not** be used as a multiplier, specially for non-standard contracts.",
            "example": "100",
            "type": "string"
          },
          "status": {
            "description": "The status of the option contract.",
            "enum": [
              "active",
              "inactive"
            ],
            "example": "active",
            "type": "string"
          },
          "strike_price": {
            "description": "The strike price of the option contract.",
            "example": "100",
            "type": "string"
          },
          "style": {
            "description": "The style of the option contract.",
            "enum": [
              "american",
              "european"
            ],
            "example": "american",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol representing the option contract.",
            "example": "AAPL250620C00100000",
            "type": "string"
          },
          "tradable": {
            "description": "Indicates whether the option contract is tradable.",
            "example": true,
            "type": "boolean"
          },
          "type": {
            "description": "The type of the option contract.",
            "enum": [
              "call",
              "put"
            ],
            "example": "call",
            "type": "string"
          },
          "underlying_asset_id": {
            "description": "The unique identifier of the underlying asset.",
            "example": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "type": "string"
          },
          "underlying_symbol": {
            "description": "The underlying symbol of the option contract.",
            "example": "AAPL",
            "type": "string"
          }
        },
        "required": [
          "id",
          "symbol",
          "name",
          "status",
          "tradable",
          "expiration_date",
          "underlying_symbol",
          "underlying_asset_id",
          "type",
          "style",
          "strike_price",
          "multiplier",
          "size",
          "ppind"
        ],
        "type": "object"
      },
      "OptionDeliverable": {
        "properties": {
          "allocation_percentage": {
            "description": "Cost allocation percentage of the deliverable.\nThis is used to determine the cost basis of the equity shares received from the exercise, specially for non-standard contracts with multiple deliverables.\n",
            "example": "100",
            "type": "string"
          },
          "amount": {
            "description": "The deliverable amount. For cash deliverables, this is the cash amount.\nFor standard contract, this is always 100.\nThis field can be null in case the deliverable settlement is delayed and the amount is yet to be determined.\n",
            "example": "100",
            "type": "string"
          },
          "asset_id": {
            "description": "Unique identifier of the deliverable asset. For standard contracts, this is equivalent to underlying_asset_id of the contracts.\nThis field is not returned for cash deliverables.\n",
            "example": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "type": "string"
          },
          "delayed_settlement": {
            "description": "If true, the settlement of the deliverable will be delayed.\nFor instance, in the event of a contract with a delayed deliverable being exercised, both the availability of the deliverable and its settlement may be postponed beyond the typical timeframe.\n",
            "example": false,
            "type": "boolean"
          },
          "settlement_method": {
            "description": "Indicates the settlement method that will be used:\n- **BTOB**: Broker to Broker\n- **CADF**: Cash Difference\n- **CAFX**: Cash Fixed\n- **CCC**: Correspondent Clearing Corp\n",
            "enum": [
              "BTOB",
              "CADF",
              "CAFX",
              "CCC"
            ],
            "example": "CCC",
            "type": "string"
          },
          "settlement_type": {
            "description": "Indicates when the deliverable will be settled if the contract is exercised/assigned.\n",
            "enum": [
              "T+0",
              "T+1",
              "T+2",
              "T+3",
              "T+4",
              "T+5"
            ],
            "example": "T+2",
            "type": "string"
          },
          "symbol": {
            "description": "Symbol of the deliverable. For standard contracts, this is equivalent to the underlying symbol of the contract.\n",
            "example": "AAPL",
            "type": "string"
          },
          "type": {
            "description": "Type of deliverable, indicating whether it's cash or equity. For standard contracts, it is always \"equity\".\n",
            "enum": [
              "cash",
              "equity"
            ],
            "example": "equity",
            "type": "string"
          }
        },
        "required": [
          "type",
          "symbol",
          "amount",
          "allocation_percentage",
          "settlement_type",
          "settlement_method",
          "delayed_settlement"
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
    "/v1/options/contracts/{symbol_or_id}": {
      "get": {
        "description": "Get an option contract by symbol or contract ID. The symbol or id should be passed in as a path parameter.",
        "operationId": "get-option-contract-symbol_or_id",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OptionContract"
                }
              }
            },
            "description": "An option contract"
          },
          "404": {
            "content": {
              "application/json": {
                "examples": {
                  "Contract Not Found": {
                    "value": {
                      "code": 40410000,
                      "message": "option contract TSLA231110C00021000 not found"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "Not Found"
          }
        },
        "summary": "Get an option contract by ID or Symbol (BETA)",
        "tags": [
          "Assets"
        ]
      },
      "parameters": [
        {
          "description": "The contract symbol or ID.",
          "in": "path",
          "name": "symbol_or_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ]
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