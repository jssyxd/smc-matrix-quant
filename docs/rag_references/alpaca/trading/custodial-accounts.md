# Custodial accounts

Source: https://docs.alpaca.markets/us/docs/custodial-accounts.md

---
updatedAt: 2026-01-22T19:47:27.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Custodial accounts

A custodial account enables an adult to open an account on behalf of a minor, who otherwise does not have the capacity to enter into a legal contract to open a brokerage account. Alpaca currently supports two custodial account types: Uniform Transfers to Minors Act (UTMA) and Uniform Gifts to Minors Act (UGMA). As part of the offering, Alpaca will custody the account, generate monthly custodial account statements, and handle all annual tax reporting. Please be aware that all tax reporting will be based on the minor's information. Furthermore, a minor cannot use or trade in a custodial account as they are only the beneficiary. Custodial accounts do not support shorting, margin, or pattern day trading. Each of the account opening steps are the same as standard brokerage accounts that Alpaca offers, and any KYC checks will be run on the adult. This documentation will serve to highlight any notable differences between the account opening processes.

**Custodial Account Object**

| Attribute        | Notes                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| account\_type    | Designate which type of account is to be opened with Alpaca - passing 'custodial' will create a custodial account.                             |
| contact          | Contact information about the user.                                                                                                            |
| identity         | KYC information about the user.                                                                                                                |
| disclosures      | Required disclosures about the user.                                                                                                           |
| documents        | Any documents that need to be uploaded (eg. passport, visa, …).                                                                                |
| trusted\_contact | The contact information of a trusted contact to the user in case account recovery is needed.                                                   |
| minor\_identity  | Information about the minor that is associated with the account. All fields in this object will be required when account\_type is 'custodial'. |

**Minor identity object**

| Attribute                   | Type           |
| --------------------------- | -------------- |
| given\_name                 | string         |
| family\_name                | string         |
| email                       | string         |
| date\_of\_birth             | date           |
| tax\_id                     | string         |
| tax\_id\_type               | ENUM.TaxIdType |
| country\_of\_citizenship    | string         |
| country\_of\_birth          | string         |
| country\_of\_tax\_residence | string         |
| state                       | string         |

<br />

## Creating a Custodial Account

```
POST /v1/accounts
```

The custodian, or adult associated with the account, will submit an account application with the required information and a signed custodian customer agreement. This will create a custodial account for the adult on behalf of the minor, whose information will be submitted in the minor\_identity section.

If you utilize Alpaca for KYCaaS, we will perform the necessary checks and approve the account once we have determined the custodian information is legitimate. Please refer to the Events API for account status changes and any KYC updates that require you to take further action.

