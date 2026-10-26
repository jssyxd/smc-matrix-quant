# FPSL Integration Guide for OmniSub

Source: https://docs.alpaca.markets/us/docs/fpsl-integration-guide-for-omnisub.md

---
updatedAt: 2026-09-23T17:30:57.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# FPSL Integration Guide for OmniSub

The Fully-Paid Securities Lending (FPSL) program enables customers to lend securities they have fully paid for, generating additional returns while retaining beneficial ownership. With Alpaca’s API, customers can easily manage their participation in the FPSL program, while partners have the flexibility to customize interest-sharing tiers. Partners can also provide a detailed securities-level breakdown of interest earned to their customers. This program offers an effective way for both the partner and the partner’s customers to earn passive income, making it a powerful tool for attracting new clients and strengthening relationships with existing ones.

### General Knowledge Points

* Interest is accrued daily (actual / 360 basis) and is paid out on a monthly basis.
* Collateral will be held for the customers in a custodial account at a tri-party bank and will be recalculated daily depending on market changes for the securities on loan.
* There would be **no** margin/buying power/equity implications to have securities on loan.
* When customers lend out their shares, they relinquish voting rights. Customers need to unenroll their accounts from FPSL if they wish to regain shareholder voting rights.
* When a stock is lent, the borrower is entitled to the dividend. However, the lenders (customers) will receive a “Substitute Payment in Lieu of Dividend” which may be subject to different tax rules than dividends.
* There is no guarantee any given share will be lent, because that depends on borrow demand, and rates move with supply and demand for the individual security. Customers also cannot choose which securities to lend. Enrollment applies to the whole eligible portfolio.
* FPSL is available in countries Alpaca has approved. Confirm your target markets with your Alpaca contact.
* Just because a share is in lendable inventory, does not mean that all of the shares will go out. Utilization of lendable inventory depends on the market demand for the specific security.
* Through vendor systems, any participant that Alpaca lends shares out to is a licensed and regulated broker-dealer, hedge fund or institution.

### Roles & Responsibilities

| Task                                                       | Alpaca                            | Partner                              |
| ---------------------------------------------------------- | --------------------------------- | ------------------------------------ |
| Per-customer lending agreement on file                     | Does not collect                  | Must collect and retain              |
| Requires partner to share revenue with sub-accounts        | Requires partner to share revenue | Must share revenue with sub-accounts |
| Individual customer eligibility test                       | Does not perform                  | Must perform                         |
| Country of tax residence check                             | Does not perform                  | Must perform                         |
| Presenting the required disclosures to your customer       | Does not verify                   | Must present                         |
| Suitability program under FINRA Rule 4330                  | Does not perform                  | Must perform                         |
| Supervisory records evidencing individual customer consent | Does not retain                   | Must retain                          |

### Prerequisites

Before using FPSL APIs on OmniSub, ensure:

1. Your correspondent is registered in Alpaca's OmniSub configuration. This is a separate enablement step from FPSL being turned on, performed by your Alpaca contact, and maps your correspondent to a specific main account.
2. Each end customer is represented in a sub account. No other account type may enroll in FPSL under an OmniSub correspondent.
3. Required Agreements: none, at the account level. Alpaca collects no agreement from sub accounts. Your own agreement with Alpaca covers the arrangement.

### Step 1: Get Available FPSL Tiers

**Endpoint:&#x20;**`GET/v1/fpsl/tiers`<br />**Purpose:** Determine what FPSL tiers are available.

**Key Considerations:**

* `customer_split`*&#x20;*&#x61;nd `partner_split`*&#x20;*&#x72;epresent the percentage of interest revenue from the gross amount paid. For example, a customer\_split of 0.20 means that if a security generates $10 in interest revenue, the customer receives $2.
* Tiers are provisioned by Alpaca during onboarding. Partners do not create, update, or delete FPSL tiers through this API.

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/tiers' \
--header 'Authorization: Basic <your-credentials>'

```

**Query Parameters:**

* `tier_name` (optional): filter by specific `tier_name`
* `market`(optional): filter by `market` (US)
* `sort_by` (optional): Sort by `tier_name`, `market`, `customer_split`, or `partner_split`
* `direction` (optional): `asc`or `desc` (default: `desc`)

**Response Example:**

```json

