# Initiate an incoming transfer

Source: https://docs.alpaca.markets/us/reference/requestacatstransfer.md

---
updatedAt: 2026-06-23T06:50:20.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Initiate an incoming transfer

This endpoint allows you to create new incoming ACATS requests. We currently support full and partial transfer types, for US equities and cash. Note that after submitting a request, it might take some time for the transfer to show up on the other endpoints. Transfers are not immediately sent to DTCC, and will appear in the `PENDING` state initially.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "AcatsCashBalance": {
        "description": "Cash balance",
        "example": {
          "amount": "10000",
          "currency": "USD"
        },
        "properties": {
          "amount": {
            "description": "Amount of cash to be transferred. Can be positive or negative. Use `transfer_all` to transfer the entire balance instead of specifying an amount -- `amount` and `transfer_all: true` are mutually exclusive, and sending both is rejected with HTTP 400.",
            "format": "decimal",
            "type": "string"
          },
          "currency": {
            "description": "Currency of the cash balance. Only `USD` is currently supported; any other value is rejected with HTTP 400. Each currency may appear at most once in the `cash` array.",
            "enum": [
              "USD"
            ],
            "type": "string"
          },
          "transfer_all": {
            "description": "Set to true to transfer the entire balance of this currency. Must not be combined with `amount`. Setting it to `false` without an `amount` is rejected with HTTP 400.",
            "type": "boolean"
          }
        },
        "required": [
          "currency"
        ],
        "type": "object"
      },
      "AcatsContraAccountDetails": {
        "description": "Contra account details",
        "example": {
          "account_number": "12345678A",
          "broker_number": "1234",
          "customer_name": "John Smith",
          "customer_tax_id": "911923333"
        },
        "properties": {
          "account_number": {
            "description": "Account number at the contra broker",
            "type": "string"
          },
          "broker_name": {
            "description": "Name of the contra broker (non-functional, used for auditability and display purposes)",
            "maxLength": 100,
            "minLength": 1,
            "type": "string"
          },
          "broker_number": {
            "description": "Clearing number of the contra broker",
            "type": "string"
          },
          "customer_name": {
            "description": "Name on the account at the contra broker",
            "type": "string"
          },
          "customer_tax_id": {
            "description": "Tax ID on the account at the contra broker",
            "type": "string"
          }
        },
        "required": [
          "account_number",
          "customer_name",
          "customer_tax_id",
          "broker_number"
        ],
        "type": "object"
      },
      "AcatsEquity": {
        "description": "Equity asset requested in a partial transfer. Identify the security with either `cusip` or `symbol` -- provide one, not both. Prefer `cusip` when you have it: it is a stable, unambiguous identifier. Use `symbol` only when a CUSIP is not available, as ticker symbols can change or be reused over time.",
        "example": {
          "position": "LONG",
          "qty": "2",
          "symbol": "AAPL"
        },
        "oneOf": [
          {
            "required": [
              "cusip",
              "position"
            ]
          },
          {
            "required": [
              "symbol",
              "position"
            ]
          }
        ],
        "properties": {
          "cusip": {
            "description": "CUSIP security identifier for the asset -- 8 uppercase alphanumeric characters followed by a check character, which may be a digit or one of `*`, `@`, `#`. Recommended over `symbol` for unambiguous identification. Provide either `cusip` or `symbol`, not both.",
            "pattern": "^[0-9A-Z]{8}[0-9*@#]$",
            "type": "string"
          },
          "position": {
            "description": "Position type. Only `LONG` and `SHORT` are accepted for equities -- `CREDIT` and `DEBIT` apply to cash positions and are rejected with HTTP 400 here.",
            "enum": [
              "LONG",
              "SHORT"
            ],
            "type": "string"
          },
          "qty": {
            "description": "Quantity of assets to transfer. Use `transfer_all` to transfer the entire position instead of specifying a quantity -- `qty` and `transfer_all: true` are mutually exclusive, and sending both is rejected with HTTP 400. Note that the ACATS system will only transfer whole shares.",
            "format": "decimal",
            "type": "string"
          },
          "symbol": {
            "description": "Stock ticker symbol (e.g. `AAPL`, `BRK.B`, `GOOGL`). Up to 6 alphanumeric characters, optionally followed by a single `.` or `-` separator and a 1-5 letter suffix. Values are trimmed and upper-cased before validation. Use only when a CUSIP is not available, since symbols can change or be reused over time. Provide either `cusip` or `symbol`, not both.",
            "pattern": "^[A-Z0-9]{1,6}([-.][A-Z]{1,5})?$",
            "type": "string"
          },
          "transfer_all": {
            "description": "Set to true to transfer the entire balance of this asset. Must not be combined with `qty`. Setting it to `false` without a `qty` is rejected with HTTP 400.",
            "type": "boolean"
          }
        },
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
      "AcatsInitiateTransferDetails": {
        "description": "Transfer details. The two transfer types are mutually exclusive in what they accept:\n- `FULL`: do not include the `cash` or `securities` objects (the entire account will be transferred). Including either is rejected with HTTP 400.\n- `PARTIAL`: specify which assets to transfer using the `cash` and/or `securities` objects. At least one of the two must be present and non-empty, otherwise the request is rejected with HTTP 400.\n",
        "example": {
          "cash": [
            {
              "amount": "10000",
              "currency": "USD"
            }
          ],
          "securities": {
            "equities": [
              {
                "cusip": "037833100",
                "position": "LONG",
                "qty": "2"
              },
              {
                "cusip": "78462F103",
                "position": "SHORT"
              }
            ]
          },
          "type": "PARTIAL"
        },
        "oneOf": [
          {
            "description": "Transfers the entire account. Must not carry `cash` or `securities`.",
            "not": {
              "anyOf": [
                {
                  "required": [
                    "cash"
                  ]
                },
                {
                  "required": [
                    "securities"
                  ]
                }
              ]
            },
            "properties": {
              "type": {
                "enum": [
                  "FULL"
                ],
                "type": "string"
              }
            },
            "title": "Full transfer"
          },
          {
            "anyOf": [
              {
                "properties": {
                  "cash": {
                    "minItems": 1,
                    "type": "array"
                  }
                },
                "required": [
                  "cash"
                ]
              },
              {
                "properties": {
                  "securities": {
                    "properties": {
                      "equities": {
                        "minItems": 1,
                        "type": "array"
                      }
                    },
                    "required": [
                      "equities"
                    ],
                    "type": "object"
                  }
                },
                "required": [
                  "securities"
                ]
              }
            ],
            "description": "Transfers selected assets. Must carry a non-empty `cash` array, a non-empty `securities.equities` array, or both.",
            "properties": {
              "type": {
                "enum": [
                  "PARTIAL"
                ],
                "type": "string"
              }
            },
            "title": "Partial transfer"
          }
        ],
        "properties": {
          "cash": {
            "description": "Cash amounts to transfer. Only used for PARTIAL transfers. Must not be included for FULL transfers.",
            "items": {
              "$ref": "#/components/schemas/AcatsCashBalance"
            },
            "type": "array"
          },
          "securities": {
            "allOf": [
              {
                "description": "Securities to transfer. Only used for PARTIAL transfers. Must not be included for FULL transfers."
              },
              {
                "$ref": "#/components/schemas/AcatsSecurities"
              }
            ]
          },
          "type": {
            "$ref": "#/components/schemas/AcatsInitiateTransferType"
          }
        },
        "required": [
          "type"
        ],
        "type": "object"
      },
      "AcatsInitiateTransferRequest": {
        "description": "Request body for initiating an incoming ACATS transfer.",
        "example": {
          "contra_account_details": {
            "account_number": "A00000123",
            "broker_number": "0158",
            "customer_name": "Jane Doe",
            "customer_tax_id": "123456789"
          },
          "ip_address": "203.0.113.42",
          "signed_at": "2026-04-29T13:00:00Z",
          "transfer_details": {
            "cash": [
              {
                "amount": "10000",
                "currency": "USD"
              }
            ],
            "securities": {
              "equities": [
                {
                  "position": "LONG",
                  "qty": "2",
                  "symbol": "AAPL"
                },
                {
                  "cusip": "123456789",
                  "position": "LONG",
                  "qty": "5"
                },
                {
                  "position": "SHORT",
                  "symbol": "TSLA"
                }
              ]
            },
            "type": "PARTIAL"
          }
        },
        "properties": {
          "contra_account_details": {
            "$ref": "#/components/schemas/AcatsContraAccountDetails"
          },
          "ip_address": {
            "description": "IP address from which the account holder initiated the transfer (IPv4 or IPv6)",
            "example": "203.0.113.42",
            "type": "string"
          },
          "signed_at": {
            "description": "Timestamp at which the account holder signed/authorized the transfer. Must be within the last week and must not be in the future (a 5 minute grace period absorbs clock skew); values outside that window are rejected with HTTP 400.",
            "example": "2026-04-29T13:00:00Z",
            "format": "date-time",
            "type": "string"
          },
          "transfer_details": {
            "$ref": "#/components/schemas/AcatsInitiateTransferDetails"
          },
          "validate_account_number": {
            "default": false,
            "description": "Whether to validate the contra account number against the contra broker's configured format rules. Defaults to false (no per-broker format check). Set to true to opt in, in which case a number that matches none of the broker's enabled rules is rejected with HTTP 422.",
            "type": "boolean"
          }
        },
        "required": [
          "contra_account_details",
          "transfer_details",
          "ip_address",
          "signed_at"
        ],
        "type": "object"
      },
      "AcatsInitiateTransferResponse": {
        "description": "Response returned when an ACATS transfer has been accepted for processing.",
        "properties": {
          "acats_id": {
            "description": "The ID of the ACATS transfer that was just initiated",
            "example": "2c827687-ddd3-4ad9-bee8-0a3cdad35301",
            "type": "string"
          }
        },
        "required": [
          "acats_id"
        ],
        "type": "object"
      },
      "AcatsInitiateTransferType": {
        "description": "Transfer type",
        "enum": [
          "FULL",
          "PARTIAL"
        ],
        "type": "string"
      },
      "AcatsSecurities": {
        "description": "List of securities to transfer",
        "properties": {
          "equities": {
            "items": {
              "$ref": "#/components/schemas/AcatsEquity"
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
    "/v1beta1/acats/{account_id}": {
      "post": {
        "description": "This endpoint allows you to create new incoming ACATS requests. We currently support full and partial transfer types, for US equities and cash. Note that after submitting a request, it might take some time for the transfer to show up on the other endpoints. Transfers are not immediately sent to DTCC, and will appear in the `PENDING` state initially.",
        "operationId": "requestACATSTransfer",
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
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/AcatsInitiateTransferRequest"
              }
            }
          },
          "description": "Details of the incoming ACATS transfer to initiate.",
          "required": true
        },
        "responses": {
          "202": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsInitiateTransferResponse"
                }
              }
            },
            "description": "Accepted"
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Bad Request"
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
          "422": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AcatsError"
                }
              }
            },
            "description": "Unprocessable Entity. Returned when:\n- the cleansed contra account number contains no digit at all;\n- `validate_account_number` is `true` and the contra account number matches none of the contra broker's enabled format rules;\n- the calling correspondent is pending migration, in which case the account is treated as being in distribution.\n"
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
        "summary": "Initiate an incoming transfer",
        "tags": [
          "ACATS"
        ],
        "x-readme": {
          "code-samples": [
            {
              "code": "curl --request POST \\\n  --url https://broker-api.alpaca.markets/v1beta1/acats/{account_id} \\\n  -u \"$BROKER_API_KEY:$BROKER_API_SECRET\" \\\n  --header 'content-type: application/json' \\\n  --data '{\n    \"contra_account_details\": {\n      \"broker_number\": \"0158\",\n      \"account_number\": \"A00000123\",\n      \"customer_name\": \"Jane Doe\",\n      \"customer_tax_id\": \"123456789\"\n    },\n    \"transfer_details\": {\n      \"type\": \"PARTIAL\",\n      \"cash\": [\n        { \"amount\": \"10000\", \"currency\": \"USD\" }\n      ],\n      \"securities\": {\n        \"equities\": [\n          { \"symbol\": \"AAPL\", \"qty\": \"2\", \"position\": \"LONG\" },\n          { \"cusip\": \"123456789\", \"qty\": \"5\", \"position\": \"LONG\" },\n          { \"symbol\": \"TSLA\", \"position\": \"SHORT\" }\n        ]\n      }\n    },\n    \"ip_address\": \"203.0.113.42\",\n    \"signed_at\": \"2026-04-29T13:00:00Z\"\n  }'",
              "language": "shell",
              "name": "Partial transfer (cash + equities)"
            },
            {
              "code": "curl --request POST \\\n  --url https://broker-api.alpaca.markets/v1beta1/acats/{account_id} \\\n  -u \"$BROKER_API_KEY:$BROKER_API_SECRET\" \\\n  --header 'content-type: application/json' \\\n  --data '{\n    \"contra_account_details\": {\n      \"broker_number\": \"0158\",\n      \"account_number\": \"A00000123\",\n      \"customer_name\": \"Jane Doe\",\n      \"customer_tax_id\": \"123456789\"\n    },\n    \"transfer_details\": { \"type\": \"FULL\" },\n    \"ip_address\": \"203.0.113.42\",\n    \"signed_at\": \"2026-04-29T13:00:00Z\"\n  }'",
              "language": "shell",
              "name": "Full transfer (entire account)"
            }
          ]
        }
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