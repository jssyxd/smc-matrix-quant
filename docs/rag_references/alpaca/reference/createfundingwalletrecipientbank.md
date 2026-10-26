# Create a recipient bank

Source: https://docs.alpaca.markets/us/reference/createfundingwalletrecipientbank.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create a recipient bank

Creates a new recipient bank. Returns the new recipient bank entity on success. entity.

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
      "FundingDetailPaymentType": {
        "description": "Status:\n * `swift_wire`: SWIFT wire\n * `local_rails`: Local scheme\n",
        "enum": [
          "swift_wire",
          "local_rails"
        ],
        "type": "string"
      },
      "FundingWalletRecipientBank": {
        "properties": {
          "account_number": {
            "description": "Bank account number.",
            "type": "string"
          },
          "bic_swift": {
            "description": "BIC/SWIFT code",
            "type": "string"
          },
          "city": {
            "description": "City",
            "type": "string"
          },
          "company_name": {
            "type": "string"
          },
          "country": {
            "description": "Two-letter ISO country code.",
            "type": "string"
          },
          "created_at": {
            "description": "Date the beneficiary record was created.",
            "format": "date-time",
            "type": "string"
          },
          "currency": {
            "description": "Currency in which money is held in the beneficiary's bank account. Three-digit currency code.",
            "type": "string"
          },
          "first_name": {
            "type": "string"
          },
          "iban": {
            "description": "IBAN code",
            "type": "string"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "last_name": {
            "type": "string"
          },
          "payment_types": {
            "items": {
              "$ref": "#/components/schemas/FundingDetailPaymentType"
            },
            "type": "array"
          },
          "postal_code": {
            "description": "Postal code",
            "type": "string"
          },
          "routing_code": {
            "description": "Value for \"routing_code_type\".",
            "type": "string"
          },
          "routing_code_type": {
            "description": "Local payment routing system.",
            "type": "string"
          },
          "state_or_province": {
            "description": "State or province.",
            "type": "string"
          },
          "street_address": {
            "type": "string"
          },
          "updated_at": {
            "description": "Date the beneficiary record was last updated.",
            "format": "date-time",
            "type": "string"
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
    "/v1beta/accounts/{account_id}/funding_wallet/recipient_bank": {
      "post": {
        "description": "Creates a new recipient bank. Returns the new recipient bank entity on success. entity.",
        "operationId": "createFundingWalletRecipientBank",
        "parameters": [
          {
            "description": "UUID alpaca account ID",
            "in": "path",
            "name": "account_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "account_number": {
                    "description": "Bank account number.",
                    "type": "string"
                  },
                  "account_type": {
                    "description": "Bank account type.",
                    "enum": [
                      "checking",
                      "savings"
                    ],
                    "type": "string"
                  },
                  "bank_account_holder_name": {
                    "description": "Bank account holder's name.",
                    "type": "string"
                  },
                  "bank_country": {
                    "description": "Two-letter code for the country in which the beneficiary's bank account is held.",
                    "type": "string"
                  },
                  "bank_name": {
                    "type": "string"
                  },
                  "bic_swift": {
                    "description": "BIC/SWIFT code",
                    "type": "string"
                  },
                  "city": {
                    "description": "City",
                    "type": "string"
                  },
                  "currency": {
                    "description": "Currency in which money is held in the beneficiary's bank account. ISO-3 currency code.",
                    "type": "string"
                  },
                  "iban": {
                    "description": "IBAN code",
                    "type": "string"
                  },
                  "postal_code": {
                    "description": "Postal code",
                    "type": "string"
                  },
                  "routing_code": {
                    "description": "Routing code for routing_code_type. If supplied, routing_code_type should also be supplied.",
                    "type": "string"
                  },
                  "routing_code_type": {
                    "description": "Local payment routing system. If supplied, routing_code should also be supplied.",
                    "enum": [
                      "sort_code",
                      "aba",
                      "bsb_code",
                      "institution_no",
                      "bank_code",
                      "branch_code",
                      "clabe",
                      "cnaps",
                      "ifsc"
                    ],
                    "type": "string"
                  },
                  "state_or_province": {
                    "description": "State or province.",
                    "type": "string"
                  },
                  "street_address": {
                    "description": "First line of address.",
                    "type": "string"
                  }
                },
                "required": [
                  "bank_country",
                  "currency",
                  "bank_name",
                  "street_address",
                  "city",
                  "account_number"
                ]
              }
            }
          }
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/FundingWalletRecipientBank"
                }
              }
            },
            "description": "Success."
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
        "summary": "Create a recipient bank",
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