[
  {
    "id": "9BAB56CA-CE9A-4C87-A702-3365F92C2EB5",
    "tier_name": "gold",
    "market": "US",
    "customer_split": "0.20",
    "partner_split": "0.30",
    "created_at": "2024-06-11T19:00:00.000000Z",
    "updated_at": "2024-06-11T19:00:00.000000Z"
  }
]

```

### Step 2.1: Communicating Customer Consent

Alpaca does not run a consent check for `omnibus_sub` accounts. Before treating assets as enrolled, the partner must obtain and retain customer consent records that satisfy its own regulatory obligations. Alpaca does not see or verify those records.

### Step 2.2: Enrolling the account&#x20;

**Endpoint:&#x20;**`PATCH/v1/accounts/{account_id} `

*Use a&#x20;*`subaccount_id`*&#x20;here.*

**Purpose:&#x20;**&#x45;nroll an `omnibus_sub`account in the FPSL program

**Request Example**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{sub_account_id}' \
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

**Response Example:&#x20;**

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

### Step 3: Check Account FPSL Status

**Endpoint:&#x20;**`GET /v1/accounts/{account_id} `<br />**Purpose:&#x20;**&#x52;etrieve current FPSL enrollment status

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

**FPSL Status Values:**

| States            | Description                           |
| ----------------- | ------------------------------------- |
| `FPSL key absent` | This account has never been enrolled. |
| `INACTIVE`        | This account has been unenrolled.     |
| `ACTIVE`          | The account is enrolled and eligible. |

**Failed OmniSub Enrollment Returns One Of The Following Errors:**

| Condition                              | Message                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| Wrong account type                     | `only omnibus_sub accounts can participate in FPSL for omnibus correspondents` |
| Tier not found                         | `fpsl tier <id> not found`                                                     |
| FPSL not enabled on your correspondent | `correspondent is not enabled to participate in FPSL`                          |
| Non-US market requested                | `only US fpsl market is supported`                                             |

### Step 4: Modify FPSL Enrollment&#x20;

Changing tier and opting out in the same call is rejected. Opting out mid-month does not forfeit interest already earned for days the shares were on loan. From the next business day, an opted-out sub account's shares are no longer offered, while any existing loan closes as the borrower returns the shares.

**Endpoint:** `PATCH/v1/accounts/{sub_account_id}`<br />Use a `subaccount_id`here

**Purpose:&#x20;**&#x43;hange tier, unenroll, or re-enroll a sub account

**Change Tier Example:**

Send the new `tier_id` with no status.

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{sub_account_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <your-credentials>' \
--data '{
    "fpsl": {
        "US": {
            "tier_id": "aab75b22-6ac7-48cd-883d-7313afd1afcd"
        }
    }
}'

```

**Change Tier Response Example:**

```json
{
    "id": "cd1045f5-c5dc-4204-a906-633ec96df05b",
    "account_number": "533888676",
    "status": "ACTIVE",
    "fpsl": {
        "US": {
            "status": "ACTIVE",
            "tier_id": "aab75b22-6ac7-48cd-883d-7313afd1afcd"
        }
    }
}

```

**Un-Enroll Account Example:**

```json

curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{sub_account_id}' \
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

**Un-Enroll Response Example:**

```json

{
    "id": "cd1045f5-c5dc-4204-a906-633ec96df05b",
    "account_number": "533888676",
    "status": "ACTIVE",
    "fpsl": {
        "US": {
            "status": "INACTIVE",
            "tier_id": "5cd4d4cf-fda9-4949-99d7-9e4a4613dc2d"
        }
    }
}

```

**Re-Enroll Account Example:**

```json
curl --location --request PATCH 'https://broker-api.sandbox.alpaca.markets/v1/accounts/{sub_account_id}' \
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

**Re-Enroll Account Response:**

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

### Step 5: Retrieve FPSL Loan Activities &#x20;

**Endpoint:&#x20;**`GET/v1/fpsl/loans`<br />**Purpose:&#x20;**&#x47;et daily stock lending activities and interest information

*List FPSL Loans*

**Request Example:&#x20;**

