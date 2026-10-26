# Get Option Contracts

Source: https://docs.alpaca.markets/us/reference/get-options-contracts.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Get Option Contracts

This endpoint allows you to retrieve a list of option contracts based on various filtering criteria.
By default only active contracts that expire before the upcoming weekend are returned.


# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "PageToken": {
        "description": "Used for pagination, this token retrieves the next page of results. It is obtained from the response of the preceding page when additional pages are available.",
        "in": "query",
        "name": "page_token",
        "required": false,
        "schema": {
          "example": "eyJpZCI6IjU1MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMCJ9Cg",
          "type": "string"
        }
      }
    },
    "schemas": {
      "NextPageToken": {
        "description": "Use this token in your next API call to paginate through the dataset and retrieve the next page of results. A null token indicates there are no more data to fetch.\n",
        "example": "MTAwMA==",
        "type": [
          "string",
          "null"
        ]
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
            "format": "uuid",
            "type": "string"
          },
          "multiplier": {
            "description": "The multiplier of the option contract is crucial for calculating both the trade premium and the extended strike price. In standard contracts, the multiplier is always set to 100.\nFor instance, if a contract is traded at $1.50 and the multiplier is 100, the total amount debited when buying the contract would be $150.00.\nSimilarly, when exercising a call contract, the total cost will be equal to the strike price times the multiplier.",
            "example": "100",
            "format": "decimal",
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
            "format": "decimal",
            "type": "string"
          },
          "style": {
            "$ref": "#/components/schemas/OptionContractStyle"
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
            "$ref": "#/components/schemas/OptionContractType"
          },
          "underlying_asset_id": {
            "description": "The unique identifier of the underlying asset.",
            "example": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "format": "uuid",
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
      "OptionContractStyle": {
        "description": "The style of the option contract.",
        "enum": [
          "american",
          "european"
        ],
        "example": "american",
        "type": "string"
      },
      "OptionContractType": {
        "description": "The type of the option contract.",
        "enum": [
          "call",
          "put"
        ],
        "example": "call",
        "type": "string"
      },
      "OptionContractsResponse": {
        "description": "Paginated list of option contracts.",
        "properties": {
          "next_page_token": {
            "$ref": "#/components/schemas/NextPageToken"
          },
          "option_contracts": {
            "example": [
              {
                "expiration_date": "2025-06-20",
                "id": "98359ef7-5124-49f3-85ea-5cf02df6defa",
                "multiplier": "100",
                "name": "AAPL Jun 20 2025 100 Call",
                "ppind": true,
                "root_symbol": "AAPL",
                "size": "100",
                "status": "active",
                "strike_price": "100",
                "style": "american",
                "symbol": "AAPL250620C00100000",
                "tradable": true,
                "type": "call",
                "underlying_asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
                "underlying_symbol": "AAPL"
              }
            ],
            "items": {
              "$ref": "#/components/schemas/OptionContract"
            },
            "type": "array"
          }
        },
        "required": [
          "option_contracts"
        ],
        "title": "OptionContractsResponse",
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
            "format": "uuid",
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
    "/v2/options/contracts": {
      "get": {
        "description": "This endpoint allows you to retrieve a list of option contracts based on various filtering criteria.\nBy default only active contracts that expire before the upcoming weekend are returned.\n",
        "operationId": "get-options-contracts",
        "parameters": [
          {
            "description": "Filter contracts by one or more underlying symbols.",
            "example": "AAPL,SPY",
            "in": "query",
            "name": "underlying_symbols",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Include deliverables array in the response.",
            "example": true,
            "in": "query",
            "name": "show_deliverables",
            "schema": {
              "type": "boolean"
            }
          },
          {
            "description": "Filter contracts by status (active/inactive). By default only active contracts are returned.",
            "example": "active",
            "in": "query",
            "name": "status",
            "schema": {
              "enum": [
                "active",
                "inactive"
              ],
              "type": "string"
            }
          },
          {
            "description": "Filter contracts by the exact expiration date (format: YYYY-MM-DD).",
            "example": "2025-06-20",
            "in": "query",
            "name": "expiration_date",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Filter contracts with expiration date greater than or equal to the specified date.",
            "example": "2025-06-20",
            "in": "query",
            "name": "expiration_date_gte",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Filter contracts with expiration date less than or equal to the specified date. By default this is set to the next weekend.",
            "example": "2025-06-20",
            "in": "query",
            "name": "expiration_date_lte",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Filter contracts by the root symbol.",
            "example": "AAPL",
            "in": "query",
            "name": "root_symbol",
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "Filter contracts by the type (call/put).",
            "example": "call",
            "in": "query",
            "name": "type",
            "schema": {
              "$ref": "#/components/schemas/OptionContractType"
            }
          },
          {
            "description": "Filter contracts by the style (american/european).",
            "example": "american",
            "in": "query",
            "name": "style",
            "schema": {
              "$ref": "#/components/schemas/OptionContractStyle"
            }
          },
          {
            "description": "Filter contracts with strike price greater than or equal to the specified value.",
            "example": 50,
            "in": "query",
            "name": "strike_price_gte",
            "schema": {
              "type": "number"
            }
          },
          {
            "description": "Filter contracts with strike price less than or equal to the specified value.",
            "example": 100,
            "in": "query",
            "name": "strike_price_lte",
            "schema": {
              "type": "number"
            }
          },
          {
            "$ref": "#/components/parameters/PageToken"
          },
          {
            "description": "The number of contracts to limit per page (default=100, max=10000).",
            "example": 100,
            "in": "query",
            "name": "limit",
            "schema": {
              "type": "integer"
            }
          },
          {
            "description": "The ppind (Penny Program Indicator) field indicates whether an option contract is eligible for penny price increments,\nwith `true` meaning it is part of the Penny Program and `false` meaning it is not.",
            "example": true,
            "in": "query",
            "name": "ppind",
            "schema": {
              "type": "boolean"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OptionContractsResponse"
                }
              }
            },
            "description": "Successful Response."
          }
        },
        "summary": "Get Option Contracts",
        "tags": [
          "Assets"
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
      "name": "Assets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```