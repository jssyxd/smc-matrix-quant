# List assets for a transfer

Source: https://docs.alpaca.markets/us/reference/listacatsassets.md

---
updatedAt: 2026-06-23T06:50:20.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List assets for a transfer

Assets are only available for partial transfers and for transfers where the deliverer has already responded with the list of assets. The asset list may change as the transfer is updated by the deliverer, all the way up until the transfer settles.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AcatsAsset": {
        "description": "An asset included in an ACATS transfer.",
        "example": {
          "amount": "24223.62",
          "asset_class": "EQUITY",
          "asset_description": "APPLE INC",
          "currency_code": "USD",
          "cusip": "037833100",
          "position": "LONG",
          "qty": "123",
          "status": "SETTLED",
          "symbol": "AAPL"
        },
        "properties": {
          "amount": {
            "description": "Positive number indicating the market value of the assets being transferred",
            "format": "decimal",
            "type": "string"
          },
          "asset_class": {
            "description": "Asset type",
            "enum": [
              "EQUITY",
              "CASH",
              "OPTION",
              "OTHER"
            ],
            "type": "string"
          },
          "asset_description": {
            "description": "Description, usually from DTCC's Security Master File",
            "type": "string"
          },
          "currency_code": {
            "description": "ISO currency code in which amount is denominated",
            "type": "string"
          },
          "cusip": {
            "description": "CUSIP security identifier for the asset. Only returned when a CUSIP was provided for this asset at the time the transfer was initiated, in which case it is returned alongside `symbol`.",
            "type": "string"
          },
          "isin": {
            "deprecated": true,
            "description": "ISIN for the asset. DEPRECATED -- will be removed in a future version; use `symbol` or `cusip` instead. Temporarily returned with all assets for backward compatibility.",
            "type": "string",
            "x-deprecation": {
              "reason": "Use `symbol` or `cusip` instead. Returned with all assets only for backward compatibility while consumers migrate.",
              "since": "2026-08-04",
              "sunset": "2027-02-04"
            }
          },
          "position": {
            "$ref": "#/components/schemas/AcatsPosition"
          },
          "qty": {
            "description": "Positive number indicating how many shares or units are being transferred",
            "format": "decimal",
            "type": "string"
          },
          "rejection_message": {
            "description": "Human readable reason for why an asset is considered ineligible for transfer",
            "type": "string"
          },
          "status": {
            "description": "Status",
            "enum": [
              "NOT_VALIDATED",
              "REQUESTED",
              "DELETED",
              "SETTLED",
              "REVERSED",
              "INTERFACE_REJECTED"
            ],
            "type": "string"
          },
          "symbol": {
            "description": "Symbol identifier for the asset. Always returned when a symbol is known for the asset, including when the transfer was initiated with a CUSIP.",
            "type": "string"
          }
        },
        "required": [
          "asset_class",
          "asset_description",
          "status",
          "position"
        ],
        "type": "object"
      },
      "AcatsError": {
        "description": "Body for responses with HTTP status codes indicating an error",
        "example": {
          "message": "contra broker number is required"
        },
        "properties": {
          "message": {
            "type": "string"
          }
        },
        "required": [
          "message"
        ],
        "type": "object"
      },
      "AcatsListAssetsResponse": {
        "description": "The list of assets associated with an ACATS transfer.",
        "example": [
          {
            "asset_class": "EQUITY",
            "asset_description": "APPLE INC",
            "cusip": "037833100",
            "position": "LONG",
            "qty": "10",
            "status": "SETTLED",
            "symbol": "AAPL"
          },
          {
            "amount": "1250.75",
            "asset_class": "CASH",
            "asset_description": "US DOLLAR",
            "currency_code": "USD",
            "position": "CREDIT",
            "status": "SETTLED"
          }
        ],
        "items": {
          "$ref": "#/components/schemas/AcatsAsset"
        },
        "type": "array"
      },
      "AcatsPosition": {
        "description": "Position type. `LONG` and `SHORT` apply to security positions; `CREDIT` and `DEBIT` apply to cash positions.",
        "enum": [
          "LONG",
          "SHORT",
          "CREDIT",
          "DEBIT"
        ],
        "type": "string"
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
    "/v1beta1/acats/{account_id}/{acats_id}/assets": {
      "get": {
        "description": "Assets are only available for partial transfers and for transfers where the deliverer has already responded with the list of assets. The asset list may change as the transfer is updated by the deliverer, all the way up until the transfer settles.",
        "operationId": "listACATSAssets",
        "parameters": [
          {
            "description": "Account ID associated with the ACATS transfer",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          },
          {
            "description": "The ID of the ACATS transfer",
            "in": "path",
            "name": "acats_id",
            "required": true,
            "schema": {
              "format": "uuid",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsListAssetsResponse"
                }
              }
            },
            "description": "OK"
          },
          "403": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Forbidden"
          },
          "404": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Not Found. No transfer with this `acats_id` exists for the given `account_id`."
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "summary": "List assets for a transfer",
        "tags": [
          "ACATS"
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
      "name": "ACATS"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```