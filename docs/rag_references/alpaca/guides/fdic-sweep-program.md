# FDIC Sweep Program

Source: https://docs.alpaca.markets/us/docs/fdic-sweep-program.md

---
updatedAt: 2026-07-07T14:19:30.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# FDIC Sweep Program

### What is an FDIC Sweep program?

An FDIC Bank Sweep Program, is an insured deposit program that allows customers who opt-in to earn interest on eligible cash balances and offers expanded FDIC insurance coverage on those cash balances\*.

### How does FDIC sweep work?

Through the Alpaca FDIC Bank Sweep Program, eligible uninvested cash in a customer brokerage account can be swept to one or more of the participating [FDIC Sweep Program Banks](https://alpaca.markets/deposit-bank-list), where the swept cash becomes eligible for FDIC insurance up to a total maximum of $1,000,000 (FDIC insurance coverage is limited to $250,000 at each program bank)\*.

### How much is insured?

Currently FDIC insurance up to a total maximum of $1,000,000 (FDIC insurance coverage is limited to $250,000 at each program bank)\*.

### What are the eligibility requirements?

1. Partners must be using a fully disclosed structure (not available to Partners with an omnibus structure at launch).
2. A customer must elect to opt-in their account into the program:\
   *Existing:* Customers with an existing Alpaca account that have signed a Customer Agreement before August 21, 2024 (prior to revision 22.2024.08) must provide opt-in consent by signing the updated Customer Agreement and be presented the[ Alpaca FDIC Bank Sweep Program Terms and Conditions](https://files.alpaca.markets/disclosures/Alpaca+FDIC+Bank+Sweep+Program+Terms+and+Conditions.pdf) on your front-end. Our Tech Integration team will help walk you through that process and the requirements.\
   *New:* Those who signed the Customer Agreement on or after August 21, 2024 (revision 22.2024.08 or newer) are automatically eligible to be enrolled.
3. The customer account has a base currency of USD.
4. The customer account is pre-funded (i.e., non-JIT).

### How does a user enroll?

Please see our blog article [Getting Started with High-Yield Cash for Broker API](https://alpaca.markets/learn/getting-started-with-high-yield-cash-for-broker-api)

### How can a user opt-out of the FDIC Sweep Program?

To opt-out a user from the Alpaca FDIC Bank Sweep Program, please email <support@alpaca.markets>.

### What account types are supported?

We are currently supporting Individual Taxable and Custodial accounts at this time.

### What are the benefits of a user enrolling?

*Income:* Earn interest on eligible cash balances\
*Security:* Up to $1m FDIC insurance\* per customer via FDIC Bank Sweep\
*Liquidity:* Daily liquid, and available for use as buying power for trading activities

<https://alpaca.markets/blog/alpacas-global-high-yield-cash-api/>

### How does a user withdraw funds from the program?

Customers are unable to withdraw directly from the program banks. Customers must therefore, request a withdrawal or transfer on the partner’s front-end the same way it’s implemented today, for which the corresponding cash will be swept out of the program to cover the request.

### How can a user opt out of a specific bank in the program?

Currently, clients must opt out of the entire program by unenrolling. In an upcoming release, we aim to offer the ability to opt-out at the individual program bank level.

### How frequently does interest accrue?

Daily

### How often is interest compounded?

Monthly

### When is interest available?

Last business day of the month. The accrued interest is booked to the customer account, but remains within the program to compound into yield.

### What decimal is interest rounded to?

Daily accrued interest is rounded to 4 decimals, while month-end realized interest is rounded to 2 decimals

### When can cash be swept into and out of the program?

Daily, excluding US weekends and holidays

### Is the APR/APY fixed or variable?

The Program Rate is variable and subject to change without notice.

### How can I access the FDIC Bank Sweep Program Deposit Bank List?

[Deposit Bank List](https://alpaca.markets/deposit-bank-list)

### Is there more detailed information available?\*\*

[Alpaca Securities LLC FDIC Bank Sweep Program Terms and Conditions](https://files.alpaca.markets/disclosures/Alpaca+FDIC+Bank+Sweep+Program+Terms+and+Conditions.pdf)

### What are the key timing considerations to be mindful of?

*11:45 am ET*

-The cutoff for when a deposit can be settled and swept into the program same-day for accounts with cash\_interest.status = ACTIVE.\
-The cutoff for when a partial withdrawal request can be facilitated out of the program.\
-The cutoff for when an Assignment API request will process the same-day.\
-The cutoff for when a Reassignment API request will process the same-day.\
-The cutoff for when an Unenroll API request will process the same-day.

*12:15 pm - 2:00 pm ET*

When cash\_interest.status updates cycle from PENDING\_CHANGE to ACTIVE or INACTIVE.

*6:00 pm ET*

When the [Account Activities endpoint](https://docs.alpaca.markets/reference/getaccountactivitiesbytype-1) is updated to reflect realized interest credited to accounts on the last business day of the month. The qty will be reflected within that day’s cash\_interest value from the EOD Cash Interest Details response.

*8:00 pm ET*

When the[ EOD Cash Interest Details endpoint](https://docs.alpaca.markets/reference/get-v1-get-eod-cash-interest-report) is updated to reflect that day’s ending state.

\*Alpaca Securities customers that enroll in the FDIC Bank Sweep are potentially eligible for enhanced FDIC pass-through insurance coverage. Neither Alpaca nor Alpaca Securities are FDIC-insured. FDIC pass-through insurance coverage is subject to various conditions. The Program’s enhanced FDIC insurance coverage is limited to the aggregate number of participating program banks, multiplied by the FDIC insurance limit (i.e., $250,000). The total number of program banks is subject to change and Alpaca Securities may not utilize all program banks at all times which will affect the Program’s enhanced FDIC insurance coverage amount. In addition, if a customer has a direct banking relationship with a program bank this may affect the amount of funds that are potentially eligible for FDIC-pass through insurance coverage. There is no guarantee that customer funds will be held in such a manner as to maximize possible FDIC pass-through insurance coverage.

Neither Alpaca, nor any of its affiliates or subsidiaries is a bank.

Alpaca Securities offers a cash management program pursuant to the FDIC Bank Sweep. Customer funds are treated differently and are subject to separate regulatory regimes depending on whether customer funds are held in their brokerage account or within the FDIC Bank Sweep. Specifically, Alpaca Securities is a member of the Securities Investor Protection Corporation (SIPC), which protects securities customers of its members up to $500,000 (including $250,000 for claims for cash). The Federal Deposit Insurance Corporation (FDIC) insures up to $250,000 per deposit against the failure of an FDIC member bank. Customer funds held in brokerage accounts are SIPC insured, but are not eligible for FDIC insurance coverage. Funds maintained in the FDIC Bank Sweep are intended to be eligible for pass-through FDIC insurance coverage, but are not subject to SIPC coverage. FDIC insurance coverage does not protect against the failure of Alpaca, Alpaca Securities, or any of its or their affiliates and/or malfeasance by any Alpaca or Alpaca Securities employee. Program banks that participate in the FDIC Bank Sweep are not members of SIPC and therefore funds held in the Program are not SIPC protected. Please see alpaca.markets/disclosures for important additional disclosures regarding Alpaca Securities brokerage offering as well as FDIC Bank Sweep terms and conditions.