# FPSL Integration Guide for Fully Disclosed

Source: https://docs.alpaca.markets/us/docs/fpsl-integration-guide-for-fully-disclosed.md

---
updatedAt: 2026-09-23T17:33:14.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# FPSL Integration Guide for Fully Disclosed

The Fully-Paid Securities Lending (FPSL) program enables customers to lend securities they have fully paid for, generating additional returns while retaining beneficial ownership. With Alpaca’s API, customers can easily manage their participation in the FPSL program, while partners have the flexibility to customize interest-sharing tiers. Partners can also provide a detailed securities-level breakdown of interest earned to their customers. This program offers an effective way for both the partner and the partner’s customers to earn passive income, making it a powerful tool for attracting new clients and strengthening relationships with existing ones.

### General Knowledge Points

* Interest is accrued daily (actual / 360 basis) and is paid out on a monthly basis.
* Collateral will be held for the customers in a custodial account at a tri-party bank and will be recalculated daily depending on market changes for the securities on loan.
* There would be **no** margin/buying power/equity implications to have securities on loan.
* When customers lend out their shares, they forfeit voting rights. Customers need to unenroll their accounts from FPSL if they wish to regain shareholder voting rights.
* When a stock is lent, the borrower is entitled to the dividend. However, the lenders (customers) will receive a “Substitute Payment in Lieu of Dividend” which may be subject to different tax rules than dividends.
* There is no guarantee any given share will be lent, because that depends on borrow demand, and rates move with supply and demand for the individual security. Customers also cannot choose which securities to lend. Enrollment applies to the whole eligible portfolio.
* FPSL is only available in certain countries and models. For questions, reach out to your Alpaca contact.
* Just because a share is in lendable inventory, does not mean that all of the shares will go out. Utilization of lendable inventory depends on the market demand for the specific security.
* Through vendor partners, any participant that Alpaca lends shares out to is a licensed and regulated broker-dealer, hedge fund or institution.

### Prerequisites&#x20;

Before using FPSL APIs, ensure:

1. The account holder meets the country eligibility requirements for FPSL. Alpaca validates the country of tax residence, and for legal entities, country of incorporation. The account must not be an account linked under a master account. Any accounts linked under a master account will receive an error message saying `fpsl enrollment is not supported on customer subaccounts`
2. Any one of the following pre-requisites must be met:
   1. `$2,500 in total account balance`
   2. `$20,000 in reported income`
   3. `$20,000 in liquid assets`
   4. `Stock investment experience reported as anything other than none`
3. Required Agreements: The account must have signed:
   1. `master_securities_lending_agreement`

### Step 1: Get Available FPSL Tiers

**Endpoint:&#x20;**`GET /v1/fpsl/tiers`<br />**Purpose:** Determine what FPSL tiers are available.

**Key Considerations:**

* Tiers are provisioned by Alpaca during onboarding. Partners do not create, update, or delete FPSL tiers through this API.
* Th&#x65;*&#x20;*`customer_split` and `partner_split` represent the percentage of interest revenue from the gross amount paid. For example, a `customer_split` of 0.20 means that if a security generates $10 in interest revenue, the customer will receive 20% of that amount, which is $2.
* Partners can determine the appropriate `customer_split`.

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/tiers' \
--header 'Authorization: Basic <your-credentials>'

