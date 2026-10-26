# Retrieve countries information

Source: https://docs.alpaca.markets/us/reference/querycountryinfos.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve countries information

The Country Info API serves country information for every supported countries including risk ratings and supported crypto states where applicable.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CountryInfo": {
        "description": "Represents the info for a country.",
        "properties": {
          "crypto_risk_rating": {
            "description": "crypto risk rating of the country",
            "enum": [
              "low",
              "medium",
              "high",
              "restricted",
              "prohibited"
            ],
            "type": "string"
          },
          "crypto_supported_states": {
            "description": "states where Alpaca supports crypto trading",
            "items": {
              "description": "the state code defined by ISO 3166-2",
              "type": "string"
            },
            "type": "array"
          },
          "full_name": {
            "description": "The full name of the country definded by ISO 3166-1",
            "example": "Åland Islands",
            "minLength": 1,
            "type": "string"
          },
          "securities_risk_rating": {
            "description": "the securities risk rating of the country",
            "enum": [
              "low",
              "medium",
              "high",
              "restricted",
              "prohibited"
            ],
            "type": "string"
          }
        },
        "required": [
          "full_name",
          "securities_risk_rating",
          "crypto_risk_rating"
        ],
        "title": "CountryInfo",
        "type": "object"
      },
      "CountryInfos": {
        "additionalProperties": {
          "$ref": "#/components/schemas/CountryInfo"
        },
        "description": "Represents the info for countries as a map where the keys are the ISO 3166 country codes.",
        "title": "CountryInfos",
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
    "/v1/country-info": {
      "get": {
        "description": "The Country Info API serves country information for every supported countries including risk ratings and supported crypto states where applicable.",
        "operationId": "queryCountryInfos",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "countries": {
                    "summary": "Example response",
                    "value": {
                      "USA": {
                        "crypto_risk_rating": "medium",
                        "crypto_supported_states": [
                          "CA",
                          "CT",
                          "GA",
                          "IA",
                          "ID",
                          "IL",
                          "IN",
                          "KS",
                          "KY",
                          "MA",
                          "MD",
                          "ME",
                          "MI",
                          "MS",
                          "MO",
                          "MT",
                          "NC",
                          "ND",
                          "NE",
                          "OH",
                          "RI",
                          "SD",
                          "UT",
                          "VT",
                          "WA"
                        ],
                        "full_name": "United States of America",
                        "securities_risk_rating": "medium"
                      },
                      "ZAF": {
                        "crypto_risk_rating": "high",
                        "full_name": "South Africa",
                        "securities_risk_rating": "high"
                      }
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/CountryInfos"
                }
              }
            },
            "description": "Returns the countries information as a map"
          }
        },
        "summary": "Retrieve countries information",
        "tags": [
          "Country Info"
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
      "name": "Country Info"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```