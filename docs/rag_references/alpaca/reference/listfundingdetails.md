# Retrieve funding details

Source: https://docs.alpaca.markets/us/reference/listfundingdetails.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve funding details

Returns a list of funding details if it exists. Query parameters must be passed to create a new funding details object if none exist.

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
      "FundingDetail": {
        "description": "Gets funding details that can be used to settle and collect funds in each available currency.\n",
        "properties": {
          "account_holder_name": {
            "type": "string"
          },
          "account_number": {
            "type": "string"
          },
          "account_number_type": {
            "type": "string"
          },
          "bank_address": {
            "type": "string"
          },
          "bank_country": {
            "type": "string"
          },
          "bank_name": {
            "type": "string"
          },
          "currency": {
            "type": "string"
          },
          "payment_type": {
            "$ref": "#/components/schemas/FundingDetailPaymentType"
          },
          "routing_code": {
            "type": "string"
          },
          "routing_code_type": {
            "$ref": "#/components/schemas/FundingDetailRoutingCodeType"
          }
        },
        "type": "object"
      },
      "FundingDetailPaymentType": {
        "description": "Status:\n * `swift_wire`: SWIFT wire\n * `local_rails`: Local scheme\n",
        "enum": [
          "swift_wire",
          "local_rails"
        ],
        "type": "string"
      },
      "FundingDetailRoutingCodeType": {
        "description": "Status:\n * `BIC`: bic_swift\n * `ACH`: ach_routing_code\n * `ABA`: aba\n * `ROUTING`: routing_code\n * `SORT_CODE`: sort_code\n",
        "enum": [
          "BIC",
          "ACH_ROUTING",
          "ABA",
          "ROUTING",
          "SORT_CODE"
        ],
        "type": "string"
      },
      "ListFundingDetails": {
        "properties": {
          "funding_details": {
            "items": {
              "$ref": "#/components/schemas/FundingDetail"
            },
            "type": "array"
          }
        },
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
    "/v1beta/accounts/{account_id}/funding_wallet/funding_details": {
      "get": {
        "description": "Returns a list of funding details if it exists. Query parameters must be passed to create a new funding details object if none exist.",
        "operationId": "listFundingDetails",
        "parameters": [
          {
            "description": "UUID alpaca account ID",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "description": "The type of SSI to be returned, priority (SWIFT) or regular (local). A null value returns all payment types.",
            "in": "query",
            "name": "payment_type",
            "required": false,
            "schema": {
              "$ref": "#/components/schemas/FundingDetailPaymentType"
            }
          },
          {
            "description": "Should be provided in ISO 4217 standard",
            "in": "query",
            "name": "currency",
            "required": false,
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
                  "items": {
                    "$ref": "#/components/schemas/ListFundingDetails"
                  }
                }
              }
            },
            "description": "list of wallets"
          },
          "default": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "error"
          }
        },
        "summary": "Retrieve funding details",
        "tags": [
          "Funding Wallets"
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
      "name": "Funding Wallets"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```