Note: All account statuses and their definitions can be found [here](https://docs.alpaca.markets/docs/accounts-statuses).

**Sample Request**

```json
{
  "account_type": "custodial",
  "contact": {
    "email_address": "cool_alpaca@example.com",
    "phone_number": "555-676-7788",
    "street_address": ["20 N San Mateo Dr"],
    "city": "San Mateo",
    "state": "CA",
    "postal_code": "94401",
    "country": "USA"
  },
  "identity": {
    "given_name": "John",
    "family_name": "Doe",
    "date_of_birth": "1990-01-01",
    "tax_id": "676-55-4321",
    "tax_id_type": "USA_SSN",
    "country_of_citizenship": "USA",
    "country_of_birth": "USA",
    "country_of_tax_residence": "USA",
    "funding_source": ["employment_income"],
    "annual_income_min": "30000",
    "annual_income_max": "50000",
    "liquid_net_worth_min": "100000",
    "liquid_net_worth_max": "150000",
    "total_net_worth_min": "10000",
    "total_net_worth_max": "10000",
    "liquidity_needs": "does_not_matter",
    "investment_experience_with_stocks": "over_5_years",
    "investment_experience_with_options": "over_5_years",
    "risk_tolerance": "conservative",
    "investment_objective": "market_speculation",
    "investment_time_horizon": "more_than_10_years",
    "marital_status": "MARRIED",
    "middle_name": "M",
    "number_of_dependents": 5
  },
  "disclosures": {
    "is_control_person": false,
    "is_affiliated_exchange_or_finra": false,
    "is_politically_exposed": false,
    "immediate_family_exposed": false
  },
  "agreements": [

         {
      "agreement": "customer_agreement",
      "signed_at": "2025-09-11T18:13:44Z",
      "ip_address": "185.13.21.99"

   }
  ],
  "documents": [
    {
      "document_type": "identity_verification",
      "document_sub_type": "passport",
      "content": "/9j/Cg==",
      "mime_type": "image/jpeg"
    }
  ],
  "trusted_contact": {
    "given_name": "Jane",
    "family_name": "Doe",
    "email_address": "jane.doe@example.com"
  },
  "minor_identity": {
    "given_name": "Jimmy",
    "family_name": "Doe",
    "email": "foo@bar.com",
    "date_of_birth": "2015-01-01",
    "tax_id": "676-54-4321",
    "tax_id_type": "USA_SSN",
    "country_of_citizenship": "USA",
    "country_of_birth": "USA",
    "country_of_tax_residence": "USA",
    "state": "CA"
  }
}

```

*A copy of the custodian customer agreement and the custodial account disclosure are available upon request - please reach out to Alpaca for more information.*

*Note: Revisions follow the RR.MM.YYYY format (RR denotes the revision number); the request payload must include the latest customer\_agreement (rev ≥ 18) with the revision explicitly specified.*

**Response model**

| Attribute       | Type               | Notes                                                                  |
| --------------- | ------------------ | ---------------------------------------------------------------------- |
| id              | string/UUID        | UUID that identifies the account for later reference                   |
| account\_number | string             | A human-readable account number that can be shown to the end user      |
| status          | ENUM.AccountStatus |                                                                        |
| currency        | string             | Always USD                                                             |
| last\_equity    | string             | EOD equity calculation (cash + long market value + short market value) |
| created\_at     | string             | RFC3339 format                                                         |

<br />

```json
{
  "account": {
    "id": "0d18ae51-3c94-4511-b209-101e1666416b",
    "account_number": "9034005019",
    "status": "ACTIVE",
    "currency": "USD",
    "last_equity": "1500.65",
    "created_at": "2019-09-30T23:55:31.185998Z"
  }
}

```

**Error Codes**

| Error Code | Description                                                                            |
| ---------- | -------------------------------------------------------------------------------------- |
| 400        | Bad Request: The body in the request is not valid                                      |
| 409        | Conflict: There is already an existing account registered with the same email address. |
| 422        | Unprocessable Entity: Invalid input value.                                             |
| 500        | Internal Server Error: Some server error occurred. Please contact Alpaca.              |

<br />

## Updating an Account

```
PATCH /v1/accounts/{account_id}
```

This operation updates custodial account information. In addition to what is listed for traditional brokerage accounts, the minor identity information is modifiable.

**Response Parameters**

| Attribute        | Requirement |
| ---------------- | ----------- |
| contact          | Optional    |
| identity         | Optional    |
| disclosures      | Optional    |
| documents        | Optional    |
| trusted\_contact | Optional    |
| minor\_identity  | Optional    |

**Minor Identity parameters**

| Attribute                   | Type           | Requirement | Notes                               |
| --------------------------- | -------------- | ----------- | ----------------------------------- |
| given\_name                 | string         | Optional    |                                     |
| family\_name                | string         | Optional    |                                     |
| email                       | string         | Optional    |                                     |
| date\_of\_birth             | date           | Optional    | RFC3339 format                      |
| tax\_id                     | string         | Optional    |                                     |
| tax\_id\_type               | ENUM.TaxIdType | Required    | Must be 'USA\_SSN'                  |
| country\_of\_citizenship    | string         | Required    | Must be 'USA'                       |
| country\_of\_birth          | string         | Required    | 3 letter country code acceptable    |
| country\_of\_tax\_residence | string         | Required    | Must be 'USA'                       |
| state                       | string         | Required    | Only accepts two letter state codes |

**Response**

If all parameters are valid and updates have been made, it returns with status code 200. The response is the account model.

**Error Codes**

| Error Code | Description                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------- |
| 400        | Bad Request: The body in the request is not valid                                                 |
| 422        | Unprocessable Entity: The request body contains an attribute that is not permitted to be updated. |
| 500        | Internal Server Error: Some server error occurred. Please contact Alpaca.                         |

## Appendix

**Sample Monthly Statement:**

<Image align="center" border={false} src="https://files.readme.io/40faeb129dcc35af0396dc34b218db02b4128e655a8c5b8147970409b0806c72-Screenshot_2025-12-01_at_11.12.58_PM.png" />