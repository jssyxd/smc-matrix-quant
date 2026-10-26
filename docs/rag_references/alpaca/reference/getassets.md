# Retrieve All Assets

Source: https://docs.alpaca.markets/us/reference/getassets.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve All Assets

Returns all assets

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "Asset": {
        "description": "Assets are sorted by asset class, exchange and symbol. Some assets are not tradable with Alpaca. These assets will be marked with the flag tradable=false",
        "properties": {
          "attributes": {
            "description": "Unique characteristics of the asset. Supported values:\n- `ptp_no_exception`: Asset is a Publicly Traded Partnership (PTP) without a qualified notice; non-U.S. customers may incur 10% withholding on gross proceeds as per IRS guidance, and are blocked from being purchased by default.\n- `ptp_with_exception`: Users can open positions in these PTPs without general restrictions.\n- `ipo`: Accepting limit orders only before the stock begins trading on the secondary market.\n- `has_options`: The underlying equity has listed options available on the platform. Note: if the equity had inactive/expired contracts in the past, this will still show up.\n- `options_late_close`: Indicates the underlying asset's options contracts close at 4:15pm ET instead of the standard 4:00pm ET.\n- `fractional_eh_enabled`: Indicates the asset accepts fractional orders during extended hours sessions (pre-market, post-market, and overnight if enabled).\n- `overnight_tradable`: Asset is eligible for overnight (24x5) trading in supported venues on the platform.\n- `overnight_halted`: Asset is eligible for overnight trading but is currently halted/blocked for overnight sessions due to risk, corporate action, compliance, or venue constraints.",
            "example": [
              "ptp_no_exception",
              "ipo"
            ],
            "items": {
              "enum": [
                "ptp_no_exception",
                "ptp_with_exception",
                "ipo",
                "has_options",
                "options_late_close",
                "fractional_eh_enabled",
                "overnight_tradable",
                "overnight_halted"
              ],
              "type": "string"
            },
            "type": "array"
          },
          "borrow_status": {
            "description": "Borrow status for US equity assets. This field is omitted for non-US-equity assets.",
            "enum": [
              "easy_to_borrow",
              "hard_to_borrow"
            ],
            "example": "easy_to_borrow",
            "type": "string"
          },
          "class": {
            "$ref": "#/components/schemas/AssetClass"
          },
          "exchange": {
            "$ref": "#/components/schemas/Exchange"
          },
          "fractionable": {
            "description": "Asset is fractionable or not",
            "example": true,
            "type": "boolean"
          },
          "id": {
            "description": "Asset ID",
            "example": "904837e3-3b76-47ec-b432-046db621571b",
            "format": "uuid",
            "type": "string"
          },
          "maintenance_margin_requirement": {
            "deprecated": true,
            "description": "**deprecated**: Please use margin_requirement_long or margin_requirement_short instead. Note that these fields are of type string.\nShows the margin requirement percentage for the asset (equities only).\n",
            "type": "number"
          },
          "margin_requirement_long": {
            "description": "The margin requirement percentage for the asset's long positions (equities only), encoded as a decimal string.",
            "example": "100",
            "format": "decimal",
            "type": "string"
          },
          "margin_requirement_short": {
            "description": "The margin requirement percentage for the asset's short positions (equities only), encoded as a decimal string.",
            "example": "30",
            "format": "decimal",
            "type": "string"
          },
          "marginable": {
            "description": "Asset is marginable or not",
            "example": true,
            "type": "boolean"
          },
          "min_order_size": {
            "description": "Minimum order size.  Field available for crypto only.",
            "type": "string"
          },
          "min_trade_increment": {
            "description": "Amount a trade quantity can be incremented by. Field available for crypto only.",
            "type": "string"
          },
          "name": {
            "description": "The official name of the asset",
            "example": "Apple Inc. Common Stock",
            "type": "string"
          },
          "price_increment": {
            "description": "Amount the price can be incremented by. Field available for crypto only.",
            "type": "string"
          },
          "shortable": {
            "description": "Asset is shortable or not",
            "example": true,
            "type": "boolean"
          },
          "status": {
            "description": "active or inactive",
            "enum": [
              "active",
              "inactive"
            ],
            "example": "active",
            "type": "string"
          },
          "symbol": {
            "description": "The symbol of the asset",
            "example": "AAPL",
            "type": "string"
          },
          "tradable": {
            "description": "Asset is tradable on Alpaca or not",
            "example": true,
            "type": "boolean"
          }
        },
        "required": [
          "id",
          "class",
          "exchange",
          "symbol",
          "name",
          "status",
          "tradable",
          "marginable",
          "shortable",
          "fractionable",
          "margin_requirement_long",
          "margin_requirement_short"
        ],
        "title": "Asset",
        "type": "object"
      },
      "AssetClass": {
        "description": "This represents the category to which the asset belongs to. It serves to identify the nature of the financial instrument, with options including \"us_equity\" for U.S. equities, \"us_option\" for U.S. options, \"crypto\" for cryptocurrencies, and \"ipo\" for IPO indications of interest. This `asset_class: ipo` value is distinct from the assets API `attributes: [\"ipo\"]` flag.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto",
          "ipo"
        ],
        "type": "string"
      },
      "Exchange": {
        "description": "Represents the exchange where an asset is traded.\n\nFor Stocks:\n- AMEX\n- ARCA\n- BATS\n- NYSE\n- NASDAQ\n- NYSEARCA\n- OTC\n\nFor Crypto:\n- CRYPTO",
        "enum": [
          "AMEX",
          "ARCA",
          "BATS",
          "NYSE",
          "NASDAQ",
          "NYSEARCA",
          "OTC"
        ],
        "example": "NASDAQ",
        "title": "Exchange",
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
    "/v1/assets": {
      "get": {
        "description": "Returns all assets",
        "operationId": "getAssets",
        "parameters": [
          {
            "description": "Asset status to filter by, will default to `all`",
            "in": "query",
            "name": "status",
            "schema": {
              "default": "all",
              "enum": [
                "active",
                "inactive",
                "all"
              ],
              "example": "all",
              "type": "string"
            }
          },
          {
            "description": "Asset class to filter by, `us_equity` or `crypto`. Defaults to `us_equity`",
            "in": "query",
            "name": "asset_class",
            "schema": {
              "default": "us_equity",
              "enum": [
                "us_equity",
                "crypto"
              ],
              "example": "us_equity",
              "type": "string"
            }
          },
          {
            "description": "Comma separated values to query for more than one attribute. Assets which have any of the given attributes will be included.\n\nSupported values:\n- `ptp_no_exception`: Asset is a Publicly Traded Partnership (PTP) without a qualified notice; non-U.S. customers may incur 10% withholding on gross proceeds as per IRS guidance, and are blocked from being purchased by default.\n- `ptp_with_exception`: Users can open positions in these PTPs without general restrictions.\n- `ipo`: Accepting limit orders only before the stock begins trading on the secondary market.\n- `has_options`: The underlying equity has listed options available on the platform. Note: if the equity had inactive/expired contracts in the past, this will still show up.\n- `options_late_close`: Indicates the underlying asset's options contracts close at 4:15pm ET instead of the standard 4:00pm ET.\n- `fractional_eh_enabled`: Indicates the asset accepts fractional orders during extended hours sessions (pre-market, post-market, and overnight if enabled).\n- `overnight_tradable`: Asset is eligible for overnight (24x5) trading in supported venues on the platform.\n- `overnight_halted`: Asset is eligible for overnight trading but is currently halted/blocked for overnight sessions due to risk, corporate action, compliance, or venue constraints.",
            "explode": false,
            "in": "query",
            "name": "attributes",
            "schema": {
              "default": [],
              "example": [
                "ptp_no_exception",
                "ipo"
              ],
              "items": {
                "enum": [
                  "ptp_no_exception",
                  "ptp_with_exception",
                  "ipo",
                  "has_options",
                  "options_late_close",
                  "fractional_eh_enabled",
                  "overnight_tradable",
                  "overnight_halted"
                ],
                "type": "string"
              },
              "type": "array"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Asset"
                  },
                  "type": "array"
                }
              }
            },
            "description": "An array of asset objects."
          }
        },
        "summary": "Retrieve All Assets",
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