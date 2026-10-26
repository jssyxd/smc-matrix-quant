# Subscribe to Account Status Events (SSE)

Source: https://docs.alpaca.markets/us/reference/suscribetoaccountstatussse.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Subscribe to Account Status Events (SSE)

The accounts events API provides streaming of account changes as they occur, via SSE (server sent events). Past events can also be queried.

Events are generated for changes to the following account properties:
- account_blocked
- admin_configurations
- cash_interest
- crypto_status
- kyc_results
- options
- status
- trading_blocked

Only the changed properties are included in the event payload.

Query Parameter Rules:
- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead
- `since` is required if `until` specified
- `since_id` is required if `until_id` specified
- `since_ulid` is required if `until_ulid` specified
- `since`, `since_id` and `since_ulid` can't be used at the same time

Behavior:
This API supports querying a range of events, starting now or in the past. If the end of the range is in the future or not specified, the connection is kept open and future events are pushed.

To be specific:
- if `since`, `since_id` or `since_ulid` is not specified, this will not return any historic data
- if `until`, `until_id` or `until_ulid` is reached, the stream will end with a status of 200

---

Note for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.

If you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.


# OpenAPI definition

````json
{
  "components": {
    "schemas": {
      "AccountCashInterestEvent": {
        "description": "This property is included when the account's cash interest program had changed due to an enrollment, APR tier change, or unenrollment.\nThe from and to status or APR tier name will be included in the event, depending on the change.\n",
        "properties": {
          "apr_tier_name_from": {
            "description": "The APR tier name before the change",
            "type": "string"
          },
          "apr_tier_name_to": {
            "description": "The APR tier name after the change",
            "type": "string"
          },
          "currency": {
            "description": "The currency of the cash interest program that changed.",
            "example": "USD",
            "type": "string"
          },
          "status_from": {
            "description": "The cash_interest program status of the account before the change",
            "type": "string"
          },
          "status_to": {
            "description": "The cash_interest program status of the account after the change",
            "type": "string"
          }
        },
        "type": "object"
      },
      "AccountFPSLEvent": {
        "description": "This property is included when the account's FPSL information had changed due to an enrollment, tier change, or unenrollment.\nThe from and to status or tier id will be included in the event, depending on the change.\n",
        "properties": {
          "US": {
            "properties": {
              "status_from": {
                "description": "The FPSL program status of the account before the change",
                "type": "string"
              },
              "status_to": {
                "description": "The FPSL program status of the account after the change",
                "type": "string"
              },
              "tier_from": {
                "description": "The tier id before the change",
                "type": "string"
              },
              "tier_to": {
                "description": "The tier id after the change",
                "type": "string"
              }
            },
            "type": "object"
          }
        },
        "type": "object"
      },
      "AccountStatusEvent": {
        "description": "Represents a change to certain account properties, sent over the events streaming API.\n",
        "examples": [
          {
            "account_id": "4db36989-6565-4011-9126-39fe6b3d9bf6",
            "at": "2021-06-14T09:59:15.232782Z",
            "event_id": 122039,
            "event_ulid": "01F84ZC0H0Q1QN7XPNWX44HF5J",
            "status_from": "",
            "status_to": "APPROVED"
          }
        ],
        "properties": {
          "account_blocked": {
            "description": "If true the account was blocked, if false, the account got unblocked",
            "type": "boolean"
          },
          "account_id": {
            "description": "The unique identifier of the account that was changed",
            "minLength": 1,
            "type": "string"
          },
          "account_number": {
            "description": "The account number of the account that was changed",
            "minLength": 1,
            "type": "string"
          },
          "admin_configurations": {
            "$ref": "#/components/schemas/AdminConfigurationsEvent"
          },
          "at": {
            "description": "timestamp of event",
            "minLength": 1,
            "type": "string"
          },
          "cash_interest": {
            "$ref": "#/components/schemas/AccountCashInterestEvent"
          },
          "crypto_status_from": {
            "description": "account crypto_status changed from",
            "type": "string"
          },
          "crypto_status_to": {
            "description": "account crypto_status changed to",
            "type": "string"
          },
          "event_id": {
            "description": "Monotonically increasing 64-bit integer not available to new partners, and for backward compatibility purposes only; use `event_ulid` as the stable identifier where possible\n",
            "type": "integer"
          },
          "event_ulid": {
            "description": "lexically sortable, monotonically increasing character array",
            "format": "ulid",
            "type": "string"
          },
          "fpsl": {
            "$ref": "#/components/schemas/AccountFPSLEvent"
          },
          "kyc_results": {
            "$ref": "#/components/schemas/KYCResults"
          },
          "options": {
            "$ref": "#/components/schemas/OptionsApprovalEvent"
          },
          "reason": {
            "deprecated": true,
            "minLength": 1,
            "type": "string"
          },
          "status_from": {
            "description": "The account status before the change",
            "example": "APPROVED",
            "type": "string"
          },
          "status_to": {
            "description": "The account status after the change",
            "example": "ACTIVE",
            "type": "string"
          },
          "trading_blocked": {
            "description": "If true the account cannot trade going forward, if false, the ban has been lifed",
            "type": "boolean"
          }
        },
        "required": [
          "account_id",
          "at",
          "event_ulid"
        ],
        "title": "AccountStatusEvent",
        "type": "object"
      },
      "AdminConfigurationsEvent": {
        "description": "Represents a change to admin configurations, as broadcast over the **events** streaming API. Only fields whose value changed are included; unrelated update events will not include a flag that did not change.\n\nDepending on the type of the Admin Configuration, the sent event will behave differently. For bool flags we are only sending the new value.\n\nFor example, the following payload means that the disable_shorting flag was set to true:\n\n```\n{\n  \"disable_shorting\": true\n}\n```\n\nFor other data types, we are embedding the old and new values into the payload. For example changing the max_margin_multiplier from 4 to 1 will yield this payload:\n\n```\n{\n  \"max_margin_multiplier\": {\n    \"from\": 4,\n    \"to\": 1\n  }\n}\n```\n\nIntroducing an override value from the default will yield a null value as `from`. For example restricting the max_margin_multiplier to 1 from default will yield the following payload:\n\n```\n{\n  \"max_margin_multiplier\": {\n    \"from\": null,\n    \"to\": 1\n  }\n}\n```",
        "properties": {
          "acct_daily_transfer_limit": {
            "description": "The correspondent level daily transfer limit override was changed",
            "properties": {
              "from": {
                "description": "Old value of the daily transfer limit",
                "type": "string"
              },
              "to": {
                "description": "New value of the daily transfer limit",
                "type": "string"
              }
            },
            "type": "object"
          },
          "allow_instant_ach": {
            "description": "If true, the account is allowed to perform instant ACH",
            "type": "boolean"
          },
          "disable_algodash_access": {
            "description": "If true, the account is allowed to access algo dash",
            "type": "boolean"
          },
          "disable_api_key": {
            "description": "If true, the account's API key will be disabled",
            "type": "boolean"
          },
          "disable_crypto": {
            "description": "If true, the account is not allowed to trade cryptos",
            "type": "boolean"
          },
          "disable_day_trading": {
            "description": "If true, the account is not allowed to day trade (e.g. buy and sell the same security on the same day)",
            "type": "boolean"
          },
          "disable_fractional": {
            "description": "If true, the account cannot create orders for fractional share positions",
            "type": "boolean"
          },
          "disable_shorting": {
            "description": "If true the account is not allowed to create short position orders",
            "type": "boolean"
          },
          "incoming_transfers_blocked": {
            "description": "If true, incoming transfers to this account are rejected",
            "type": "boolean"
          },
          "max_margin_multiplier": {
            "description": "Max margin multiplier was changed by admin to this value",
            "properties": {
              "from": {
                "description": "Old value of margin multiplier",
                "type": "string"
              },
              "to": {
                "description": "New value of margin multiplier",
                "type": "string"
              }
            },
            "type": "object"
          },
          "max_options_trading_level": {
            "description": "Max options trading level was changed by admin to this value. It can be 0, 1, 2, or 3.",
            "properties": {
              "from": {
                "description": "Old value of max options trading level",
                "type": "string"
              },
              "to": {
                "description": "New value of max options trading level",
                "type": "string"
              }
            },
            "type": "object"
          },
          "outgoing_transfers_blocked": {
            "description": "If true, outgoing transfers from this account are rejected",
            "type": "boolean"
          },
          "restrict_to_liquidation_reasons": {
            "$ref": "#/components/schemas/RestrictToLiquidationReasons"
          }
        },
        "title": "AdminConfigurationsEvent",
        "type": "object"
      },
      "KYCResultType": {
        "description": "A KYC reason identifier used as a property name in `KYCResultTypeSet`. The set is extensible, so integrations must tolerate and preserve unrecognized values.",
        "examples": [
          "IDENTITY_VERIFICATION",
          "compromised_document"
        ],
        "title": "KYCResultType",
        "type": "string"
      },
      "KYCResultTypeSet": {
        "additionalProperties": {
          "maxProperties": 0,
          "type": "object"
        },
        "description": "A nullable set of KYC reason identifiers represented as property names with empty object values. See `KYCResults` for documented identifiers and interpretation guidance.",
        "examples": [
          null,
          {},
          {
            "IDENTITY_VERIFICATION": {},
            "WATCHLIST_HIT": {}
          }
        ],
        "propertyNames": {
          "$ref": "#/components/schemas/KYCResultType"
        },
        "title": "KYCResultTypeSet",
        "type": [
          "object",
          "null"
        ]
      },
      "KYCResults": {
        "description": "Holds information about the result of KYC.\n\n`accept`, `indeterminate`, and `reject` are nullable sets represented as objects. Each property name is a KYC reason identifier, and every property value is always an empty object (`{}`) carrying no nested data. For example:\n\n```json\n{\n  \"IDENTITY_VERIFICATION\": {},\n  \"WATCHLIST_HIT\": {}\n}\n```\n\nInterpret each reason together with its enclosing result category and `additional_information`.\n\nDocumented reason identifiers:\n- `IDENTITY_VERIFICATION`: A government-issued identity document is required to verify the account owner's identity.\n- `TAX_IDENTIFICATION`: A tax identification document is required to verify the account owner's tax identification number.\n- `ADDRESS_VERIFICATION`: Additional documentation, such as a government-issued ID or statement, may be required to verify the account owner's residential address.\n- `DATE_OF_BIRTH`: A government-issued identity document is required to verify the account owner's date of birth.\n- `SELFIE_VERIFICATION`: A live selfie of the account owner is required to verify identity.\n- `PEP`: The account owner disclosed politically exposed person status, and additional information may be required.\n- `FAMILY_MEMBER_PEP`: The account owner disclosed that an immediate family member is politically exposed, and additional information may be required.\n- `CONTROL_PERSON`: Additional company information may be required because the account owner disclosed a control position.\n- `AFFILIATED`: Additional firm information may be required because the account owner disclosed an affiliation with FINRA or an exchange.\n- `VISA_TYPE_OTHER`: The account owner's visa type and expiration date may be required because the submitted visa type was \"other.\"\n- `W8BEN_CORRECTION`: A new W-8BEN with corrected identifying information is required.\n- `COUNTRY_NOT_SUPPORTED`: The account owner's country of tax residence or legal residence is not supported for this account.\n- `WATCHLIST_HIT`: Watchlist screening returned a result that requires further review; no action is needed from the account owner unless separately requested.\n- `OTHER`: See `additional_information` for a custom message describing what is required from the account owner.\n- `OTHER_PARTNER`: See `additional_information` for a custom message intended for the Broker API partner.\n- `CITIZENSHIP_COUNTRY_NOT_SUPPORTED`: The account owner's country of citizenship is not supported for this account.\n- `DIFFERING_COUNTRY`: A submitted identity document was issued by a country different from the account owner's country of tax residence.\n- `WL_PEP_SCREENING`: Watchlist screening returned a result related to possible political exposure.\n- `WL_LEGAL_REGULATORY_WARNING`: Watchlist screening returned a legal or regulatory warning result.\n- `UNDER_MINIMUM_AGE`: The account owner does not meet the minimum age requirement for this account.\n- `PEP_FOREIGN`: The account owner disclosed foreign politically exposed person status, and additional information may be required.\n- `FAMILY_MEMBER_PEP_FOREIGN`: The account owner disclosed that an immediate family member has foreign politically exposed person status, and additional information may be required.\n- `DISCRETIONARY`: The account is designated for discretionary trading by a registered investment adviser and requires review.\n- `HIO`: Additional information and a declaration form may be required because the account owner disclosed being the head of an international organization.\n- `INTERNAL_CHECK`: A non-specific account-opening check contributed to the KYC outcome; no more specific reason is available.\n- `compromised_document`: The identity document check indicated that the document may be compromised.\n- `data_comparison`: Data extracted from the identity document did not pass comparison checks and requires review.\n- `image_integrity`: A document or selfie image did not pass image-integrity checks and requires review.\n\nThe set of reason identifiers is extensible, so integrations must tolerate and preserve unrecognized values.\n",
        "properties": {
          "accept": {
            "$ref": "#/components/schemas/KYCResultTypeSet"
          },
          "additional_information": {
            "description": "Used to display a custom message.",
            "type": "string"
          },
          "indeterminate": {
            "$ref": "#/components/schemas/KYCResultTypeSet"
          },
          "reject": {
            "$ref": "#/components/schemas/KYCResultTypeSet"
          },
          "summary": {
            "description": "Either `pass` or `fail`. Used to indicate if KYC has completed and passed or not. This field is used for internal purposes only.",
            "type": "string"
          }
        },
        "type": [
          "object",
          "null"
        ]
      },
      "OptionsApprovalEvent": {
        "description": "This property is included when the account's approved options level changes.\n",
        "properties": {
          "approved_level_from": {
            "description": "The approved options level before the change",
            "type": "integer"
          },
          "approved_level_to": {
            "description": "The approved options level after the change",
            "type": "integer"
          }
        },
        "type": "object"
      },
      "RestrictToLiquidationReasons": {
        "description": "Reasons why the liquidation only flag was set",
        "properties": {
          "ach_return": {
            "description": "Set when an incoming ACH transfer gets rejected",
            "type": "boolean"
          },
          "position_to_equity_ratio": {
            "description": "Set when the position to equity ration exceeds the maximum limit",
            "type": "boolean"
          },
          "unspecified": {
            "description": "Default value for unknown reason",
            "type": "boolean"
          }
        },
        "title": "RestrictToLiquidationReasons",
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
    "/v1/events/accounts/status": {
      "get": {
        "description": "The accounts events API provides streaming of account changes as they occur, via SSE (server sent events). Past events can also be queried.\n\nEvents are generated for changes to the following account properties:\n- account_blocked\n- admin_configurations\n- cash_interest\n- crypto_status\n- kyc_results\n- options\n- status\n- trading_blocked\n\nOnly the changed properties are included in the event payload.\n\nQuery Parameter Rules:\n- `since_id` and `until_id` are deprecated and available only to select broker partners; use `since_ulid` and `until_ulid` instead\n- `since` is required if `until` specified\n- `since_id` is required if `until_id` specified\n- `since_ulid` is required if `until_ulid` specified\n- `since`, `since_id` and `since_ulid` can't be used at the same time\n\nBehavior:\nThis API supports querying a range of events, starting now or in the past. If the end of the range is in the future or not specified, the connection is kept open and future events are pushed.\n\nTo be specific:\n- if `since`, `since_id` or `since_ulid` is not specified, this will not return any historic data\n- if `until`, `until_id` or `until_ulid` is reached, the stream will end with a status of 200\n\n---\n\nNote for people using the clients generated from this OAS spec. Currently OAS-3 doesn't have full support for representing SSE style responses from an API, so if you are using a generated client and don't specify a `since` and `until` there is a good chance the generated clients will hang waiting for the response to end.\n\nIf you require the streaming capabilities we recommend not using the generated clients for this specific usecase until the OAS-3 standards come to a consensus on how to represent this correctly in OAS-3.\n",
        "operationId": "suscribeToAccountStatusSSE",
        "parameters": [
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "since",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "Format: YYYY-MM-DD",
            "in": "query",
            "name": "until",
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "deprecated": true,
            "in": "query",
            "name": "since_id",
            "schema": {
              "type": "integer"
            },
            "x-deprecation": {
              "reason": "Use since_ulid instead.",
              "since": "2023-08-01",
              "sunset": "2027-02-15"
            }
          },
          {
            "deprecated": true,
            "in": "query",
            "name": "until_id",
            "schema": {
              "type": "integer"
            },
            "x-deprecation": {
              "reason": "Use until_ulid instead.",
              "since": "2023-08-01",
              "sunset": "2027-02-15"
            }
          },
          {
            "in": "query",
            "name": "since_ulid",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "until_ulid",
            "schema": {
              "format": "ulid",
              "type": "string"
            }
          },
          {
            "in": "query",
            "name": "id",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "text/event-stream": {
                "examples": {},
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/AccountStatusEvent"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Connected. Events will now start streaming as long as you keep the connection open."
          }
        },
        "summary": "Subscribe to Account Status Events (SSE)",
        "tags": [
          "Events"
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
      "name": "Events"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
````