```json
# Aggregated view across sub accounts under main account
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/loans?account_id={main_account}' \
--header 'Authorization: Basic <your-credentials>'

# Single sub account view
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/fpsl/loans?account_id={sub_account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

*updated\_at may be present when loan values, including interest, have been adjusted.*

**Query Parameters:**

* `page_token` (optional): pagination token
* `start`*&#x20;*(optional): inclusive start date in YYYY-MM-DD
* `end`*&#x20;*(optional): exclusive end date in YYYY-MM-DD
* `limit` (optional): page size
* `account_id`(optional): filter by account
* always pass `account_id`for reconciliation. If omitted, results may include all accounts visible to your API credentials

**Default Date Behavior:**

* `start` defaults to the first day of the current month
* `end` defaults to the day after the current date
* `defaults`use New York timezone logic

**Response Structure:&#x20;**

```json
{
  "loans": [
    {
      "date": "2024-07-11",
      "account_id": "{main_account_id}",
      "account_number": "533888676",
      "correspondent": "YOUR_CORRESPONDENT",
      "symbol": "AAPL",
      "quantity": 400,
      "market_value": 60000.00,
      "collateral": 61350.00,
      "updated_at": "2024-07-12T05:00:00.000000Z",
      "interest": {
        "customer": 9.10,
        "partner": 5.40
      }
    }
  ],
  "next_page_token": "{value_to_send_to_continue_paging}"
}

```

### Step 6: Retrieve Month-End Interest

**Endpoint:&#x20;**`GET/v1/accounts/activities/INT`<br />**Purpose:&#x20;**&#x47;et the month end interest activity

**Request Example:**

```json
curl --location 'https://broker-api.sandbox.alpaca.markets/v1/accounts/activities/INT?account_id={sub_account_id}' \
--header 'Authorization: Basic <your-credentials>'

```

**Response Example:**

```json
[
    {
        "id": "5ca8b9e6-cd56-48fa-99a7-ce1f5290f312",
        "activity_type": "INT",
        "activity_sub_type": "FPSL",
        "date": "2024-07-31",
        "net_amount": 14.50,
        "description": "Securities Lending Program Interest - JUNE 2024",
        "status": "executed"
    }
]
 "5ca8b9e6-cd56-48fa-99a7-ce1f5290f312",
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

**Endpoint:&#x20;**`GET/v1/events/accounts/status`<br />**Purpose:&#x20;**&#x52;etrieve FPSL status history for an account

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

* In sandbox, FPSL account status events are not emitted. During sandbox testing, validate status changes by polling `GET /v1/accounts/{account_id}`

### Important Notes&#x20;

1. **Revenue Split:&#x20;**&#x52;evenue splits between the partner, sub account's customer, and Alpaca based on the tier configuration the partner assigned to that sub account.
2. **Collateral:&#x20;**&#x43;ollateral is posted automatically for every loan and allocated across your sub accounts as described in Step 5.
3. **Account state vs lending effect:&#x20;**&#x45;nrollment, tier changes and opt-outs on a sub account are reflected immediately in that account's response and on the SSE stream. The lending effect is not immediate. A newly enrolled sub account contributes no shares until the next business day's lendable inventory calculation, and an opted-out sub account stops receiving new loans from the next business day, with existing loans closing as borrowers return the shares.
4. **Where the partner's share goes:** The partner's share settles through monthly invoicing. Use OM loan data for attribution. Do not sum activity rows, because no activity row exists for the partner share.

<br />

*Please read&#x20;*[*Important Risk Disclosures With Respect To Participating In Fully Paid Securities Lending Transactions*](https://files.alpaca.markets/disclosures/Important+Risk+Disclosures+With+Respect+To+Participating+In+Fully+Paid+Securities+Lending+Transactions.pdf)*&#x20;carefully before deciding whether to participate in lending Fully Paid Securities or agreeing to enter into a Master Securities Lending Agreement with Alpaca Securities LLC.*

*These disclosures describe important characteristics of, and risks associated with engaging in,
securities-lending transactions.*

*The OmniSub product is offered by AlpacaDB, Inc. as a technology service for sub-accounting related to omnibus clearing services. Approval for this technology service is subject to Alpaca Securities LLC due diligence review.*