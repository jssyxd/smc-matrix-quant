# An array of whitelisted addresses

Source: https://docs.alpaca.markets/us/reference/listwhitelistedaddress.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# An array of whitelisted addresses

Returns the list of whitelisted withdrawal addresses for your account.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "TravelRuleInfo": {
        "description": "Travel rule information pertaining to the wallet being whitelisted. Identify the destination by providing beneficiary_vasp_id, setting beneficiary_is_self_hosted to true, or providing beneficiary_manual_entry. Either beneficiary_entity_name (for legal entities) or beneficiary_given_name and beneficiary_family_name (for natural persons) must be provided.",
        "properties": {
          "beneficiary_country_of_residence": {
            "description": "ISO 3166-1 country code for the beneficiary's country of residence.",
            "example": "US",
            "type": "string"
          },
          "beneficiary_entity_name": {
            "description": "The beneficiary's legal entity name (required for legal entities)",
            "example": "Alpaca Crypto LLC",
            "minLength": 1,
            "type": "string"
          },
          "beneficiary_family_name": {
            "description": "The beneficiary's last name (required for natural persons)",
            "example": "Doe",
            "minLength": 1,
            "type": "string"
          },
          "beneficiary_geographic_address_building_number": {
            "description": "Building number in the beneficiary's geographic address.",
            "example": "1",
            "type": "string"
          },
          "beneficiary_geographic_address_country": {
            "description": "ISO 3166-1 alpha-2 or alpha-3 country code in the beneficiary's geographic address.",
            "example": "US",
            "type": "string"
          },
          "beneficiary_geographic_address_post_code": {
            "description": "Postal code in the beneficiary's geographic address.",
            "example": "10001",
            "type": "string"
          },
          "beneficiary_geographic_address_street_name": {
            "description": "Street name in the beneficiary's geographic address.",
            "example": "Main Street",
            "type": "string"
          },
          "beneficiary_geographic_address_town_name": {
            "description": "Town or city in the beneficiary's geographic address.",
            "example": "New York",
            "type": "string"
          },
          "beneficiary_given_name": {
            "description": "The beneficiary's first name (required for natural persons)",
            "example": "John",
            "minLength": 1,
            "type": "string"
          },
          "beneficiary_is_self_hosted": {
            "description": "Beneficiary is receiving funds to a self-hosted / non-custodial wallet",
            "example": true,
            "type": "boolean"
          },
          "beneficiary_manual_entry": {
            "$ref": "#/components/schemas/TravelRuleManualEntry"
          },
          "beneficiary_vasp_id": {
            "description": "The W3C Decentralized Identifier (DID) representing the beneficiary's VASP.",
            "example": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
            "pattern": "^did:[a-zA-Z0-9]*:.*$",
            "type": "string"
          }
        },
        "title": "TravelRuleInfo",
        "type": "object"
      },
      "TravelRuleManualEntry": {
        "description": "Information about a beneficiary VASP that is not available in the VASP directory.",
        "properties": {
          "vasp_name": {
            "description": "The name of the receiving exchange.",
            "example": "Alpaca",
            "type": "string"
          },
          "vasp_website": {
            "description": "The receiving exchange's website.",
            "example": "https://alpaca.markets",
            "format": "uri",
            "type": "string"
          }
        },
        "required": [
          "vasp_name",
          "vasp_website"
        ],
        "type": "object"
      },
      "WhitelistedAddress": {
        "properties": {
          "address": {
            "description": "The whitelisted address",
            "type": "string"
          },
          "asset": {
            "description": "Symbol of underlying asset for the whitelisted address",
            "type": "string"
          },
          "chain": {
            "description": "Underlying network this address represents",
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp (RFC3339) of account creation.",
            "format": "date-time",
            "type": "string"
          },
          "id": {
            "description": "Unique ID for whitelisted address",
            "type": "string"
          },
          "status": {
            "description": "Status of whitelisted address which is either APPROVED or PENDING. Whitelisted addresses will be subjected to a 24 waiting period. After the waiting period is over the status will become APPROVED.",
            "enum": [
              "APPROVED",
              "PENDING"
            ],
            "type": "string"
          },
          "travel_rule_info": {
            "allOf": [
              {
                "$ref": "#/components/schemas/TravelRuleInfo"
              }
            ],
            "description": "Travel rule information associated with the whitelisted address."
          }
        },
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
    "/v2/wallets/whitelists": {
      "get": {
        "description": "Returns the list of whitelisted withdrawal addresses for your account.",
        "operationId": "listWhitelistedAddress",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/WhitelistedAddress"
                }
              }
            },
            "description": "An array of whitelisted objects"
          }
        },
        "summary": "An array of whitelisted addresses",
        "tags": [
          "Crypto Funding"
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
      "name": "Crypto Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```