```

**Query Parameters:**

* `tier_name` (optional): Exact tier name
* `market` (optional): Filter by market (e.g., "US")
* `sort_by` (optional): Sort by `tier_name`, `market`, `customer_split`, or `partner_split`
* `direction` (optional): `asc` or `desc` (default is `desc`)

**Response Example:**

```json
[
  {
    "id": "9BAB56CA-CE9A-4C87-A702-3365F92C2EB5",
    "tier_name": "gold",
    "market": "US",
    "customer_split": "0.20",
    "partner_split": "0.47",
    "created_at": "2024-06-11T19:00:00.000000Z",
    "updated_at": "2024-06-11T19:00:00.000000Z"
  },
  {
    "id": "2F4EF316-E076-4389-BDCC-96033C69E707",
    "tier_name": "regular",
    "market": "US",
    "customer_split": "0.10",
    "partner_split": "0.57",
    "created_at": "2024-06-11T19:00:00.000000Z",
    "updated_at": "2024-06-11T19:00:00.000000Z"
  }
[

```

**Filtering Examples:**

```json
# Filter by market and tier name
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/tiers?market=US&tier_name=silver'

# Sort by partner split descending

curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/tiers?sort_by=partner_split&direction=desc'

```

### Step 2.1: Communicating Customer Consent

Work with your Alpaca contact to ensure that you are following the correct requirements for communicating customer consent.

E**ndpoint:&#x20;**`POST v1/accounts/`<br />E**ndpoint:&#x20;**`PATCH /v1/accounts/{account_id}`<br />**Purpose:&#x20;**&#x41;cknowledge master securities lending agreement

**Key Considerations:**

* `revision` is optional, if left blank it will default to the latest revision number
* `fpsl.status` will be shown in the response body, more details about this status provided in the section below
* `fpsl`*&#x20;property&#x20;*&#x6D;ust be set at the time of enrollment
* A partner can consent (sign the MSLA) and enroll/assign a tier in the same call, and it works for both create and patch

**Request Example:**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "agreements": [
        {
            "agreement": "master_securities_lending_agreement",
            "signed_at": "2024-07-11T18:09:33Z",
            "ip_address": "185.13.21.99",
            "revision": "<insert updated revision number>"
        }
    ]
}'
```

**Response:&#x20;**&#x52;eturns the updated account object with 200 OK HTTP status:

```json
200 OK 
```

### Step 2.2: Enrolling the account&#x20;

**Endpoint:&#x20;**`PATCH /v1/accounts/{account_id}`<br />**Purpose:&#x20;**&#x45;nroll an existing account in FPSL program

**Request Example:**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "fpsl": {
        "US": {
            "tier_id": "5cd4d4cf-fda9-4949-99d7-9e4a4613dc2d",
            "status": "ACTIVE"
        }
    }
}'


```

**Enrollment Rules&#x20;**

* `tier_id` is required for first enrollment
* `status` is optional for first enrollment
* If `status` is omitted on first enrollment, the account is enrolled as `ACTIVE`

**Response Example:&#x20;**&#x52;eturns the updated account object with FPSL status

```json
{
    "id": "cd1045f5-c5dc-4204-a906-633ec96df05b",
    "account_number": "533888676",
    "status": "ACTIVE",
    
    "fpsl": {

        "US": {
            "status": "ACTIVE",
            "tier_id": "5cd4d4cf-fda9-4949-99d7-9e4a4613dc2d"
        }
    }
}
```

### Step 3: Check FPSL Enrollment Status

IMPORTANT: Before engaging in this step, it is recommended to attempt Step 7 first using SSE requests. This specific method is more of a backup in case that you have issues with the SSE request option.

**Endpoint:&#x20;**`GET /v1/accounts/{account_id}`
**Purpose:&#x20;**&#x52;etrieve current FPSL enrollment status

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

**FPSL Status Values:**

| States          | Description                           |
| --------------- | ------------------------------------- |
| FPSL key absent | This account has never been enrolled. |
| `INACTIVE`      | This account has been unenrolled.     |
| `ACTIVE`        | The account is enrolled and eligible. |

**Enrolled Account Snippet:**

```json
{
  "id": "4db36989-6565-4011-9126-39fe6b3d9bf6",
  "fpsl": {
    "US": {
      "status": "ACTIVE",
      "tier_id": "61e69015-8549-4bfd-b9c3-01e75843f47d"
    }
  }
}

```

### Step 4: Modify FPSL Enrollment&#x20;

Changing tier and opting out in the same call is rejected. Opting out mid-month does not forfeit interest already earned for days the shares were on loan. From the next business day, an opted-out account's shares are no longer offered, while any existing loan closes as the borrower returns the shares.

**Change Tier Example:**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "fpsl": {
        "US": {
            "tier_id": "aab75b22-6ac7-48cd-883d-7313afd1afcd",
            "status": "ACTIVE"
        }
    }
}'

```

**Un-Enroll Account Example:&#x20;**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "fpsl": {
        "US": {
            "status": "INACTIVE"
        }
    }
}'

```

**Re-Enroll Account Example:**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "fpsl": {
        "US": {
            "status": "ACTIVE"
        }
    }
}'


```

