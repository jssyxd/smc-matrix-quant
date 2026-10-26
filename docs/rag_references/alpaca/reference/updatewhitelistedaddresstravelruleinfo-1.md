# Update travel rule information for a whitelisted wallet

Source: https://docs.alpaca.markets/us/reference/updatewhitelistedaddresstravelruleinfo-1.md

---
updatedAt: 2026-07-29T12:06:40.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Update travel rule information for a whitelisted wallet

You are required to supply travel rule information for the crypto wallets you're withdrawing to.

It is preferred that you use the `Search VASPs` endpoint to find the VASP DID for the exchange you are withdrawing to,
otherwise, if it's a self-hosted wallet, please set `beneficiary_is_self_hosted` to true.

If the exchange cannot be found in our directory, please supply the information manually using the `beneficiary_manual_entry` object.

# OpenAPI definition

```json
{
  "components": {
    "examples": {
      "TravelRuleValidationError": {
        "description": "The request requires the beneficiary's name before the transfer can proceed.",
        "summary": "Missing beneficiary name",
        "value": {
          "error_code": "BENEFICIARY_NAME_REQUIRED",
          "message": "Please provide the beneficiary's name. Select one of the following options.",
          "next_actions": [
            {
              "description": "Provide the recipient's first and last name.",
              "name": "supply_beneficiaryName_naturalPerson",
              "required_fields": [
                {
                  "description": "The recipient's first name.",
                  "field": "beneficiary_given_name",
                  "value_type": "string"
                },
                {
                  "description": "The recipient's last name.",
                  "field": "beneficiary_family_name",
                  "value_type": "string"
                }
              ],
              "type": "ONE_OF"
            },
            {
              "description": "Provide the entity's legal name.",
              "name": "supply_beneficiaryName_legalEntity",
              "required_fields": [
                {
                  "description": "The legal name of the receiving entity.",
                  "field": "beneficiary_entity_name",
                  "value_type": "string"
                }
              ],
              "type": "ONE_OF"
            }
          ]
        }
      }
    },
    "schemas": {
      "TravelRuleErrorResponse": {
        "description": "A wallet or travel rule validation error.",
        "oneOf": [
          {
            "$ref": "#/components/schemas/TravelRuleValidationError"
          },
          {
            "$ref": "#/components/schemas/WalletError"
          }
        ]
      },
      "TravelRuleFieldOption": {
        "description": "Allowed value for a travel rule field that accepts a fixed set of choices.",
        "properties": {
          "description": {
            "type": "string"
          },
          "value": {
            "type": "string"
          }
        },
        "required": [
          "value",
          "description"
        ],
        "type": "object"
      },
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
      "TravelRuleNextAction": {
        "description": "Action the client must take to satisfy travel rule requirements.",
        "properties": {
          "description": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "required_fields": {
            "items": {
              "$ref": "#/components/schemas/TravelRuleRequiredField"
            },
            "type": "array"
          },
          "type": {
            "enum": [
              "REQUIRED",
              "ONE_OF"
            ],
            "type": "string"
          }
        },
        "required": [
          "name",
          "description",
          "type"
        ],
        "type": "object"
      },
      "TravelRuleRequiredField": {
        "description": "Request field required to complete a travel rule action.",
        "properties": {
          "description": {
            "type": "string"
          },
          "field": {
            "type": "string"
          },
          "options": {
            "description": "List of valid choices for 'enum' types. Null for simple strings or booleans.",
            "items": {
              "$ref": "#/components/schemas/TravelRuleFieldOption"
            },
            "type": [
              "array",
              "null"
            ]
          },
          "value_type": {
            "enum": [
              "string",
              "bool"
            ],
            "type": "string"
          }
        },
        "required": [
          "field",
          "value_type",
          "description"
        ],
        "type": "object"
      },
      "TravelRuleValidationError": {
        "description": "Travel rule validation failure and the actions required to correct it.",
        "properties": {
          "error_code": {
            "$ref": "#/components/schemas/TravelRuleValidationErrorCode"
          },
          "message": {
            "example": "Please provide the beneficiary's name. Select one of the following options.",
            "type": "string"
          },
          "next_actions": {
            "description": "A list of actions to be taken to fulfill information requirements.",
            "example": [
              {
                "description": "Provide the recipient's first and last name.",
                "name": "supply_beneficiaryName_naturalPerson",
                "required_fields": [
                  {
                    "description": "The recipient's first name.",
                    "field": "beneficiary_given_name",
                    "value_type": "string"
                  },
                  {
                    "description": "The recipient's last name.",
                    "field": "beneficiary_family_name",
                    "value_type": "string"
                  }
                ],
                "type": "ONE_OF"
              },
              {
                "description": "Provide the entity's legal name.",
                "name": "supply_beneficiaryName_legalEntity",
                "required_fields": [
                  {
                    "description": "The legal name of the receiving entity.",
                    "field": "beneficiary_entity_name",
                    "value_type": "string"
                  }
                ],
                "type": "ONE_OF"
              }
            ],
            "items": {
              "$ref": "#/components/schemas/TravelRuleNextAction"
            },
            "type": "array"
          }
        },
        "required": [
          "error_code",
          "message",
          "next_actions"
        ],
        "type": "object"
      },
      "TravelRuleValidationErrorCode": {
        "description": "Machine-readable code identifying the travel rule validation failure.",
        "enum": [
          "INVALID_DATA",
          "UNKNOWN_VASP",
          "ADDRESS_BELONGS_TO_VASP",
          "TRAVEL_RULE_ACTION_REQUIRED",
          "BENEFICIARY_NAME_REQUIRED"
        ],
        "example": "BENEFICIARY_NAME_REQUIRED",
        "type": "string"
      },
      "UpdateWhitelistedAddressTravelRuleInfoRequest": {
        "description": "Travel rule information to associate with a whitelisted address.",
        "properties": {
          "travel_rule_info": {
            "$ref": "#/components/schemas/TravelRuleInfo"
          }
        },
        "required": [
          "travel_rule_info"
        ],
        "type": "object"
      },
      "WalletError": {
        "additionalProperties": false,
        "description": "A wallet error response.",
        "properties": {
          "message": {
            "example": "travel_rule_info is missing",
            "type": "string"
          }
        },
        "required": [
          "message"
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
    "/v2/wallets/whitelists/{whitelisted_address_id}/travel-rule-info": {
      "parameters": [
        {
          "description": "The whitelisted address update travel rule information for",
          "in": "path",
          "name": "whitelisted_address_id",
          "required": true,
          "schema": {
            "format": "uuid",
            "type": "string"
          }
        }
      ],
      "patch": {
        "description": "You are required to supply travel rule information for the crypto wallets you're withdrawing to.\n\nIt is preferred that you use the `Search VASPs` endpoint to find the VASP DID for the exchange you are withdrawing to,\notherwise, if it's a self-hosted wallet, please set `beneficiary_is_self_hosted` to true.\n\nIf the exchange cannot be found in our directory, please supply the information manually using the `beneficiary_manual_entry` object.",
        "operationId": "updateWhitelistedAddressTravelRuleInfo",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UpdateWhitelistedAddressTravelRuleInfoRequest"
              }
            }
          },
          "description": "Travel rule information to associate with the whitelisted address.",
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successfully updated travel rule information"
          },
          "400": {
            "content": {
              "application/json": {
                "examples": {
                  "TravelRuleValidationError": {
                    "$ref": "#/components/examples/TravelRuleValidationError"
                  },
                  "WalletError": {
                    "value": {
                      "message": "travel_rule_info is missing"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/TravelRuleErrorResponse"
                }
              }
            },
            "description": "The request or travel rule information is invalid."
          }
        },
        "summary": "Update travel rule information for a whitelisted wallet",
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