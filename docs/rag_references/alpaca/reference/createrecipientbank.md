# Create a Bank Relationship for an Account

Source: https://docs.alpaca.markets/us/reference/createrecipientbank.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create a Bank Relationship for an Account

If successful, retrieves Bank Relationships for an account

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
    "schemas": {
      "Bank": {
        "examples": [
          {
            "account_id": "56712986-9ff7-4d8f-8e52-077e099e533e",
            "account_number": "123456789abc",
            "bank_code": "123456789",
            "bank_code_type": "ABA",
            "city": "",
            "country": "",
            "created_at": "2022-02-11T21:35:19.268681613Z",
            "id": "8475c676-68e3-4cfc-a683-9ca2f47a6172",
            "name": "Bank XYZ",
            "postal_code": "",
            "state_province": "",
            "status": "QUEUED",
            "street_address": "",
            "updated_at": "2022-02-11T21:35:19.268681613Z"
          }
        ],
        "properties": {
          "account_id": {
            "format": "uuid",
            "type": "string"
          },
          "account_number": {
            "type": "string"
          },
          "bank_code": {
            "description": "9-Digit ABA RTN (Routing Number) or BIC",
            "type": "string"
          },
          "bank_code_type": {
            "description": "ABA (Domestic) or BIC (International)",
            "enum": [
              "ABA",
              "BIC"
            ],
            "type": "string"
          },
          "city": {
            "description": "Only for international banks",
            "type": "string"
          },
          "country": {
            "description": "Only for international banks",
            "type": "string"
          },
          "created_at": {
            "description": "Format: 2020-01-01T01:01:01Z",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          },
          "extra_fields": {
            "$ref": "#/components/schemas/BankAdditionalFields"
          },
          "id": {
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          },
          "name": {
            "description": "Name of recipient bank",
            "type": "string"
          },
          "postal_code": {
            "description": "Only for international banks",
            "type": "string"
          },
          "state_province": {
            "description": "Only for international banks",
            "type": "string"
          },
          "status": {
            "description": "QUEUED, SENT_TO_CLEARING, APPROVED, REJECTED, CANCELED",
            "enum": [
              "QUEUED",
              "SENT_TO_CLEARING",
              "APPROVED",
              "REJECTED",
              "CANCELED"
            ],
            "type": "string"
          },
          "street_address": {
            "description": "Only for international banks",
            "type": "string"
          },
          "updated_at": {
            "description": "Format: 2020-01-01T01:01:01Z",
            "example": "2021-03-16T18:38:01.942282Z",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "id",
          "created_at",
          "updated_at",
          "name",
          "bank_code",
          "bank_code_type",
          "account_number"
        ],
        "type": "object"
      },
      "BankAdditionalFields": {
        "description": "Additional wire instructions used to explicitly specify intermediary (correspondent) banks for international wire transfers. If omitted, intermediary banks may be automatically selected by downstream institutions, which can result in delays or additional charges.\n",
        "properties": {
          "intermediary_bank1_bic": {
            "description": "The primary intermediary (correspondent) bank to be used when routing the international wire transfer to the beneficiary bank.",
            "type": "string"
          },
          "intermediary_bank2_bic": {
            "description": "An additional intermediary bank to be used if the wire transfer requires multiple correspondent banks before reaching the beneficiary bank.",
            "type": "string"
          },
          "intermediary_bank3_bic": {
            "description": "A tertiary intermediary bank used in complex international wire routes that require three correspondent banks prior to reaching the beneficiary bank.",
            "type": "string"
          }
        },
        "type": "object"
      },
      "CreateBankRequest": {
        "description": "Represents the possible fields to send when creating a new associated Bank resource for an account",
        "properties": {
          "account_number": {
            "type": "string"
          },
          "bank_code": {
            "description": "9-Digit ABA RTN (Routing Number) or BIC",
            "type": "string"
          },
          "bank_code_type": {
            "description": "ABA (Domestic) or BIC (International)",
            "enum": [
              "ABA",
              "BIC"
            ],
            "type": "string"
          },
          "city": {
            "description": "Only for international banks, ie if bank_code_type = BIC",
            "type": "string"
          },
          "country": {
            "description": "Only for international banks, ie if bank_code_type = BIC",
            "type": "string"
          },
          "extra_fields": {
            "$ref": "#/components/schemas/BankAdditionalFields"
          },
          "name": {
            "description": "Name of recipient bank",
            "type": "string"
          },
          "postal_code": {
            "description": "Only for international banks, ie if bank_code_type = BIC. Minimum of 3 characters",
            "type": "string"
          },
          "state_province": {
            "description": "Only for international banks, ie if bank_code_type = BIC",
            "type": "string"
          },
          "street_address": {
            "description": "Only for international banks, ie if bank_code_type = BIC",
            "type": "string"
          }
        },
        "required": [
          "name",
          "bank_code",
          "bank_code_type",
          "account_number"
        ],
        "title": "CreateBankRequest",
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
    "/v1/accounts/{account_id}/recipient_banks": {
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        }
      ],
      "post": {
        "description": "If successful, retrieves Bank Relationships for an account",
        "operationId": "createRecipientBank",
        "parameters": [
          {
            "$ref": "#/components/parameters/AccountID"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateBankRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Bank"
                }
              }
            },
            "description": "The created Bank relationship"
          },
          "400": {
            "description": "Bad Request"
          },
          "409": {
            "description": "A Bank relationship already exists for this account"
          }
        },
        "summary": "Create a Bank Relationship for an Account",
        "tags": [
          "Funding",
          "Accounts"
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
      "name": "Accounts"
    },
    {
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```