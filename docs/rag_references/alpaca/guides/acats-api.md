# ACATS API

Source: https://docs.alpaca.markets/us/docs/acats-api.md

---
updatedAt: 2026-09-01T22:20:11.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# ACATS API

### Can a user submit multiple ACATS at once?

**Incoming ACATS to Alpaca**, a user can submit multiple ACATS requests provided that they are either coming from different contra brokers or coming from the same contra broker but for different account numbers.

**Outgoing ACATS sent by Alpaca**, we only allow one outgoing ACATS per account at a time. We also do not support both incoming and outgoing ACATS to be processed in parallel.

<br />

### What are the eligibility criteria for a user to submit an incoming ACATS request to Alpaca?

* The user’s account must be in a KYC approved state meaning the account status is one of the following; ACTIVE, APPROVED, or ACCOUNT\_UPDATED.
* The assets scoped for the transfer must be supported for ACATS transfer by Alpaca. See supported assets in the question below
* The user’s name, tax ID number, and account types must match between the contra broker and Alpaca.

<br />

### What are the eligibility criteria for a user to have an outgoing ACATS transfer successfully processed and sent by Alpaca?

<br />

* The account cannot be enrolled in our High Yield cash program. If the account is already enrolled then our team will disable it in order to process the ACATS request.
* If the user is requesting a full transfer then fractional shares and any ACATS unsupported assets cannot be transferred. Any fractional shares or unsupported assets held by the user will be liquidated before being sent out in the ACATS transfer.
* The account cannot have any pending debit interest unpaid. If there is an unpaid debit balance then our team may hold funds to cover any pending interest charges before sending out the funds in the ACATS transfer.

<br />

### What kind of assets are supported for ACATS transfers?

We support transferring in all US securities that are tradable on Alpaca’s platform as well as cash. Unsupported assets include:
Options (supported for outgoing but not for incoming ACATS at this time)
Crypto
Fixed income
Mutual funds
Bonds
Derivatives (futures or event contracts)
Annuities
Certificates of deposits (CDs)
OTC Stocks
CVRs
Warrants
Other assets that haven't been identified as transferable assets

<br />

### What if a user’s outside account has unsupported assets?

The user should either liquidate the unsupported assets from their outside account and then request a full transfer or request a partial transfer and only request the transfer with the supported assets. If the user initiates a request for an account holding unsupported assets, the transfer will be rejected.

<br />

### What account types are supported for ACATS?

For incoming and outgoing ACATS transfers, we support transferring into and out of individual, roth IRA, traditional IRA, entity, and custodial accounts. We also support transferring a joint account into an individual account held at Alpaca or the opposite of transferring an individual account’s assets into an external joint account held at another brokerage. Note this is the only case where the account types are not required to match.

<br />

### Is there any tax implication if a user transfers their outside IRA account to their IRA at Alpaca via ACATS?

No this is considered an IRA Transfer which is a nontaxable event.

<br />

### What’s a DTC number?

A DTC number is the unique 4 digit number assigned to each clearing broker by DTCC. This number is used to facilitate transfers by identifying which broker the assets should be sent to or requested from. You can find your brokerage’s DTC number by looking it up on their FAQ page or contacting them directly.

<br />

### What is Alpaca’s DTC number?

Alpaca’s DTC number is 3021.

<br />

### Is cost basis data transferred along with the positions for incoming ACATS to Alpaca?

Cost basis data will be added to the positions when it is provided by the contra broker. The contra broker has up to 15 calendar days to send the cost basis information after the transfer is settled. If we don’t get this information, you need to ask the other brokerage to send this information to us to remedy this issue. In general the flow for cost basis will follow this flow:

<Image src="https://files.readme.io/b04c858cadd854d5caec25b66f2607a259d77318a14085c7e958935cdfec6a87-image.png" align="left" wrap={true} />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

<br />

### How long does it take for an ACATS transfer to process?

It can take anywhere from 5-7 business days for assets to settle but cost basis data can arrive later.

<br />

### Is an ACATS transfer considered final after the assets have settled and cost basis data has arrived?

The transfer is considered final after assets have settled and cost basis data has arrived but please note that residual transfers can continue to come into Alpaca but these would be recorded as separate, distinct ACATS transfers. This can happen for example in the event of the outside account being credited dividends after the funds have already been sent out by the contra broker.

### Can I track the transfer?

Yes, we provide both a GET ACATS Transfer endpoint for pulling the status, along with the transfer details, at any given moment in time as well as an SSE endpoint for pulling real time updates to the ACATS transfer throughout its lifecycle.

### What happens if a transfer is rejected?

We provide both the rejection reason, originating from DTCC, and a freeform rejection message field that our team may use to send a custom message with the details of the reason for rejection. We encourage you to build rejection flows into your UX wherever possible. For in depth guidance on what each rejection reason means and what action is needed from you refer to the question below.

<br />

### What are some of the most common reasons for an ACATS transfer to be rejected?

An account transfer can be rejected for a number of reasons, including the following:

<br />

* The account number was entered incorrectly.
* Account information such as name, SSN/Tax ID, or account type does not match between brokers
* The outside account contains unsupported assets. We provide an asset level breakdown for each ACATS transfer which includes the status of each asset via API. This endpoint can be used to easily identify which assets are unsupported so you can guide your user to resubmit the transfer request but excluding these assets.
* You haven't met the margin balance requirements. Your account will need to support the margin balances and positions you transfer in to avoid any margin calls or account deficits.

