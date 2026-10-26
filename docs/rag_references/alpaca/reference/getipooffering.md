# Retrieve an IPO Offering

Source: https://docs.alpaca.markets/us/reference/getipooffering.md

---
updatedAt: 2026-05-13T15:05:07.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve an IPO Offering

Returns a single IPO offering by `offering_reference`.

The `offering_reference` value matches the one delivered on the [IPO Events Stream](#operation/subscribeToIPOEventsSSE).


# OpenAPI definition

```json
{
  "components": {
    "examples": {
      "IPOOfferingGetExample": {
        "summary": "Single IPO offering",
        "value": {
          "data": {
            "anticipated_shares": 5000000,
            "availability": "available",
            "cusip_id": "123456789",
            "description": "Example Corp is a leading provider of example services.",
            "ipo_reference": "FI111225",
            "logo_small": "https://example.com/logos/exmp-small.png",
            "max_price": "44",
            "max_ticket_size": "100000",
            "min_price": "40",
            "min_ticket_size": "100",
            "name": "Example Corp",
            "no_new_orders": false,
            "offering_type": "IPO",
            "prospectus_url": "https://example.com/prospectus/example-corp.pdf",
            "settlement_date": "2026-04-04",
            "ticker_symbol": "EXMP",
            "trade_date": "2026-04-02",
            "underwriters": [
              "Goldman Sachs",
              "Morgan Stanley"
            ],
            "unit_step_size": "1"
          }
        }
      }
    },
    "schemas": {
      "IPOOffering": {
        "description": "An IPO (Initial Public Offering) offering exposed via the IPO discovery REST API. Returned by `GET /v1/ipos` and `GET /v1/ipos/{offering_reference}`.\n\nMost IPO lifecycle changes (new offerings, prospectus availability, 60-minute mail, allocations, cancellations) are pushed in real time over the [IPO Events Stream](#operation/subscribeToIPOEventsSSE).\n",
        "properties": {
          "anticipated_shares": {
            "description": "Anticipated total share count for the offering, when known.",
            "format": "int64",
            "type": "integer"
          },
          "availability": {
            "description": "Whether the offering is currently accepting orders.\n- `available` - accepting new orders.\n- `not_available` - not yet open for orders.\n- `closed` - no longer accepting orders.\n\nNote: the IPO Events Stream uses a different casing for the analogous `payload.available_to_order` field on `Offering`/`OfferingUpdate` events (`Available`, `NotAvailable`, `Closed`).\n",
            "enum": [
              "available",
              "not_available",
              "closed"
            ],
            "example": "available",
            "type": "string"
          },
          "cusip_id": {
            "description": "CUSIP identifier of the offering.",
            "example": "123456789",
            "type": "string"
          },
          "description": {
            "description": "A longer human-readable description of the offering, when available.",
            "type": "string"
          },
          "ipo_reference": {
            "description": "The unique offering identifier used across the IPO Events Stream and `/v1/ipos/{offering_reference}`. Note that this value is also used as the path parameter, where it is named `offering_reference`.\n",
            "example": "FI111225",
            "type": "string"
          },
          "logo_small": {
            "description": "URL to a small logo asset for the issuer.",
            "type": "string"
          },
          "max_price": {
            "description": "Upper bound of the indicated price range.",
            "example": "42",
            "format": "decimal",
            "type": "string"
          },
          "max_ticket_size": {
            "description": "Maximum allowed order amount.",
            "type": "string"
          },
          "min_price": {
            "description": "Lower bound of the indicated price range.",
            "example": "42",
            "format": "decimal",
            "type": "string"
          },
          "min_ticket_size": {
            "description": "Minimum allowed order amount.",
            "type": "string"
          },
          "name": {
            "description": "The official name of the offering.",
            "example": "Example Corp",
            "type": "string"
          },
          "no_new_orders": {
            "description": "When `true`, the offering is in its 60-minute pricing window and is not accepting new orders. This mirrors the `SixtyMinMail` event on the IPO Events Stream.\n",
            "example": false,
            "type": "boolean"
          },
          "offering_type": {
            "description": "The type of offering. Currently always `IPO`.",
            "example": "IPO",
            "type": "string"
          },
          "prospectus_url": {
            "description": "URL to the prospectus document. Mirrors the `prospectus_url` payload of the corresponding `Prospectus` event on the IPO Events Stream.\n",
            "type": "string"
          },
          "settlement_date": {
            "description": "Anticipated settlement date.",
            "format": "date",
            "type": "string"
          },
          "ticker_symbol": {
            "description": "The ticker symbol that will be used once the security begins trading on the secondary market.",
            "example": "EXMP",
            "type": "string"
          },
          "trade_date": {
            "description": "Anticipated first trading date on the secondary market.",
            "format": "date",
            "type": "string"
          },
          "underwriters": {
            "description": "List of underwriter names participating in the offering.",
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "unit_step_size": {
            "description": "The minimum increment in which order quantities can be specified.",
            "type": "string"
          }
        },
        "required": [
          "name",
          "ipo_reference",
          "offering_type",
          "availability",
          "max_price",
          "min_price",
          "no_new_orders"
        ],
        "title": "IPOOffering",
        "type": "object"
      },
      "IPOOfferingResponse": {
        "description": "Wrapper response returned by `GET /v1/ipos/{offering_reference}`.",
        "properties": {
          "data": {
            "$ref": "#/components/schemas/IPOOffering"
          }
        },
        "required": [
          "data"
        ],
        "title": "IPOOfferingResponse",
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
    "/v1/ipos/{offering_reference}": {
      "get": {
        "description": "Returns a single IPO offering by `offering_reference`.\n\nThe `offering_reference` value matches the one delivered on the [IPO Events Stream](#operation/subscribeToIPOEventsSSE).\n",
        "operationId": "getIPOOffering",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/IPOOfferingGetExample"
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/IPOOfferingResponse"
                }
              }
            },
            "description": "The requested IPO offering."
          },
          "404": {
            "description": "No IPO offering exists for the given `offering_reference`."
          }
        },
        "summary": "Retrieve an IPO Offering",
        "tags": [
          "IPO"
        ]
      },
      "parameters": [
        {
          "description": "The unique offering identifier (also referred to as `ipo_reference` in the response body).",
          "example": "FI111225",
          "in": "path",
          "name": "offering_reference",
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
      "description": "Endpoints for discovering and tracking IPO (Initial Public Offering) lifecycle data. Use [`GET /v1/ipos`](#operation/listIPOOfferings) and [`GET /v1/ipos/{offering_reference}`](#operation/getIPOOffering) to query offerings on demand, and the [IPO Events Stream](#operation/subscribeToIPOEventsSSE) under the **Events** group to receive real-time and historical lifecycle updates (new offerings, prospectus, 60-minute mail, allocations, cancellations).\n",
      "name": "IPO"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```