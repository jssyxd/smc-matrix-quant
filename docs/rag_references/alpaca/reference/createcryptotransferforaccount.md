# Request a New Withdrawal

Source: https://docs.alpaca.markets/us/reference/createcryptotransferforaccount.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Request a New Withdrawal

Creates a withdrawal request. Note that outgoing withdrawals must be sent to a whitelisted address and you must whitelist addresses at least 24 hours in advance. If you attempt to withdraw funds to a non-whitelisted address then the transfer will be rejected.

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
      "CreateCryptoTransferRequest": {
        "properties": {
          "address": {
            "description": "The destination wallet address",
            "type": "string"
          },
          "amount": {
            "description": "The amount, denoted in the specified asset, to be withdrawn from the user's wallet",
            "type": "string"
          },
          "asset": {
            "description": "The crypto asset symbol, e.g. BTC, ETH, USDT.",
            "type": "string"
          },
          "chain": {
            "$ref": "#/components/schemas/CryptoChain"
          }
        },
        "required": [
          "amount",
          "address",
          "asset"
        ],
        "title": "CreateCryptoTransferRequest",
        "type": "object"
      },
      "CryptoChain": {
        "description": "Chain identifier for multi-chain crypto assets.",
        "enum": [
          "SOL",
          "ETH",
          "BTC",
          "XRP",
          "ARB"
        ],
        "example": "ETH",
        "type": "string"
      },
      "CryptoTransfer": {
        "description": "Transfers allow you to transfer assets into your end customer's account (deposits) or out (withdrawal).",
        "properties": {
          "amount": {
            "description": "Amount of transfer denominated in the underlying crypto asset",
            "type": "string"
          },
          "asset": {
            "description": "Symbol of crypto asset for given transfer (e.g. BTC)",
            "type": "string"
          },
          "chain": {
            "description": "Underlying network for given transfer",
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp when transfer was created",
            "format": "date-time",
            "type": "string"
          },
          "direction": {
            "$ref": "#/components/schemas/TransferDirection"
          },
          "fees": {
            "type": "string"
          },
          "from_address": {
            "description": "Originating address of the transfer",
            "type": "string"
          },
          "id": {
            "description": "The crypto transfer ID",
            "format": "uuid",
            "type": "string"
          },
          "network_fee": {
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/CryptoTransferStatus"
          },
          "to_address": {
            "description": "Destination address of the transfer",
            "type": "string"
          },
          "tx_hash": {
            "description": "On-chain transaction hash (e.g. 0xabc...xyz)",
            "type": "string"
          },
          "usd_value": {
            "description": "Equivalent USD value at time of transfer",
            "type": "string"
          }
        },
        "type": "object"
      },
      "CryptoTransferStatus": {
        "enum": [
          "PROCESSING",
          "FAILED",
          "COMPLETE"
        ],
        "example": "PROCESSING",
        "type": "string"
      },
      "TransferDirection": {
        "enum": [
          "INCOMING",
          "OUTGOING"
        ],
        "example": "INCOMING",
        "type": "string"
      },
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
    "/v2/wallets/transfers": {
      "post": {
        "deprecated": true,
        "description": "Creates a withdrawal request. Note that outgoing withdrawals must be sent to a whitelisted address and you must whitelist addresses at least 24 hours in advance. If you attempt to withdraw funds to a non-whitelisted address then the transfer will be rejected.",
        "operationId": "createCryptoTransferForAccount",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateCryptoTransferRequest"
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
                  "$ref": "#/components/schemas/CryptoTransfer"
                }
              }
            },
            "description": "Successfully requested a transfer."
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
                      "message": "asset cannot be empty"
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
        "summary": "Request a New Withdrawal",
        "tags": [
          "Crypto Funding"
        ],
        "x-deprecation": {
          "reason": "This endpoint is deprecated. Use the Alpaca web application to initiate withdrawals.",
          "since": "2026-07-09",
          "sunset": "2026-10-09"
        }
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