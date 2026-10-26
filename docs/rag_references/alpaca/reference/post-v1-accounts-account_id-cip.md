# Upload CIP information

Source: https://docs.alpaca.markets/us/reference/post-v1-accounts-account_id-cip.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Upload CIP information

The customer identification program (CIP) API allows you to submit the CIP results received from your KYC provider.

The minimum requirements to open an individual financial account are delimited and you must verify the true identity of the account holder at account opening:

Name
Date of birth
Address
Identification number (for a U.S. citizen, a taxpayer identification number)

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CIPDocument": {
        "description": "Represents results of checking a document for CIPInfo\n",
        "examples": [
          {
            "created_at": "2021-06-10T15:37:03Z",
            "id": "55B9931A-3BE6-4BC0-9BDD-0B954E4A4632",
            "image_integrity": "clear",
            "result": "clear",
            "status": "complete"
          }
        ],
        "properties": {
          "age_validation": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "comprised_document": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "created_at": {
            "description": "Datetime for when this check was done",
            "format": "date-time",
            "type": "string"
          },
          "data_comparison": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "data_comparison_breakdown": {
            "description": "json object representing the results of the various sub-checks\n          done when calculating the result on `data_comparison`. Example: {\"date_of_birth\": \"clear\",\n          \"date_of_expiry\": \"clear\" \"document_numbers\": \"clear\", \"document_type\": \"clear\", \"first_name\": \"clear\",\n          \"gender\": \"clear\", \"issuing_country\": \"clear\", \"last_name\": \"clear\"}",
            "type": "string"
          },
          "date_of_birth": {
            "description": "Datetime for when this check was done",
            "format": "date",
            "type": "string"
          },
          "date_of_expiry": {
            "description": "Datetime for when this check was done",
            "format": "date",
            "type": "string"
          },
          "document_numbers": {
            "description": "Number of the document that was checked",
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "document_type": {
            "description": "Type of the document that was checked",
            "type": "string"
          },
          "first_name": {
            "description": "First name extracted from the document",
            "type": "string"
          },
          "gender": {
            "description": "Gender info extracted from the document",
            "type": "string"
          },
          "id": {
            "description": "Your internal ID of check",
            "type": "string"
          },
          "image_integrity": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "image_integrity_breakdown": {
            "description": "json object representing the results of the various sub-checks done\n          when calculating the result on `image_integrity`. Example: example: {\"colour_picture\": \"clear\",\n          \"conclusive_document_quality\": \"clear\", \"image_quality\": \"clear\", \"supported_document\": \"clear\"}",
            "type": "string"
          },
          "issuing_country": {
            "description": "Country for which issued the document",
            "type": "string"
          },
          "last_name": {
            "description": "Last name extracted from the document",
            "type": "string"
          },
          "nationality": {
            "description": "Nationality extracted from the document",
            "type": "string"
          },
          "police_record": {
            "$ref": "#/components/schemas/CIPStatus"
          },
          "result": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "status": {
            "$ref": "#/components/schemas/CIPStatus"
          },
          "visual_authenticity": {
            "description": "json object representing the various sub-checks done when determining\n          whether visual (non-textual) elements are correct given the document type. Example: {\n          \"digital_tampering\": \"clear\", \"face_detection\": \"clear\", \"fonts\": \"clear\", \"original_document_present\":\n          \"clear\", \"picture_face_integrity\": \"clear\", \"security_features\": \"clear\", \"template\": \"clear\"}",
            "type": "string"
          }
        },
        "required": [
          "id"
        ],
        "type": "object"
      },
      "CIPIdentity": {
        "examples": [
          {
            "address": "clear",
            "created_at": "2021-06-10T15:37:03Z",
            "date_of_birth": "clear",
            "id": "28E1CCE8-1B1A-4472-9AD4-C6C5B7C3A6AF",
            "result": "clear",
            "sources": "clear",
            "status": "complete"
          }
        ],
        "properties": {
          "address": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "address_breakdown": {
            "description": "a json object representing the breakdown of the `address` field. For example:\n          {\"credit_agencies\": {\"result\": \"clear\",\"properties\":{\"number_of_matches\":\"1\"}}",
            "type": "string"
          },
          "created_at": {
            "description": "datetime when identity check happened",
            "type": "string"
          },
          "date_of_birth": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "date_of_birth_breakdown": {
            "description": "a json object representing the breakdown of the `date_of_birth` field.\n          For example: example: {\"credit_agencies\":{\"result\": \"clear\",\"properties\": {\"number_of_matches\": \"1\"}}",
            "type": "string"
          },
          "id": {
            "description": "Your internal ID of check",
            "type": "string"
          },
          "matched_address": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "matched_addresses": {
            "description": "datetime when identity check happened",
            "type": "string"
          },
          "result": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "sources": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "sources_breakdown": {
            "description": "a json object representing the breakdown of `sources` field. For example:\n          {\"total_sources\": {\"result\": \"clear\",\"properties\": {\"total_number_of_sources\": \"3\"}}}",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/CIPStatus"
          },
          "tax_id": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "tax_id_breakdown": {
            "description": "a json object representing the breakdown of the `tax_id` field",
            "type": "string"
          }
        },
        "required": [
          "id"
        ],
        "type": "object"
      },
      "CIPInfo": {
        "description": "Customer Identification Program (CIP) information for an account applicant.",
        "properties": {
          "account_id": {
            "description": "UUID of the Account instance this CIPInfo is for",
            "format": "uuid",
            "type": "string"
          },
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "document": {
            "$ref": "#/components/schemas/CIPDocument"
          },
          "id": {
            "description": "ID of this CIPInfo",
            "format": "uuid",
            "type": "string"
          },
          "identity": {
            "$ref": "#/components/schemas/CIPIdentity"
          },
          "kyc": {
            "$ref": "#/components/schemas/CIPKYC"
          },
          "photo": {
            "$ref": "#/components/schemas/CIPPhoto"
          },
          "provider_name": {
            "description": "List of KYC providers this information came from",
            "items": {
              "$ref": "#/components/schemas/CIPProvider"
            },
            "type": "array"
          },
          "updated_at": {
            "format": "date-time",
            "type": "string"
          },
          "watchlist": {
            "$ref": "#/components/schemas/CIPWatchlist"
          }
        },
        "title": "CIPInfo",
        "type": "object"
      },
      "CIPKYC": {
        "description": "Represents Know Your Customer (KYC) info for a CIPInfo",
        "examples": [
          {
            "address": "42 Faux St",
            "applicant_name": "John Doe",
            "approval_status": "approved",
            "approved_at": "2021-06-10T15:38:03Z",
            "approved_by": "Jane Doe",
            "check_completed_at": "2021-06-10T15:37:03Z",
            "check_initiated_at": "2021-06-10T15:37:03Z",
            "country_of_residency": "USA",
            "date_of_birth": "1970-12-01",
            "email_address": "johndoe@example.com",
            "id": "CBDAD1C4-1047-450E-BAE5-B6C406F509B4",
            "id_number": "jd0000123456789",
            "ip_address": "127.0.0.1",
            "kyc_completed_at": "2021-06-10T15:37:03Z",
            "nationality": "American",
            "postal_code": "94401",
            "risk_level": "LOW"
          }
        ],
        "properties": {
          "address": {
            "description": "Concatenated street address, city, state and country of applicant",
            "type": "string"
          },
          "applicant_name": {
            "description": "Given and family name of applicant",
            "type": "string"
          },
          "approval_status": {
            "description": "Approval status of KYC check",
            "enum": [
              "approved",
              "rejected"
            ],
            "example": "approved",
            "type": "string"
          },
          "approved_at": {
            "description": "Reason for approving this KYC check",
            "format": "date-time",
            "type": "string"
          },
          "approved_by": {
            "description": "Identifier of who approved KYC check",
            "type": "string"
          },
          "approved_reason": {
            "description": "Datetime that this KYC check was approved",
            "type": "string"
          },
          "check_completed_at": {
            "description": "completion datetime of KYC check",
            "format": "date-time",
            "type": "string"
          },
          "check_initiated_at": {
            "description": "start datetime of KYC check",
            "format": "date-time",
            "type": "string"
          },
          "country_of_residency": {
            "description": "country for `address` field",
            "type": "string"
          },
          "date_of_birth": {
            "description": "DOB of applicant",
            "format": "date",
            "type": "string"
          },
          "email_address": {
            "description": "email address of applicant",
            "type": "string"
          },
          "id": {
            "description": "Your internal ID of check",
            "format": "uuid",
            "type": "string"
          },
          "ip_address": {
            "description": "IP address of applicant at time of KYC check",
            "type": "string"
          },
          "kyc_completed_at": {
            "description": "Datetime that KYC check was completed at",
            "format": "date-time",
            "type": "string"
          },
          "nationality": {
            "description": "nationality of applicant",
            "type": "string"
          },
          "postal_code": {
            "description": "postal code for `address` field",
            "type": "string"
          },
          "risk_categories": {
            "description": "The list of risk categories returned by the KYC provider or assessed",
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "risk_level": {
            "description": "Overall risk level returned by KYC provider or assessed",
            "type": "string"
          },
          "risk_score": {
            "description": "Overall risk score returned by KYC provider or assessed",
            "type": "integer"
          }
        },
        "required": [
          "id"
        ],
        "title": "CIPKYCInfo",
        "type": "object"
      },
      "CIPPhoto": {
        "description": "Represents the results of checking a Photo for CIPInfo",
        "examples": [
          {
            "created_at": "2021-06-10T15:37:03Z",
            "face_comparison": "clear",
            "id": "0DD13020-F0FD-4B5A-B58F-BC1885E90A6D",
            "result": "clear",
            "status": "complete"
          }
        ],
        "properties": {
          "created_at": {
            "description": "datetime of when the check happened",
            "type": "string"
          },
          "face_comparison": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "face_comparison_breakdown": {
            "description": "a json object representing the breakdown of sub-checks done in\n          `face_comparison`. Example: {\"face_match\":{\"result\": \"clear\",\"properties\":{\"score\": \"80\"}}}",
            "type": "string"
          },
          "id": {
            "description": "Your internal ID of the check",
            "type": "string"
          },
          "image_integrity": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "image_integrity_breakdown": {
            "description": "a json object representing the breakdown of sub-checks done in\n          `image_integrity`. Example  {\"face_detected\":{\"result\": \"clear\"},\"source_integrity\": {\"result\": \"clear\"}}",
            "type": "string"
          },
          "result": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "status": {
            "description": "Overall status of the check. Either `complete` or `withdrawn`.",
            "enum": [
              "complete",
              "withdrawn"
            ],
            "type": "string"
          },
          "visual_authenticity": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "visual_authenticity_breakdown": {
            "description": "a json object representing the breakdown of sub-checks don in\n          `visual_authenticity`. Example {\"spoofing_detection\": {\"result\": \"clear\",\"properties\": {\"score\": \"26\"}}}}",
            "type": "string"
          }
        },
        "required": [
          "id"
        ],
        "type": "object"
      },
      "CIPProvider": {
        "description": "\"alloy\"   - ALLOY\n\"trulioo\" - TRULIOO\n\"onfido\"  - ONFIDO\n\"veriff\"  - VERIFF\n\"jumio\"   - JUMIO\n\"getmati\" - GETMATI",
        "title": "CIPProvider",
        "type": "string"
      },
      "CIPResult": {
        "description": "The result of the check. Either `clear` or `consider`.",
        "title": "CIPResult",
        "type": "string"
      },
      "CIPStatus": {
        "description": "An enum representing the status of the CIPInfo\n\n\"complete\"\n\n\"withdrawn\"",
        "title": "CIPStatus",
        "type": "string"
      },
      "CIPWatchlist": {
        "description": "Represents the result of checking to see if the applicant is in any watchlists for a CIPInfo",
        "examples": [
          {
            "adverse_media": "clear",
            "created_at": "2021-06-10T15:37:03Z",
            "id": "7572B870-EB4C-46A2-8B88-509194CCEE7E",
            "monitored_lists": "clear",
            "politically_exposed_person": "clear",
            "result": "clear",
            "sanction": "clear",
            "status": "complete"
          }
        ],
        "properties": {
          "adverse_media": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "created_at": {
            "description": "datetime when check happened",
            "type": "string"
          },
          "id": {
            "description": "Your internal ID of check",
            "type": "string"
          },
          "monitored_lists": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "politically_exposed_person": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "records": {
            "description": "a json object. Example [{\"text\": \"Record info\"}]",
            "type": "string"
          },
          "result": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "sanction": {
            "$ref": "#/components/schemas/CIPResult"
          },
          "status": {
            "$ref": "#/components/schemas/CIPStatus"
          }
        },
        "required": [
          "id"
        ],
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
    "/v1/accounts/{account_id}/cip": {
      "parameters": [
        {
          "in": "path",
          "name": "account_id",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ],
      "post": {
        "description": "The customer identification program (CIP) API allows you to submit the CIP results received from your KYC provider.\n\nThe minimum requirements to open an individual financial account are delimited and you must verify the true identity of the account holder at account opening:\n\nName\nDate of birth\nAddress\nIdentification number (for a U.S. citizen, a taxpayer identification number)",
        "operationId": "post-v1-accounts-account_id-cip",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CIPInfo"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "OK"
          }
        },
        "summary": "Upload CIP information",
        "tags": [
          "KYC"
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
      "name": "KYC"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```