### Do I need to submit a new transfer request if the transfer was rejected?

Yes, if a transfer is rejected that is considered a final state so the user must resubmit a new request if they still wish to transfer their account.

<br />

### What action should I take when a transfer is rejected?

A breakdown of rejection reasons, what it means, and what action you can take is documented here:

<br />

<br />

| Rejection Code                                         | What It Means                                                                                                                                                                                                                                   | Action Required                                                                                                                                                                                                |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SS\_TAX\_ID\_MISMATCH                                  | The SSN or TIN provided doesn't match the delivering firm's records                                                                                                                                                                             | Verify correct SSN/TIN with customer; Customer should ensure tax ID is accurate and matching and both firms and resubmit with accurate tax ID                                                                  |
| ACCOUNT\_TITLE\_MISMATCH                               | Account owner name or registration type doesn't match (e.g., individual vs. IRA)                                                                                                                                                                | Confirm exact account title with delivering firm; ensure name spelling and account type match exactly; resubmit                                                                                                |
| DOCUMENTATION\_NEEDED                                  | Delivering firm requires additional paperwork (authorization forms, legal docs, etc.). This is sometimes used as a general rejection reason, so the comments provided would provide more insight into what is needed for a successful transfer. | Contact delivering firm to identify required documents; obtain and submit necessary paperwork; resubmit. If no documentation needed, work with firm to understand what is needed to resubmit                   |
| ACCOUNT\_FLAT                                          | Account is empty or already closed—no assets to transfer; or non transferable assets in the account (e.g only fractional shares)                                                                                                                | Verify account status with customer; confirm assets exist, and are transferable before resubmitting; may need to cancel transfer.                                                                              |
| INVALID\_ACCOUNT\_NUMBER                               | Account number doesn't exist, is incorrect, or improperly formatted                                                                                                                                                                             | Double-check account number with customer and delivering firm; verify format requirements; resubmit with correct number                                                                                        |
| DUPLICATE                                              | Another transfer request already in process or recently completed                                                                                                                                                                               | Check for existing transfer; cancel duplicate or wait for original to complete; Confirm with client if duplicate may be going to another firm; submit new request only if original was cancelled               |
| ACCOUNT\_IN\_DISTRIBUTION\_OR\_TRANSFER                | Account involved in another transfer<br />(ACATS or ACH), estate distribution, or legal proceeding                                                                                                                                              | Wait for current process to complete; Customer to confirm with delivering firm on timing; submit new request once account is available                                                                         |
| CLIENT\_RESCINDED                                      | Customer contacted delivering firm and cancelled the transfer                                                                                                                                                                                   | Confirm customer intent; if transfer still desired, obtain fresh authorization and submit entirely new request; Customer needs to confirm with delivering firm they are authorizing the transfer request again |
| MISSING\_AUTHORIZATION\_SIGNATURE                      | Required customer signature missing from authorization form.  This is sometimes used as a general rejection reason, so the comments provided would provide more insight into what is needed for a successful transfer.                          | Obtain a properly signed authorization form from the customer; submit a new transfer request with complete documentation. If no signature is needed, work with firm to understand what is needed to resubmit   |
| ACCOUNT\_VIOLATES\_CREDIT\_POLICY\_OF\_RECEIVING\_FIRM | The account doesn't meet Alpaca's margin, risk, or account type requirements. Assets in the transfer may be unsupported by Alpaca                                                                                                               | Review Alpaca's account policies; may need to adjust account type, close margin positions, non-transferrable assets, or transfer to different account structure                                                |
| UNRECOGNIZED\_FOR\_RESIDUAL\_CREDIT\_BALANCE           | Cannot process remaining cash balance in transfer                                                                                                                                                                                               | Contact Alpaca operations for clarification; may need to handle cash separately or adjust transfer type                                                                                                        |
| PARTIAL\_TRANSFER\_DELIVERER\_INITIATED\_REJECT        | Alpaca doesn't accept this deliverer-initiated partial transfer                                                                                                                                                                                 | Coordinate with delivering firm; may need to initiate as receiving-firm partial transfer instead                                                                                                               |
| FAIL\_REVERSAL\_REJECT                                 | Rejecting correction of previously failed transfer                                                                                                                                                                                              | Contact Alpaca operations to determine next steps; may need to submit fresh transfer request                                                                                                                   |
| RECLAIM\_REJECT                                        | Rejecting request to return assets to delivering firm                                                                                                                                                                                           | Contact Alpaca operations to determine next steps                                                                                                                                                              |
| MUTUAL\_FUND\_CLEANUP                                  | Rejecting mutual fund residual/cleanup transaction                                                                                                                                                                                              | Alpaca may not support certain mutual funds; verify fund eligibility                                                                                                                                           |
| INVALID\_PARTICIPANT                                   | Broker DTCC number is invalid or incorrectly formatted                                                                                                                                                                                          | Verify correct DTCC participant number for delivering firm; ensure firm is DTCC/ACATS eligible, and that the customer is not using same broker for both sides; resubmit with correct number                    |