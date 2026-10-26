# Create an Account

Source: https://docs.alpaca.markets/us/reference/createaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Create an Account

Create an account for a new or existing account holder. Required fields, eligibility, and initial status depend on the account type, enabled assets, and your correspondent configuration. Account status changes are available through the Account Status Events stream.

To create an account for an existing holder, provide `primary_account_holder_id` instead of inline holder information. Among the documented account types, existing holders are supported for trading and IRA accounts. Donor-advised accounts instead reference an existing legal entity with `entity_id`.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "Account": {
        "description": "Represents high level account info. Used when returning entire account information would not be useful like the getAllAccounts operation",
        "examples": [
          {
            "account_number": "9034005019",
            "created_at": "2019-09-30T23:55:31.185998Z",
            "currency": "USD",
            "id": "0d18ae51-3c94-4511-b209-101e1666416b",
            "last_equity": "1500.65",
            "primary_account_holder_id": null,
            "status": "APPROVED"
          }
        ],
        "properties": {
          "account_number": {
            "description": "A human-readable account number that can be shown to the end user",
            "type": [
              "string",
              "null"
            ]
          },
          "account_type": {
            "$ref": "#/components/schemas/AccountType"
          },
          "agreements": {
            "items": {
              "$ref": "#/components/schemas/Agreement"
            },
            "type": "array"
          },
          "allow_instant_ach": {
            "description": "Determines whether the account is enabled for Instant ACH by the partner.",
            "type": "boolean"
          },
          "cash_interest": {
            "$ref": "#/components/schemas/AccountCashInterestResponse"
          },
          "contact": {
            "$ref": "#/components/schemas/Contact"
          },
          "created_at": {
            "description": "Timestamp (RFC3339) of account creation.",
            "format": "date-time",
            "type": "string"
          },
          "crypto_status": {
            "$ref": "#/components/schemas/AccountStatus"
          },
          "currency": {
            "$ref": "#/components/schemas/Currency"
          },
          "disclosures": {
            "$ref": "#/components/schemas/Disclosures"
          },
          "documents": {
            "description": "The documents associated with the primary owner of the account",
            "items": {
              "$ref": "#/components/schemas/OwnerDocument"
            },
            "type": "array"
          },
          "enabled_assets": {
            "description": "Assets the user has enabled and is able to trade once status and/or crypto_status are ACTIVE",
            "items": {
              "$ref": "#/components/schemas/EnabledAssetClass"
            },
            "type": "array"
          },
          "fpsl": {
            "$ref": "#/components/schemas/AccountFPSLResponse"
          },
          "id": {
            "description": "UUID that identifies the account for later reference",
            "format": "uuid",
            "type": "string"
          },
          "identity": {
            "$ref": "#/components/schemas/Identity"
          },
          "instant_ach_blocked": {
            "description": "Indicates whether the account is blocked for Instant ACH by Alpaca. Defaults to false when the partner creates the account. If the partner has set allow_instant_ach to true but instant_ach_blocked is true, then the account is blocked for Instant ACH irrespective of the fact that the partner has it enabled.",
            "type": "boolean"
          },
          "last_equity": {
            "description": "EOD equity calculation (cash + long market value + short market value)",
            "format": "decimal",
            "type": "string"
          },
          "primary_account_holder_id": {
            "description": "UUID of the account's primary holder when available; otherwise `null`.",
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "status": {
            "$ref": "#/components/schemas/AccountStatus"
          },
          "trusted_contact": {
            "$ref": "#/components/schemas/TrustedContact"
          }
        },
        "required": [
          "id",
          "account_number",
          "status",
          "currency",
          "created_at",
          "last_equity"
        ],
        "type": "object"
      },
      "AccountCashInterestPost": {
        "description": "The configuration of the account's USD cash interest program when creating an account.\nIf cash_interest is not provided and there is a default APR tier defined, that tier will be used.\nTo enroll the account in a non-default APR tier, provide the cash_interest object with the desired apr_tier_name. The status should not be specified on enrollment.\nThe response will contain a status of PENDING_CHANGE. An event showing the status change to ACTIVE will be generated when the enrollment is complete.\n",
        "properties": {
          "USD": {
            "$ref": "#/components/schemas/AccountCashInterestProgram"
          }
        },
        "type": "object"
      },
      "AccountCashInterestProgram": {
        "properties": {
          "apr_tier_name": {
            "description": "The unique name of the APR tier for a specific program",
            "example": "gold",
            "type": "string"
          },
          "status": {
            "description": "The status of the account within a cash interest program. One of:\n- **ACTIVE**\nThe account is enrolled and eligible for idle cash to be swept at the end of day (EOD).\n- **INACTIVE**\nThe account is not enrolled due to it either not being eligible (e.g. the updated Alpaca Customer Agreement has not been signed), an APR tier needs to be assigned, or they have been unenrolled.\n- **PENDING_CHANGE**\nAn enrollment, APR Tier change, or unenrollment is in progress\n",
            "example": "ACTIVE",
            "type": "string"
          }
        },
        "type": "object"
      },
      "AccountCashInterestResponse": {
        "description": "The configuration and status of the account's USD cash interest program\n",
        "properties": {
          "USD": {
            "$ref": "#/components/schemas/AccountCashInterestProgram"
          }
        },
        "type": "object"
      },
      "AccountConfigurations": {
        "description": "Represents additional configuration settings for an account",
        "properties": {
          "disable_overnight_trading": {
            "description": "If true, overnight trading is disabled.",
            "type": "boolean"
          },
          "fractional_trading": {
            "description": "If true, account is able to participate in fractional trading",
            "type": "boolean"
          },
          "max_margin_multiplier": {
            "description": "Can be \"1\" or \"2\"",
            "type": "string"
          },
          "max_options_trading_level": {
            "description": "The desired maximum options trading level. 0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "type": "integer"
          },
          "no_shorting": {
            "description": "If true, account becomes long-only mode.",
            "type": "boolean"
          },
          "ptp_no_exception_entry": {
            "description": "If set to true then Alpaca will accept orders for PTP symbols with no exception. Default is false.",
            "type": "string"
          },
          "suspend_trade": {
            "description": "If true, new orders are blocked.",
            "type": "boolean"
          },
          "trade_confirm_email": {
            "description": "all or none. If none, emails for order fills are not sent.",
            "enum": [
              "all",
              "none"
            ],
            "type": "string"
          }
        },
        "title": "AccountConfigurations",
        "type": "object"
      },
      "AccountCreationRequest": {
        "description": "Fields accepted when creating an account. Requirements vary by account type, enabled assets, existing holder agreements, and correspondent configuration. The server enforces conditional requirements that are not represented statically in this schema.\n\nAccount-specific requirements:\n- Trading accounts require inline `identity` plus `contact`, or an existing holder through `primary_account_holder_id`. Individual US equity accounts created with inline identity also require `disclosures`.\n- Custodial accounts require `identity` and `minor_identity`. US equity accounts also require `disclosures`.\n- IRA accounts require `account_sub_type`, US equity, and either inline `identity` or an existing holder through `primary_account_holder_id`; they do not support crypto. IRA accounts created with inline identity also require `disclosures`.\n- Donor-advised accounts require `entity_id`.\n",
        "properties": {
          "account_sub_type": {
            "allOf": [
              {
                "$ref": "#/components/schemas/AccountSubType"
              }
            ],
            "description": "The account subtype. Required for IRA accounts."
          },
          "account_type": {
            "allOf": [
              {
                "$ref": "#/components/schemas/AccountCreationType"
              }
            ],
            "default": "trading",
            "description": "The account type. Defaults to `trading` when omitted."
          },
          "agreements": {
            "description": "Agreements submitted for the account or holder. Required agreement types depend on account type, enabled assets, existing holder agreements, and correspondent configuration. The server validates required coverage.",
            "items": {
              "$ref": "#/components/schemas/Agreement"
            },
            "type": "array"
          },
          "allow_instant_ach": {
            "default": false,
            "description": "Determines whether the account will be enabled for Instant ACH by the partner. Defaults to false if not provided.",
            "type": "boolean"
          },
          "beneficiaries": {
            "description": "IRA Account only. A user can submit max 6 beneficiaries.",
            "items": {
              "$ref": "#/components/schemas/Beneficiary"
            },
            "type": "array"
          },
          "cash_interest": {
            "$ref": "#/components/schemas/AccountCashInterestPost"
          },
          "contact": {
            "$ref": "#/components/schemas/Contact"
          },
          "disclosures": {
            "$ref": "#/components/schemas/Disclosures"
          },
          "documents": {
            "items": {
              "$ref": "#/components/schemas/OwnerDocumentUploadRequest"
            },
            "type": "array"
          },
          "enabled_assets": {
            "description": "Will default to `us_equity`. Alpaca has the ability to update the default value upon request.",
            "items": {
              "$ref": "#/components/schemas/EnabledAssetClass"
            },
            "type": "array"
          },
          "entity_id": {
            "description": "UUID of an existing legal entity used as the holder of a donor-advised account. Required for donor-advised accounts.",
            "format": "uuid",
            "type": "string"
          },
          "fpsl": {
            "$ref": "#/components/schemas/AccountFPSLPost"
          },
          "identity": {
            "$ref": "#/components/schemas/Identity"
          },
          "investment_objective": {
            "description": "The user's investment objective. This field should be used instead of the deprecated `investment_objective` under identity.\n",
            "enum": [
              "generate_income",
              "preserve_wealth",
              "market_speculation",
              "growth",
              "balance_preserve_wealth_with_growth"
            ],
            "type": "string"
          },
          "investment_time_horizon": {
            "description": "The expected period of time the user plan to invest to achieve his/her financial goal(s). This field should be used instead of the deprecated `investment_time_horizon` under identity.\n",
            "enum": [
              "less_than_1_year",
              "1_to_2_years",
              "3_to_5_years",
              "6_to_10_years",
              "more_than_10_years"
            ],
            "type": "string"
          },
          "liquidity_needs": {
            "description": "The user's ability to quickly and easily convert to cash all or a portion of the investments in this account without experiencing significant loss in value. This field should be used instead of the deprecated `liquidity_needs` under identity.\n",
            "enum": [
              "very_important",
              "important",
              "somewhat_important",
              "does_not_matter"
            ],
            "type": "string"
          },
          "minor_identity": {
            "allOf": [
              {
                "$ref": "#/components/schemas/CustodialAccountMinorIdentity"
              }
            ],
            "description": "Identity information for the minor. Required for custodial accounts."
          },
          "primary_account_holder_id": {
            "description": "UUID of an existing party to use as the primary account holder. Among the documented account types, existing holders are supported for trading and IRA accounts.\n\nWhen provided, omit inline holder fields such as `contact`, `identity`, `disclosures`, and `minor_identity`. The server validates the referenced party, account-type compatibility, eligibility, and required agreements.\n",
            "format": "uuid",
            "type": "string"
          },
          "risk_tolerance": {
            "description": "The user's investment risk tolerance. This field should be used instead of the deprecated `risk_tolerance` under identity.\n",
            "enum": [
              "conservative",
              "moderate",
              "significant_risk"
            ],
            "type": "string"
          },
          "trading_configurations": {
            "$ref": "#/components/schemas/AccountConfigurations"
          },
          "trusted_contact": {
            "$ref": "#/components/schemas/TrustedContact"
          }
        },
        "title": "AccountCreationRequest",
        "type": "object"
      },
      "AccountCreationType": {
        "description": "The account type to create.",
        "enum": [
          "trading",
          "custodial",
          "donor_advised",
          "ira"
        ],
        "example": "trading",
        "title": "AccountCreationType",
        "type": "string"
      },
      "AccountFPSLItem": {
        "properties": {
          "status": {
            "description": "The status of the account for this FPSL market. One of:\n- **ACTIVE**\nThe account is successfully enrolled for FPSL for this market.\n- **INACTIVE**\nThe account is not enrolled for FPSL for this market due to it either not being eligible, an FPSL tier has not been assigned, or it has been unenrolled.\n",
            "example": "ACTIVE",
            "type": "string"
          },
          "tier_id": {
            "description": "The id of the FPSL tier for this market",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          }
        },
        "type": "object"
      },
      "AccountFPSLItemPost": {
        "properties": {
          "tier_id": {
            "description": "The id of the FPSL tier for this market",
            "example": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "format": "uuid",
            "type": "string"
          }
        },
        "type": "object"
      },
      "AccountFPSLPost": {
        "description": "The account's Fully Paid Securities Lending (FPSL) configuration.\nTo enroll the account for a market, specify the tier_id. The status should not be specified on enrollment.\nCurrently only the US market is supported.\n",
        "properties": {
          "US": {
            "$ref": "#/components/schemas/AccountFPSLItemPost"
          }
        },
        "type": "object"
      },
      "AccountFPSLResponse": {
        "description": "The account's Fully Paid Securities Lending (FPSL) configuration.\nThis is only returned for accounts that have FPSL enabled.\n",
        "properties": {
          "US": {
            "$ref": "#/components/schemas/AccountFPSLItem"
          }
        },
        "type": "object"
      },
      "AccountStatus": {
        "description": "Designates the current status of this account\n\nPossible Values:\n- **INACTIVE**\nAccount not set to trade given asset.\n- **PAPER_ONLY**\nThe account is limited to paper trading.\n- **ONBOARDING**\nAn application is expected for this user, but has not been submitted yet.\n- **SUBMITTED**\nThe application has been submitted and is being processed.\n- **SUBMISSION_FAILED**\nUsed to display if failure on submission\n- **ACTION_REQUIRED**\nThe application requires manual action.\n- **ACCOUNT_UPDATED**\nUsed to display when Account has been modified by user\n- **APPROVAL_PENDING**\nInitial value. The application approval process is in progress.\n- **APPROVED**\nThe account application has been approved, and waiting to be ACTIVE\n- **REJECTED**\nThe account application is rejected for some reason\n- **ACTIVE**\nThe account is fully active. Trading and funding are processed under this status.\n- **ACCOUNT_CLOSED**\nThe account is closed.\n",
        "enum": [
          "INACTIVE",
          "PAPER_ONLY",
          "ONBOARDING",
          "SUBMITTED",
          "SUBMISSION_FAILED",
          "ACTION_REQUIRED",
          "ACCOUNT_UPDATED",
          "APPROVAL_PENDING",
          "APPROVED",
          "REJECTED",
          "ACTIVE",
          "ACCOUNT_CLOSED"
        ],
        "example": "ACTIVE",
        "type": "string"
      },
      "AccountSubType": {
        "description": "IRA Account only\n\nPossible values are:\n\n- traditional\n- roth",
        "enum": [
          "traditional",
          "roth"
        ],
        "example": "traditional",
        "title": "AccountSubType",
        "type": "string"
      },
      "AccountType": {
        "description": "The account type returned for the account.",
        "enum": [
          "trading",
          "custodial",
          "donor_advised",
          "ira",
          "trust",
          "omnibus_non_disclosed",
          "omnibus_sub",
          "hsa",
          "joint"
        ],
        "example": "trading",
        "title": "AccountType",
        "type": "string"
      },
      "Agreement": {
        "properties": {
          "agreement": {
            "$ref": "#/components/schemas/AgreementType"
          },
          "ip_address": {
            "description": "The ip_address the signed agreements were sent from by the user.",
            "example": "185.13.21.99",
            "format": "ipv4",
            "type": "string"
          },
          "revision": {
            "description": "The agreement revision.\nThe format is XX.YYYY.MM where XX is an incrementing revision number, YYYY is the year and MM is the month.\nIf the revision is not specified in a POST or PATCH request, the active revision will be used, which will align with the [Alpaca Documents Library](https://alpaca.markets/disclosures).\n",
            "type": "string"
          },
          "signed_at": {
            "description": "The timestamp the agreement was signed.",
            "example": "2019-09-11T18:09:33Z",
            "format": "date-time",
            "type": "string"
          }
        },
        "required": [
          "agreement",
          "signed_at",
          "ip_address"
        ],
        "type": "object"
      },
      "AgreementType": {
        "description": "- margin_agreement: Alpaca Margin Agreement\n- account_agreement: Alpaca Account Agreement\n- customer_agreement: Alpaca Customer Agreement\n- crypto_agreement: Alpaca Crypto agreement\n- options_agreement: Alpaca Option agreement\n- custodial_customer_agreement: Alpaca Custodial Customer agreement\n",
        "enum": [
          "margin_agreement",
          "account_agreement",
          "customer_agreement",
          "crypto_agreement",
          "options_agreement"
        ],
        "example": "customer_agreement",
        "title": "AgreementType",
        "type": "string"
      },
      "Beneficiary": {
        "description": "Beneficiary of an account",
        "example": {
          "date_of_birth": "1970-01-01",
          "family_name": "Doe",
          "given_name": "Jane",
          "middle_name": "P",
          "relationship": "spouse",
          "share_pct": "100",
          "tax_id": "xxx-xx-xxxx",
          "tax_id_type": "USA_SSN",
          "type": "primary"
        },
        "properties": {
          "date_of_birth": {
            "example": "1970-01-01",
            "type": "string"
          },
          "family_name": {
            "example": "Doe",
            "type": "string"
          },
          "given_name": {
            "example": "Jane",
            "type": "string"
          },
          "middle_name": {
            "example": "P",
            "type": "string"
          },
          "relationship": {
            "example": "spouse",
            "type": "string"
          },
          "share_pct": {
            "example": "100",
            "type": "string"
          },
          "tax_id": {
            "example": "xxx-xx-xxxx",
            "type": "string"
          },
          "tax_id_type": {
            "example": "USA_SSN",
            "type": "string"
          },
          "type": {
            "example": "primary",
            "type": "string"
          }
        },
        "required": [
          "given_name",
          "middle_name",
          "family_name",
          "date_of_birth",
          "tax_id",
          "tax_id_type",
          "relationship",
          "type",
          "share_pct"
        ],
        "type": "object"
      },
      "Contact": {
        "description": "Contact is the model for the account owner contact information.\n",
        "properties": {
          "city": {
            "example": "San Mateo",
            "type": "string"
          },
          "country": {
            "description": "country code in ISO 3166-1 alpha-3 format, representing the country the person/entity resides in.",
            "example": "USA",
            "type": "string"
          },
          "email_address": {
            "example": "john.doe@example.com",
            "format": "email",
            "type": "string"
          },
          "phone_number": {
            "description": "Phone number should include the country code, format: \"+15555555555\"",
            "example": "+15556667788",
            "type": [
              "string",
              "null"
            ]
          },
          "postal_code": {
            "example": "94401",
            "type": "string"
          },
          "state": {
            "description": "Required if the country or country_of_tax_residence (in the identity model below) is 'USA'.",
            "example": "CA",
            "type": "string"
          },
          "street_address": {
            "description": "The user's street address. If multiple lines in address, pass in as additional array elements. Maximum of 3 objects in array",
            "items": {
              "$ref": "#/components/schemas/StreetAddress"
            },
            "type": "array"
          },
          "unit": {
            "description": "The specific apartment number if applicable",
            "type": "string"
          }
        },
        "required": [
          "email_address",
          "street_address",
          "city"
        ],
        "type": "object"
      },
      "Currency": {
        "description": "\"USD\" // US Dollar\n\"JPY\" // Japanese Yen\n\"EUR\" // Euro\n\"CAD\" // Canadian Dollar\n\"GBP\" // British Pound Sterling\n\"CHF\" // Swiss Franc\n\"TRY\" // Turkish Lira\n\"AUD\" // Australian Dollar\n\"CZK\" // Czech Koruna\n\"SEK\" // Swedish Krona\n\"DKK\" // Danish Krone\n\"SGD\" // Singapore Dollar\n\"HKD\" // Hong Kong Dollar\n\"HUF\" // Hungarian Forint\n\"NZD\" // New Zealand Dollar\n\"NOK\" // Norwegian Krone\n\"PLN\" // Poland Złoty",
        "title": "Currency",
        "type": "string"
      },
      "CustodialAccountMinorIdentity": {
        "description": "Represents Identity information for a minor that an account of type \"custodial\" is for",
        "properties": {
          "country_of_birth": {
            "type": "string"
          },
          "country_of_citizenship": {
            "type": "string"
          },
          "country_of_tax_residence": {
            "type": "string"
          },
          "date_of_birth": {
            "format": "date",
            "type": "string"
          },
          "email": {
            "format": "email",
            "type": "string"
          },
          "family_name": {
            "type": "string"
          },
          "given_name": {
            "type": "string"
          },
          "state": {
            "type": "string"
          },
          "tax_id": {
            "type": "string"
          },
          "tax_id_type": {
            "$ref": "#/components/schemas/TaxIdType"
          }
        },
        "required": [
          "given_name",
          "family_name",
          "date_of_birth",
          "tax_id_type",
          "country_of_tax_residence",
          "state",
          "email"
        ],
        "type": "object"
      },
      "DisclosureContextAnnotation": {
        "properties": {
          "company_city": {
            "description": "Required for FINRA affiliations and controlled firms.",
            "type": "string"
          },
          "company_compliance_email": {
            "description": "Required for FINRA affiliations and controlled firms.",
            "type": "string"
          },
          "company_country": {
            "description": "Required for FINRA affiliations and controlled firms.",
            "type": "string"
          },
          "company_name": {
            "description": "Required for FINRA affiliations and controlled firms.",
            "type": "string"
          },
          "company_state": {
            "description": "Required if and only if `company_country` is `USA`.",
            "type": "string"
          },
          "company_street_address": {
            "description": "Required for FINRA affiliations and controlled firms.",
            "type": "string"
          },
          "context_type": {
            "description": "Specifies the type of disclosure annotation. Valid types are FINRA affiliations, for users affiliated with or employed by a FINRA member firm, a Stock Exchange Member, FINRA, Registered Investment Advisor, or a Municipal Securities Broker/Dealer; Company control relationships, for senior executives, and 10% or greater shareholders, of a publicly traded company; and immediate family members of politically exposed individuals.",
            "enum": [
              "CONTROLLED_FIRM",
              "IMMEDIATE_FAMILY_EXPOSED",
              "AFFILIATE_FIRM"
            ],
            "type": "string"
          },
          "family_name": {
            "description": "Required for immediate family members of politically exposed persons.",
            "type": "string"
          },
          "given_name": {
            "description": "Required for immediate family members of politically exposed persons.",
            "type": "string"
          }
        },
        "required": [
          "context_type"
        ],
        "title": "DisclosureContextAnnotation",
        "type": "object"
      },
      "Disclosures": {
        "description": "Disclosures fields denote if the account owner falls under\neach category defined by FINRA rule. The client has to ask\nquestions for the end user and the values should reflect\ntheir answers.\nIf one of the answers is true (yes), the account goes into\nACTION_REQUIRED status.\n",
        "example": {
          "immediate_family_exposed": false,
          "is_affiliated_exchange_or_finra": false,
          "is_control_person": false,
          "is_politically_exposed": false
        },
        "properties": {
          "context": {
            "description": "Array of annotations describing the rationale for marking `is_control_person`, `is_affiliated_exchange_or_finra`, and/or `immediate_family_exposed` as true",
            "items": {
              "$ref": "#/components/schemas/DisclosureContextAnnotation"
            },
            "type": [
              "array",
              "null"
            ]
          },
          "employer_address": {
            "description": "The employer's address if the user is employed.",
            "type": "string"
          },
          "employer_name": {
            "description": "The name of the employer if the user is employed.",
            "type": "string"
          },
          "employment_position": {
            "description": "The user's position if they are employed.",
            "type": "string"
          },
          "employment_sector": {
            "description": "The industry sector of employment.\nIf the `employment_status` is `unemployed` or `student`, set this property to `not_employed`.\nIf the `employment_status` is `retired`, set this to `self_employed`.\n",
            "enum": [
              "agriculture",
              "business_management",
              "computers_and_it",
              "construction",
              "education",
              "finance",
              "government",
              "healthcare",
              "hospitality",
              "manufacturing",
              "marketing",
              "media",
              "other",
              "science",
              "self_employed",
              "transportation",
              "not_employed"
            ],
            "type": "string"
          },
          "employment_status": {
            "description": "One of the following: `employed`, `unemployed`, `retired`, or `student`.",
            "enum": [
              "unemployed",
              "employed",
              "student",
              "retired"
            ],
            "type": "string"
          },
          "immediate_family_exposed": {
            "description": "If your user's immediate family member (sibling, husband/wife, child, parent) is either politically exposed or holds a control position.",
            "type": "boolean"
          },
          "is_affiliated_exchange_or_finra": {
            "description": "Whether user is affiliated with any exchanges or FINRA.",
            "type": "boolean"
          },
          "is_control_person": {
            "description": "Whether user holds a controlling position in a publicly traded company, member of the board of directors or has policy making abilities in a publicly traded company.",
            "type": "boolean"
          },
          "is_politically_exposed": {
            "description": "Whether the user is politically exposed.",
            "type": "boolean"
          }
        },
        "required": [
          "is_control_person",
          "is_affiliated_exchange_or_finra",
          "is_politically_exposed",
          "immediate_family_exposed"
        ],
        "type": "object"
      },
      "EnabledAssetClass": {
        "description": "An asset class that can be enabled on a brokerage account, i.e. a value that may appear in an account's `enabled_assets`. This differs from `AssetClass` (which also covers order and asset metadata) by excluding `ipo`, which is not an enable-able asset.",
        "enum": [
          "us_equity",
          "us_option",
          "crypto"
        ],
        "type": "string"
      },
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
      "Identity": {
        "description": "Identity is the model to provide account owner's identity information.\n",
        "example": {
          "country_of_birth": "AUS",
          "country_of_citizenship": "AUS",
          "country_of_tax_residence": "USA",
          "date_of_birth": "1990-01-01",
          "family_name": "Doe",
          "funding_source": [
            "employment_income"
          ],
          "given_name": "John",
          "tax_id": "666-55-4321",
          "tax_id_type": "USA_SSN"
        },
        "properties": {
          "annual_income_max": {
            "description": "The upper bound of the user's annual income.",
            "example": "100000",
            "format": "decimal",
            "type": "string"
          },
          "annual_income_min": {
            "description": "The lower bound of the user's annual income.",
            "example": "50000",
            "format": "decimal",
            "type": "string"
          },
          "country_of_birth": {
            "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
            "example": "USA",
            "type": "string"
          },
          "country_of_citizenship": {
            "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
            "example": "USA",
            "type": "string"
          },
          "country_of_tax_residence": {
            "description": "[ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html).\n",
            "example": "USA",
            "type": "string"
          },
          "date_of_birth": {
            "description": "The date of birth in \"YYYY-MM-DD\" format.",
            "example": "1990-01-01",
            "format": "date",
            "type": "string"
          },
          "date_of_departure_from_usa": {
            "description": "Required if `visa_type` = B1 or B2",
            "format": "date",
            "type": "string"
          },
          "family_name": {
            "description": "The last name (surname) of the user.",
            "example": "Doe",
            "type": "string"
          },
          "funding_source": {
            "description": "Can be one or more of the following: `employment_income`, `investments`, `inheritance`, `business_income`, `savings`, `family`.",
            "items": {
              "enum": [
                "employment_income",
                "investments",
                "inheritance",
                "business_income",
                "savings",
                "family"
              ],
              "type": "string"
            },
            "type": "array"
          },
          "given_name": {
            "description": "The first/given name of the user.",
            "example": "John",
            "type": "string"
          },
          "investment_experience_with_options": {
            "description": "The user's level of expertise and familiarity with investing in Options.\n",
            "enum": [
              "none",
              "1_to_5_years",
              "over_5_years"
            ],
            "type": "string"
          },
          "investment_experience_with_stocks": {
            "description": "The user's level of expertise and familiarity with investing in US Equities.\n",
            "enum": [
              "none",
              "1_to_5_years",
              "over_5_years"
            ],
            "type": "string"
          },
          "investment_objective": {
            "deprecated": true,
            "description": "The user's investment objective. This field is deprecated. Please use the top level `investment_objective` field.\n",
            "enum": [
              "generate_income",
              "preserve_wealth",
              "market_speculation",
              "growth",
              "balance_preserve_wealth_with_growth"
            ],
            "type": "string"
          },
          "investment_time_horizon": {
            "deprecated": true,
            "description": "The expected period of time the user plan to invest to achieve his/her financial goal(s). This field is deprecated. Please use the top level `investment_time_horizon` field.\n",
            "enum": [
              "less_than_1_year",
              "1_to_2_years",
              "3_to_5_years",
              "6_to_10_years",
              "more_than_10_years"
            ],
            "type": "string"
          },
          "liquid_net_worth_max": {
            "description": "The upper bound of the user's liquid net worth.",
            "example": "500000",
            "format": "decimal",
            "type": "string"
          },
          "liquid_net_worth_min": {
            "description": "The lower bound of the user's liquid net worth.",
            "example": "100000",
            "format": "decimal",
            "type": "string"
          },
          "liquidity_needs": {
            "deprecated": true,
            "description": "The user's ability to quickly and easily convert all or part of their investments in this account to cash without significant loss in value. This field is deprecated. Please use the top level `liquidity_needs` field.\n",
            "enum": [
              "very_important",
              "important",
              "somewhat_important",
              "does_not_matter"
            ],
            "type": "string"
          },
          "marital_status": {
            "description": "The marital status of the user.\n",
            "enum": [
              "SINGLE",
              "MARRIED",
              "DIVORCED",
              "WIDOWED"
            ],
            "type": "string"
          },
          "middle_name": {
            "description": "The middle name of the user.",
            "type": "string"
          },
          "number_of_dependents": {
            "description": "The number of dependents the user has.\n",
            "type": "integer"
          },
          "permanent_resident": {
            "description": "Only used to collect permanent residence status in the USA.",
            "type": "boolean"
          },
          "risk_tolerance": {
            "deprecated": true,
            "description": "The user's investment risk tolerance. This field is deprecated. Please use the top level `risk_tolerance` field.\n",
            "enum": [
              "conservative",
              "moderate",
              "significant_risk"
            ],
            "type": "string"
          },
          "tax_id": {
            "description": "If this is provided, `tax_id_type` is required.",
            "example": "666-55-4321",
            "type": "string"
          },
          "tax_id_type": {
            "description": "Required on write when `tax_id` is set. May be `null` on read when unset or for sparse identity on OmniSub / omnibus-non-disclosed accounts.",
            "oneOf": [
              {
                "$ref": "#/components/schemas/TaxIdType"
              },
              {
                "type": "null"
              }
            ]
          },
          "total_net_worth_max": {
            "description": "The upper bound of the user's total net worth.",
            "example": "1000000",
            "format": "decimal",
            "type": "string"
          },
          "total_net_worth_min": {
            "description": "The lower bound of the user's total net worth.",
            "example": "100000",
            "format": "decimal",
            "type": "string"
          },
          "visa_expiration_date": {
            "description": "Required if `visa_type` is set.",
            "format": "date",
            "type": "string"
          },
          "visa_type": {
            "description": "Only used to collect visa types for users residing in the USA.",
            "type": "string"
          }
        },
        "required": [
          "given_name",
          "family_name",
          "date_of_birth",
          "country_of_tax_residence",
          "funding_source"
        ],
        "type": "object"
      },
      "OwnerDocument": {
        "description": "A document associated with an owner of the account",
        "example": {
          "created_at": "2019-09-30T23:55:31.185998Z",
          "document_sub_type": "passport",
          "document_type": "identity_verification",
          "id": "0d18ae51-3c94-4511-b209-101e1666416b",
          "mime_type": "image/jpeg"
        },
        "properties": {
          "created_at": {
            "format": "date-time",
            "type": "string"
          },
          "document_sub_type": {
            "description": "The sub-type of the document. This is a free-form property.",
            "type": "string"
          },
          "document_type": {
            "$ref": "#/components/schemas/OwnerDocumentType"
          },
          "id": {
            "format": "uuid",
            "type": "string"
          },
          "mime_type": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "document_type",
          "created_at"
        ],
        "type": "object"
      },
      "OwnerDocumentType": {
        "description": "The type of the owner document",
        "enum": [
          "account_approval_letter",
          "address_verification",
          "cip_result",
          "company_formation",
          "date_of_birth_verification",
          "entity_operating_document",
          "entity_registration",
          "hio_declaration_form",
          "identity_verification",
          "limited_trading_authorization",
          "pep_declaration_form",
          "tax_id_verification",
          "w8ben",
          "w9"
        ],
        "example": "identity_verification",
        "type": "string"
      },
      "OwnerDocumentUploadRequest": {
        "description": "The request to upload a document for an owner of the account",
        "example": {
          "content": "/9j/Cg==",
          "document_sub_type": "passport",
          "document_type": "identity_verification",
          "mime_type": "image/jpeg"
        },
        "examples": [
          {
            "content": "/9j/Cg==",
            "document_sub_type": "passport",
            "document_type": "identity_verification",
            "mime_type": "image/jpeg"
          }
        ],
        "properties": {
          "content": {
            "contentEncoding": "base64",
            "description": "The base64 string encoding of the document contents. This property is required unless content_data is provided.",
            "example": "/9j/Cg==",
            "type": "string"
          },
          "content_data": {
            "$ref": "#/components/schemas/W8benDocument"
          },
          "document_sub_type": {
            "description": "The specific type of document, e.g. passport. This is a free-form property.",
            "example": "passport",
            "type": "string"
          },
          "document_type": {
            "$ref": "#/components/schemas/OwnerDocumentType"
          },
          "mime_type": {
            "description": "This field is required if content is specified. ENUM: application/pdf, image/png, or image/jpeg. If document_type is w8ben then application/json is also accepted",
            "example": "image/jpeg",
            "type": "string"
          }
        },
        "required": [
          "document_type",
          "content"
        ],
        "title": "OwnerDocumentUploadRequest",
        "type": "object"
      },
      "StreetAddress": {
        "example": "20 N San Mateo Dr",
        "type": "string"
      },
      "TaxIdType": {
        "description": "An Enum of the various kinds of Tax ID formats Alpaca supports.\n\nPossible Values are:\n\n\n- **USA_SSN**\nUSA Social Security Number\n\n- **USA_ITIN**\nUSA Individual Taxpayer Identification Number\n\n- **ARG_AR_CUIT**\nArgentina CUIT\n\n- **AUS_TFN**\nAustralian Tax File Number\n\n- **AUS_ABN**\nAustralian Business Number\n\n- **BOL_NIT**\nBolivia NIT\n\n- **BRA_CPF**\nBrazil CPF\n\n- **CHL_RUT**\nChile RUT\n\n- **COL_NIT**\nColombia NIT\n\n- **CRI_NITE**\nCosta Rica NITE\n\n- **DEU_TAX_ID**\nGermany Tax ID (Identifikationsnummer)\n\n- **DOM_RNC**\nDominican Republic RNC\n\n- **ECU_RUC**\nEcuador RUC\n\n- **FRA_SPI**\nFrance SPI (Reference Tax Number)\n\n- **GBR_UTR**\nUK UTR (Unique Taxpayer Reference)\n\n- **GBR_NINO**\nUK NINO (National Insurance Number)\n\n- **GTM_NIT**\nGuatemala NIT\n\n- **HND_RTN**\nHonduras RTN\n\n- **HUN_TIN**\nHungary TIN Number\n\n- **IDN_KTP**\nIndonesia KTP\n\n- **IND_PAN**\nIndia PAN Number\n\n- **ISR_TAX_ID**\nIsrael Tax ID (Teudat Zehut)\n\n- **ITA_TAX_ID**\nItaly Tax ID (Codice Fiscale)\n\n- **JPN_TAX_ID**\nJapan Tax ID (Koijin Bango)\n\n- **MEX_RFC**\nMexico RFC\n\n- **NIC_RUC**\nNicaragua RUC\n\n- **NLD_TIN**\nNetherlands TIN Number\n\n- **PAN_RUC**\nPanama RUC\n\n- **PER_RUC**\nPeru RUC\n\n- **PRY_RUC**\nParaguay RUC\n\n- **SGP_NRIC**\nSingapore NRIC\n\n- **SGP_FIN**\nSingapore FIN\n\n- **SGP_ASGD**\nSingapore ASGD\n\n- **SGP_ITR**\nSingapore ITR\n\n- **SLV_NIT**\nEl Salvador NIT\n\n- **SWE_TAX_ID**\nSweden Tax ID (Personnummer)\n\n- **URY_RUT**\nUruguay RUT\n\n- **VEN_RIF**\nVenezuela RIF\n\n- **NATIONAL_ID**\nNational ID number, if a tax ID number is not available\n\n- **PASSPORT**\nPassport number, if a tax ID number is not available\n\n- **PERMANENT_RESIDENT**\nPermanent resident number, if a tax ID number is not available\n\n- **DRIVER_LICENSE**\nDriver's license number, if a tax ID number is not available\n\n- **OTHER_GOV_ID**\nOther government issued identifier, if a tax ID number is not available\n\n- **NOT_SPECIFIED**\nOther Tax IDs",
        "enum": [
          "USA_SSN",
          "USA_ITIN",
          "ARG_AG_CUIT",
          "AUS_TFN",
          "AUS_ABN",
          "BOL_NIT",
          "BRA_CPF",
          "CHL_RUT",
          "COL_NIT",
          "CRI_NITE",
          "DEU_TAX_ID",
          "DOM_RNC",
          "ECU_RUC",
          "FRA_SPI",
          "GBR_UTR",
          "GBR_NINO",
          "GTM_NIT",
          "HND_RTN",
          "HUN_TIN",
          "IDN_KTP",
          "IND_PAN",
          "ISR_TAX_ID",
          "ITA_TAX_ID",
          "JPN_TAX_ID",
          "MEX_RFC",
          "NIC_RUC",
          "NLD_TIN",
          "PAN_RUC",
          "PER_RUC",
          "PRY_RUC",
          "SGP_NRIC",
          "SGP_FIN",
          "SGP_ASGD",
          "SGP_ITR",
          "SLV_NIT",
          "SWE_TAX_ID",
          "URY_RUT",
          "VEN_RIF",
          "NATIONAL_ID",
          "PASSPORT",
          "PERMANENT_RESIDENT",
          "DRIVER_LICENSE",
          "OTHER_GOV_ID",
          "NOT_SPECIFIED"
        ],
        "example": "USA_SSN",
        "title": "TaxIdType",
        "type": "string"
      },
      "TrustedContact": {
        "anyOf": [
          {
            "required": [
              "email_address"
            ]
          },
          {
            "required": [
              "phone_number"
            ]
          },
          {
            "required": [
              "street_address"
            ]
          }
        ],
        "dependentRequired": {
          "street_address": [
            "city",
            "state",
            "postal_code",
            "country"
          ]
        },
        "description": "This model input is optional. However, the client should make a reasonable effort to obtain the trusted contact information. See [FINRA Notice 17-11](https://www.finra.org/sites/default/files/Regulatory-Notice-17-11.pdf) for more details.\n\nAt least one of the following is required:\n- `email_address`\n- `phone_number`\n- `street_address`\n",
        "example": {
          "email_address": "jane.doe@example.com",
          "family_name": "Doe",
          "given_name": "Jane"
        },
        "properties": {
          "city": {
            "description": "Required if `street_address` is set.",
            "type": "string"
          },
          "country": {
            "description": "The country in [ISO 3166-1 alpha-3](https://www.iso.org/iso-3166-country-codes.html) format. Required if `street_address` is set.",
            "type": "string"
          },
          "email_address": {
            "description": "At least one of `email_address`, `phone_number`, or `street_address` is required.",
            "example": "jane.doe@example.com",
            "format": "email",
            "type": "string"
          },
          "family_name": {
            "example": "Doe",
            "type": "string"
          },
          "given_name": {
            "example": "Jane",
            "type": "string"
          },
          "phone_number": {
            "description": "At least one of `email_address`, `phone_number`, or `street_address` is required.",
            "type": "string"
          },
          "postal_code": {
            "description": "Required if `street_address` is set.",
            "type": "string"
          },
          "state": {
            "description": "Required if `street_address` is set.",
            "type": "string"
          },
          "street_address": {
            "description": "At least one of `email_address`, `phone_number`, or `street_address` is required.",
            "items": {
              "type": "string"
            },
            "type": "array"
          }
        },
        "required": [
          "given_name",
          "family_name"
        ],
        "type": "object"
      },
      "W8benDocument": {
        "description": "Use this property (instead of the content property) to upload W-8 BEN data in JSON format.",
        "examples": [
          {
            "additional_conditions": "None",
            "country_citizen": "Australia",
            "date": "2021-06-14",
            "date_of_birth": "1970-01-01",
            "foreign_tax_id": "123 456 789",
            "ftin_not_required": false,
            "full_name": "John Doe",
            "income_type": "interest",
            "ip_address": "127.0.0.1",
            "mailing_address_city_state": "Adelaide, South Australia",
            "mailing_address_country": "Australia",
            "mailing_address_street": "51 Main St",
            "paragraph_number": "15",
            "percent_rate_withholding": 5,
            "permanent_address_city_state": "Adelaide, South Australia",
            "permanent_address_country": "Australia",
            "permanent_address_street": "20 Main St",
            "reference_number": "abc123",
            "residency": "Australia",
            "revision": "10-2021",
            "signer_full_name": "Mr. Signing User",
            "tax_id_ssn": "123-00-456",
            "timestamp": "2021-06-14T09:31:05Z"
          }
        ],
        "properties": {
          "additional_conditions": {
            "description": "Any additional conditions to specify",
            "type": "string"
          },
          "country_citizen": {
            "description": "The country that the applicant is a citizen of",
            "type": "string"
          },
          "date": {
            "description": "date signed",
            "format": "date",
            "type": "string"
          },
          "date_of_birth": {
            "description": "date of birth of applicant",
            "format": "date",
            "type": "string"
          },
          "foreign_tax_id": {
            "description": "Applicant's tax id in their home country",
            "type": "string"
          },
          "ftin_not_required": {
            "description": "Required if foreign_tax_id and tax_id_ssn are empty.",
            "type": "boolean"
          },
          "full_name": {
            "description": "Full name of applicant",
            "type": "string"
          },
          "income_type": {
            "description": "Income type of applicant",
            "type": "string"
          },
          "ip_address": {
            "description": "IP address of applicant when signed",
            "type": "string"
          },
          "mailing_address_city_state": {
            "description": "Mailing city/state of applicant",
            "type": "string"
          },
          "mailing_address_country": {
            "description": "Mailing country for applicant",
            "type": "string"
          },
          "mailing_address_street": {
            "description": "Mailing street address for applicant",
            "type": "string"
          },
          "paragraph_number": {
            "type": "string"
          },
          "percent_rate_withholding": {
            "type": "integer"
          },
          "permanent_address_city_state": {
            "description": "Permanent city/state of applicant",
            "type": "string"
          },
          "permanent_address_country": {
            "description": "Permanent country of residence of applicant",
            "type": "string"
          },
          "permanent_address_street": {
            "description": "Permanent street address of applicant",
            "type": "string"
          },
          "reference_number": {
            "type": "string"
          },
          "residency": {
            "description": "Country of residency of applicant",
            "type": "string"
          },
          "revision": {
            "description": "Revision of the W8BEN form",
            "type": "string"
          },
          "signer_full_name": {
            "description": "Full name of signing user",
            "type": "string"
          },
          "tax_id_ssn": {
            "description": "TaxID/SSN of applicant",
            "type": "string"
          },
          "timestamp": {
            "description": "Timestamp when form data was gathered",
            "format": "time",
            "type": "string"
          }
        },
        "required": [
          "country_citizen",
          "date",
          "date_of_birth",
          "full_name",
          "ip_address",
          "permanent_address_city_state",
          "permanent_address_country",
          "permanent_address_street",
          "revision",
          "timestamp",
          "signer_full_name"
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
    "/v1/accounts": {
      "post": {
        "description": "Create an account for a new or existing account holder. Required fields, eligibility, and initial status depend on the account type, enabled assets, and your correspondent configuration. Account status changes are available through the Account Status Events stream.\n\nTo create an account for an existing holder, provide `primary_account_holder_id` instead of inline holder information. Among the documented account types, existing holders are supported for trading and IRA accounts. Donor-advised accounts instead reference an existing legal entity with `entity_id`.\n",
        "operationId": "createAccount",
        "requestBody": {
          "content": {
            "application/json": {
              "examples": {
                "custodial-account": {
                  "summary": "Custodial account with guardian and minor information",
                  "value": {
                    "account_type": "custodial",
                    "agreements": [
                      {
                        "agreement": "customer_agreement",
                        "ip_address": "185.13.21.99",
                        "signed_at": "2020-09-11T18:13:44Z"
                      }
                    ],
                    "contact": {
                      "city": "San Mateo",
                      "country": "USA",
                      "email_address": "john.doe@example.com",
                      "postal_code": "94401",
                      "state": "CA",
                      "street_address": [
                        "123 Main Street"
                      ]
                    },
                    "disclosures": {
                      "immediate_family_exposed": false,
                      "is_affiliated_exchange_or_finra": false,
                      "is_control_person": false,
                      "is_politically_exposed": false
                    },
                    "enabled_assets": [
                      "us_equity"
                    ],
                    "identity": {
                      "country_of_birth": "USA",
                      "country_of_citizenship": "USA",
                      "country_of_tax_residence": "USA",
                      "date_of_birth": "1990-01-01",
                      "family_name": "Doe",
                      "funding_source": [
                        "employment_income"
                      ],
                      "given_name": "John",
                      "tax_id": "666-55-4321",
                      "tax_id_type": "USA_SSN"
                    },
                    "minor_identity": {
                      "country_of_birth": "USA",
                      "country_of_citizenship": "USA",
                      "country_of_tax_residence": "USA",
                      "date_of_birth": "2012-04-05",
                      "email": "jamie.doe@example.com",
                      "family_name": "Doe",
                      "given_name": "Jamie",
                      "state": "CA",
                      "tax_id": "666-55-1234",
                      "tax_id_type": "USA_SSN"
                    }
                  }
                },
                "donor-advised-account": {
                  "summary": "Donor-advised account for an existing legal entity",
                  "value": {
                    "account_type": "donor_advised",
                    "entity_id": "14fbfc51-3704-4c74-8984-8326c4117aee"
                  }
                },
                "existing-holder-ira": {
                  "summary": "IRA account for an existing holder",
                  "value": {
                    "account_sub_type": "traditional",
                    "account_type": "ira",
                    "agreements": [
                      {
                        "agreement": "customer_agreement",
                        "ip_address": "185.13.21.99",
                        "signed_at": "2020-09-11T18:13:44Z"
                      }
                    ],
                    "enabled_assets": [
                      "us_equity"
                    ],
                    "primary_account_holder_id": "8b5b7e4c-9f2d-4f4a-9a7b-1b2c3d4e5f60"
                  }
                },
                "trading-account": {
                  "summary": "Trading account with inline holder information",
                  "value": {
                    "agreements": [
                      {
                        "agreement": "customer_agreement",
                        "ip_address": "185.13.21.99",
                        "signed_at": "2020-09-11T18:13:44Z"
                      }
                    ],
                    "contact": {
                      "city": "San Mateo",
                      "country": "USA",
                      "email_address": "john.doe@example.com",
                      "postal_code": "94401",
                      "state": "CA",
                      "street_address": [
                        "123 Main Street"
                      ]
                    },
                    "disclosures": {
                      "immediate_family_exposed": false,
                      "is_affiliated_exchange_or_finra": false,
                      "is_control_person": false,
                      "is_politically_exposed": false
                    },
                    "enabled_assets": [
                      "us_equity"
                    ],
                    "identity": {
                      "country_of_birth": "USA",
                      "country_of_citizenship": "USA",
                      "country_of_tax_residence": "USA",
                      "date_of_birth": "1990-01-01",
                      "family_name": "Doe",
                      "funding_source": [
                        "employment_income"
                      ],
                      "given_name": "John",
                      "tax_id": "666-55-4321",
                      "tax_id_type": "USA_SSN"
                    }
                  }
                }
              },
              "schema": {
                "$ref": "#/components/schemas/AccountCreationRequest"
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
                  "$ref": "#/components/schemas/Account"
                }
              }
            },
            "description": "OK"
          },
          "400": {
            "content": {
              "application/json": {
                "examples": {
                  "malformed-request-body": {
                    "summary": "Malformed request body",
                    "value": {
                      "code": 40010000,
                      "message": "request body format is invalid: error decoding string '\"\"': can't convert \"\" to decimal"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request body is malformed or cannot be decoded."
          },
          "409": {
            "description": "There is already an existing account registered with the same email address."
          },
          "422": {
            "content": {
              "application/json": {
                "examples": {
                  "conflicting-holder-data": {
                    "summary": "Conflicting inline and referenced holder data",
                    "value": {
                      "code": 40010001,
                      "message": "cannot specify primary_account_holder_id together with identity or contact or disclosures or minor_identity"
                    }
                  }
                },
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            },
            "description": "The request is well-formed but fails account-creation validation. This can include conflicting inline and referenced holder data, an unsupported account-type and holder combination, or an ineligible referenced party."
          }
        },
        "summary": "Create an Account",
        "tags": [
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
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```