*Note - If no&#x20;*`tier_id`*&#x20;is specified on re-enroll, the previously assigned tier is reused.*

### Step 5: Retrieve FPSL Loan Activities &#x20;

**Endpoint:&#x20;**`GET /v1/fpsl/loans`<br />**Purpose:&#x20;**&#x47;et daily stock lending activities and interest information

**Request Example:&#x20;**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/loans?account_id={account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

* `interest`*&#x20;may be omitted if interest has not yet been calculated for the loan*
* `updated_at`*&#x20;may be present when loan values, including interest, have been adjusted*

**Query Parameters:**

* `page_token` (optional): pagination token
* `start`*&#x20;*(optional): inclusive start date in YYYY-MM-DD
* `end`*&#x20;*(optional): exclusive end date in YYYY-MM-DD
* `limit`*&#x20;*(optional): page size
* `account_id` (optional): filter by account
* *recommendation*: always pass `account_id`*&#x20;*&#x66;or reconciliation. If omitted, results may include all accounts visible to your API credentials

**Default Date Behavior:**

* `start` defaults to the first day of the current month
* `end` defaults to the day after the current date
* `defaults` use New York timezone logic

**Response Structure:&#x20;**

```json
{
  "loans": [
    {
      "date": "2024-07-11",
      "account_id": "cd1045f5-c5dc-4204-a906-633ec96df05b",
      "account_number": "533888676",
      "correspondent": "YOUR_CORRESPONDENT",
      "symbol": "AAPL",
      "quantity": 100,
      "market_value": 15000.00,
      "collateral": 15300.00,
      "updated_at": "2024-07-12T05:00:00.000000Z",
      "interest": {
        "customer": 2.50,
        "partner": 5.85
      }
    }
  ],
  "next_page_token": "{value_to_send_to_continue_paging}"
}

```

### Step 6: Get Monthly FPSL Interest Activity

**Endpoint:&#x20;**`GET /v1/accounts/activities/INT`<br />**Purpose:&#x20;**&#x4F;btain the month end interest activity for FPSL

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/accounts/activities/INT?account_id={account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

**Response Example:**

```json
{
  "id": "5ca8b9e6-cd56-48fa-99a7-ce1f5290f312",
  "qty": null,
  "price": null,
  "status": "executed",
  "symbol": "",
  "entry_type": "INT",
  "net_amount": 0.58,
  "description": "June 2024 Fully-Paid Securities Lending",
  "settle_date": "2024-06-28",
  "system_date": "2024-06-28",
  "entry_sub_type": "FPSL",
  "per_share_amount": null
}

```

### Step 7: FPSL SSE events (optional)

**Endpoint:&#x20;**`GET /v1/events/accounts/status`<br />**Purpose:&#x20;**&#x52;etrieve the program status history for an account

**Request Example:&#x20;**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/events/accounts/status?id={account_id}&since_ulid={since_ulid}' \
--header 'Authorization: Basic <your-credentials>' \
--header 'Accept: text/event-stream'

```

**Response Example:&#x20;**

```json
{
  "fpsl": {
    "US": {
      "status_from": "ACTIVE",
      "status_to": "INACTIVE"
    }
  },
  "account_id": "382dd20d-d627-4d9f-9c93-7e24cd340546",
  "account_number": "533888676",
  "at": "2024-06-11T19:00:00.000000Z",
  "event_ulid": "01J2VQMVJRMXQRPNS3831XFE1Y"
}

```

**Other Information**

* In sandbox, FPSL account status events are not emitted. During sandbox testing, validate status changes by polling `GET /v1/accounts/{account_id}`.

<br />

*Please read&#x20;*[*Important Risk Disclosures With Respect To Participating In Fully Paid Securities Lending Transactions&#x20;*](https://files.alpaca.markets/disclosures/Important+Risk+Disclosures+With+Respect+To+Participating+In+Fully+Paid+Securities+Lending+Transactions.pdf)*carefully before deciding whether to participate in lending Fully Paid Securities or agreeing to enter into a Master Securities Lending Agreement with Alpaca Securities LLC.*

*These disclosures describe important characteristics of, and risks associated with engaging in, securities-lending transactions.*