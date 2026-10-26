# Voluntary Corporate Actions

Source: https://docs.alpaca.markets/us/docs/voluntary-corporate-actions.md

---
updatedAt: 2025-09-24T23:20:19.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Voluntary Corporate Actions

Frequently Asked Voluntary Corporate Action Questions

# Voluntary Corporate Actions

### How are voluntary corporate actions communicated to customers?

Alpaca works with a third party vendor to communicate voluntary corporate actions. Emails are sent to each customer when there is a voluntary corporate action with details and instructions on how to take action. These emails will have the broker partner name on them with an option to add a logo.

***

### Can we block all voluntary actions such as rights distribution?

No, those have to be sent to customers. There is a cost associated with these, which usually deters customers from acting on them. The cost is $100 per client per voluntary corporate action, which is stated in the email. Alpaca can reject a customer's decision to act if there is no cash in the account, which would be the case here.

***

### Why is there a field ‘qty’ that is != 0 in change name response body?

CUSIP change, symbol change, or a combination of both lead to this happening. Basically, there are two NC event the qty will be negative to remove the old symbol and positive when adding the new one.

***

### What are the possible voluntary actions?

* **Dutch Auction/Purchase/Tender Offer:** This is when a company wants to purchase your shares at a specific price or when they ask you to choose the price at which you would be willing to sell your shares.
* **Conversion/Exchange Offer:** This is when a company offers to exchange your shares for a new type of in-kind share like bonds or fixed income securities.
* **Election Merger:** This is when a company offers to pay cash, new shares, or a combination of both for your currently held shares.
* **Consent Request:** This is when a company usually asks for your permission, as a bondholder, to change the bond agreement.
* **Rights Offer:** This is when a company offers to sell you new shares (typically below the market price) before they offer these shares publicly.
* **Warrant Exercise:** This is when a company offers to sell you new shares at a specific exercise price.  Expirations can be up to 5 years in the future.

***

### What are unit splits, and how does Alpaca handle them?

* Units are a type of security that usually contain a combination of common shares and warrants. Rights may also be included, but this is less common.
* Unit Splits can be either a mandatory event or a voluntary event
  * For a mandatory event
    * Clients will receive a combination of common shares and warrants based on the unit split ratio; no action is needed by the client
    * The REORG entry type will be used for this event
  * For a voluntary event
    * Clients can choose whether or not to split their units as long as the agent window is open to perform the unit split.
    * We don't usually have a lot of clients trading units, but as long as the window is open for a unit split, a Partner can request one at any time. This will have the $100.00 voluntary submission fee attached to it.
    * The VOF entry type will be used for this event

***

### How are voluntary corporate actions processed at Alpaca?

On Alpaca's end, voluntary corporate actions use 3 main NTA activity types: VOF, REORG, and FEE:

* `VOF` is used when there is a change in shares.
* `REORG` is used when there is a change in cash.
* `FEE` is used to book the fee associated with a VCA.

The general process at Alpaca to handle voluntary corporate actions is as follows:

1. The client's underlying shares are moved to a contra/placeholder security; this way, they don't liquidate the shares that were elected
   * This would be done with 2 `VOF` entries (1 to remove underlying shares and 1 to allocate contra)
2. Once we receive the allocation from DTC (which is normally a week or two after the client's election is submitted), we will then remove the contra security and allocate the voluntary payment (cash or new shares usually)
   * If they are receiving cash; there would be 1 `VOF` entry to remove the contra shares and 1 `REORG` entry to allocate the cash
   * If they are receiving new shares; there would be 2 `VOF` entries to remove the contra shares and allocate the new shares

Below are the different offer types and the standard Alpaca NTAs that would be created for them, noting that there might be slight differences on a case by case scenario:

* **Purchase/Tender offer** - explained [here](https://www.investopedia.com/terms/t/tenderoffer.asp), would be a combination of:
  * 3 `VOF`
    * Remove the underlying shares
    * Allocate contra shares
    * Remove the contra shares when we receive payment from DTC
  * `REORG` to allocate the cash to the client when we receive payment from DTC
  * `FEE` Entry
* **Exchange offer** - explained here, would be a combination of:
  * 4 `VOF`
    * Remove the underlying shares
    * Allocate contra shares
    * Remove the contra shares when we receive payment from DTC
    * Allocate the new shares when we receive payment from DTC
  * `FEE` Entry
* **Rights/Warrant offer** - explained here, would be a combination of:
  * Either 2 `VOF`
    * Distribution of the rights
    * Exercise the rights
  * OR 4 `VOF` (if there is a move to Contra needed similar to the previous cases)
  * 2 `FEE` Entries.
  * There might also be an additional `REORG` (for mandatory events like a worthless removal).
* **Consent request** - Doesn't apply

## Sample NTAs

Some sample NTAs that you would receive for the offer types mentioned above are added for reference:

### Sample Purchase/Tender Offer

`MNST` shares removed with a `VOF` entry

```Text json
{  
  "id": "f2ad14c5-f46b-47bd-b6cc-422dd535f086",  
  "qty": -97,  
  "price": null,  
  "status": "executed",  
  "symbol": "MNST",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Monster Beverage voluntary submission (expiration 06/05/24)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

`611NSP014` (the contra security) was allocated with a `VOF` entry

```Text json
{  
  "id": "221e1a62-5e43-4288-b320-0921c6bc56cb",  
  "qty": 97,  
  "price": null,  
  "status": "executed",  
  "symbol": "611NSP014",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Monster Beverage voluntary submission (expiration 06/05/24)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

`611NSP014` was removed with a `VOF` entry after allocation was received from DTC

```Text json
{  
  "id": "aeb0dc92-1197-4c33-96f6-2545b43d37c6",  
  "qty": -97,  
  "price": null,  
  "status": "executed",  
  "symbol": "611NSP014",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Monster Beverage voluntary allocation (expiration 06/05/24)",  
  "settle_date": "2024-06-12",  
  "system_date": "2024-06-12",  
  "per_share_amount": null  
}
```

Cash was allocated to the client using a `REORG` entry

```Text json
{
  "id": "6c452d1f-bcec-4300-b857-faae17f8624e",
  "qty": 0,
  "price": null,
  "status": "executed",
  "symbol": "611NSP014",
  "entry_type": "REORG",
  "net_amount": 5141,
  "description": "Monster Beverage voluntary allocation (expiration 06/05/24)",
  "settle_date": "2024-06-12",
  "system_date": "2024-06-12",
  "per_share_amount": null
}
```

Fee was booked using a `Fee` entry

```
{  
  "id": "2af9d6d2-c1bd-49f1-a9df-6d14a13f4af5",  
  "qty": 0,  
  "price": null,  
  "status": "executed",  
  "symbol": "",  
  "entry_type": "FEE",  
  "net_amount": -100,  
  "description": "Monster Beverage Voluntary Submission Fee (expiration 06/05/24)",  
  "settle_date": "2024-06-12",  
  "system_date": "2024-06-12",  
  "per_share_amount": null  
}
```

### Sample Exchange Offer

`CMI` Shares were removed using a `REORG` entry

```
{  
  "id": "7642d450-69d0-4d7e-87e0-62b0b94a3097",  
  "qty": -99,  
  "price": null,  
  "status": "executed",  
  "symbol": "CMI",  
  "entry_type": "REORG",  
  "net_amount": 0,  
  "description": "Voluntary Tender Election for Cummins, Inc. (CMI)",  
  "settle_date": "2024-03-12",  
  "system_date": "2024-03-12",  
  "per_share_amount": null  
}
```

`231992017` (the contra security) was allocated with a `REORG` entry

```Text json
{  
  "id": "c163bd41-c9d7-4204-816e-1b8bd98091df",  
  "qty": 99,  
  "price": null,  
  "status": "executed",  
  "symbol": "231992017",  
  "entry_type": "REORG",  
  "net_amount": 0,  
  "description": "Voluntary Tender Election for Cummins, Inc. (CMI)",  
  "settle_date": "2024-03-12",  
  "system_date": "2024-03-12",  
  "per_share_amount": null  
}
```

Fee was booked using a `Fee` entry

```Text json
{  
  "id": "d9a91441-558a-41f9-8926-bd9446308c58",  
  "qty": 0,  
  "price": null,  
  "status": "executed",  
  "symbol": "",  
  "entry_type": "FEE",  
  "net_amount": -100,  
  "description": "Voluntary Tender Election for Cummins, Inc. (CMI) Fees",  
  "settle_date": "2024-03-12",  
  "system_date": "2024-03-12",  
  "per_share_amount": null  
}
```

`231992017` (the contra security) shares were removed using a `VOF` entry

```
{  
  "id": "58259fb2-973b-407d-8e18-e7080ae65bdc",  
  "qty": -99,  
  "price": null,  
  "status": "executed",  
  "symbol": "231992017",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Voluntary Tender Payment for Cummins, Inc. (CMI)",  
  "settle_date": "2024-03-20",  
  "system_date": "2024-03-20",  
  "per_share_amount": null  
}
```

`ATMU` shares were allocated with a `VOF` entry

```Text json
{  
  "id": "04226589-e3a5-43fd-a69e-dbda35546b3e",  
  "qty": 1190,  
  "price": 22.33,  
  "status": "executed",  
  "symbol": "ATMU",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Voluntary Tender Payment for Cummins, Inc. (CMI)",  
  "settle_date": "2024-03-20",  
  "system_date": "2024-03-20",  
  "per_share_amount": null  
}
```

### Sample Rights Offer

`FEE` for the new shares:

```Text json
{  
  "id": "f71b410e-b9c4-4071-b627-f5ea92633e89",  
  "qty": 0,  
  "price": null,  
  "status": "executed",  
  "symbol": "",  
  "entry_type": "FEE",  
  "net_amount": -2125,  
  "description": "Barnes & Noble Rights Exercise Cost (067RGT019)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

DTC Fee

```Text json
{  
  "id": "8c82a56a-7602-4a83-977b-aafd1cea3db8",  
  "qty": 0,  
  "price": null,  
  "status": "executed",  
  "symbol": "",  
  "entry_type": "FEE",  
  "net_amount": -100,  
  "description": "Barnes & Noble Rights Exercise Submission Fee (067RGT019)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

`VOF` to remove underlying security

```Text json
{  
  "id": "47007871-2f92-4adf-b7dc-efc6b1550fe7",  
  "qty": -2500,  
  "price": null,  
  "status": "executed",  
  "symbol": "067RGT019",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Rights Exercise (symbol BNED; expiration 06/05/24)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

`VOF` to allocate contra security

```Text json
{  
  "id": "01233557-9f6b-403f-8832-6b70f057d85c",  
  "qty": 2500,  
  "price": null,  
  "status": "executed",  
  "symbol": "067BAS012",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Rights Exercise (symbol BNED; expiration 06/05/24)",  
  "settle_date": "2024-06-05",  
  "system_date": "2024-06-05",  
  "per_share_amount": null  
}
```

`VOF` to remove contra security

```Text json
{  
  "id": "42830cc1-2dfb-4d6f-959b-463c148774ac",  
  "qty": -2500,  
  "price": null,  
  "status": "executed",  
  "symbol": "067BAS012",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Rights Payment (symbol BNED; expiration 06/05/24)",  
  "settle_date": "2024-06-11",  
  "system_date": "2024-06-11",  
  "per_share_amount": null  
}
```

`VOF` to allocate new shares

```Text json
{  
  "id": "43eb77dd-1b8c-4b3d-81b1-647a00436aa3",  
  "qty": 42500,  
  "price": 0.09,  
  "status": "executed",  
  "symbol": "BNED",  
  "entry_type": "VOF",  
  "net_amount": 0,  
  "description": "Rights Payment (symbol BNED; expiration 06/05/24)",  
  "settle_date": "2024-06-11",  
  "system_date": "2024-06-11",  
  "per_share_amount": null  
}
```

In this case, there was also an extra `REORG` due to a mandatory event (worthless removal)

```Text json
{  
  "id": "89f26a95-2624-43ab-a95c-a17db20dc361",  
  "qty": -150,  
  "price": null,  
  "status": "correct",  
  "symbol": "067RGT019",  
  "entry_type": "REORG",  
  "net_amount": 0,  
  "description": "Worthless Removal - 067RGT019",  
  "settle_date": "2024-06-13",  
  "system_date": "2024-06-13",  
  "per_share_amount": null  
}
```

Please note that this piece is for general informational purposes only. The examples above are for illustrative purposes only. Alpaca does not provide investment, tax, or legal advice. Please consult your own independent advisor as to any investment, tax, or legal statements made herein.