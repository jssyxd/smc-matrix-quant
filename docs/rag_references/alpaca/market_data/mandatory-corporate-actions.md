# Mandatory Corporate Actions

Source: https://docs.alpaca.markets/us/docs/mandatory-corporate-actions.md

---
updatedAt: 2026-07-08T14:43:33.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Mandatory Corporate Actions

Frequently Asked Mandatory Corporate Action Questions

# Mandatory Corporate Actions

### What are the most common corporate actions Alpaca handles, and what are they?

* **Dividends** - Dividends are payments made by companies to shareholders to account for their share of profits made by the company. The usual timeline for dividend payments is quarterly payments, but this is fully dependent on the companies themselves. There are 3 main types of dividends; a brief overview of each is added below:
* **Cash** - Cash dividends are when companies pay out cash to their shareholders to account for their profits.
* **Stock** - Stock dividends are when companies pay out stock to their shareholders to account for their profits.
* **SPLITs** - Splits are events in which a company changes its number of shares, either by splitting a share into multiple shares, or combining multiple shares into 1. In both events, the quantity that a user owns in a stock will be affected and updated according to the SPLIT ratio.
  * **Forward** - A forward split is when the company splits 1 share into multiple shares, resulting in a lower price per share.
  * **Reverse** - A reverse split is when the company combines multiple shares into 1 share, resulting in a higher price per share.
* **SPIN** - Spinoffs occur when a company provides its shareholders shares in a subsidiary or business division. Clients will continue to hold original shares and cost basis may be adjusted due to the new spin off security.
* **Mergers** - A merger is when 2 companies join to become 1 new company.\
  For the explanations below, assume company A and company B are participants in a merger, with company B being the larger of the 2 companies. Company A is being merged into company B.
  * **Stock Merger** - This is when a shareholder of a company receives shares in another company due to the participation in a merger. For example, company B allocates 2 shares of B to a shareholder in company A after the merger is done.
  * **Cash Merger** - This is when the shareholders of a company receive cash due to participation in a merger. For example, company B pays 100$ to a shareholder in company A after the merger is done.
  * **Stock and Cash Merger** - This is when the shareholders of a company receive both stock & cash due to participation in a merger. For example, company B allocates 2 shares of B & pays 100$ to a shareholder in company A after the merger is done.
* **Full Call** - This is when the shareholders of a company receive cash due to the company exercising their right to purchase shares from shareholders. This is usually done on preferred shares.
* **Final Liquidation** - This is when the shareholders of a company receive cash and the underlying shares are removed. This is usually done on SPACs or securities such as CVRs and escrow shares.
* **Partial Liquidation** - This is when the shareholders of a company receive cash, but the underlying shares continue to be held in anticipation of potential future distributions. This is usually done on securities such as CVRs and escrow shares.
* **NC** - A name change occurs when a company changes its legal name, regardless of the reason behind the change. When this happens, the underlying asset might be affected in multiple ways:
  * **Symbol change** - This is when the symbol of the underlying asset changes as part of the name change event.
  * **CUSIP change** - This is when the CUSIP of the underlying asset changes as part of the name change event.
  * **Symbol & CUSIP change** - This is when both the symbol & CUSIP of the underlying asset change as part of the name change event.\
    Note: There might also be no change in either CUSIP or symbol, in which case the update to the asset will occur without triggering an NC event.

**Examples** of each type of Mandatory Event above are available in the docs [here](https://docs.alpaca.markets/docs/draft-sse-events#non-trade-activities-events).

***

### Which of all the dates in the response body should we use in each transaction detail?

Settle date.

***

### How does Alpaca handle stock-and-cash mergers?

Stock and cash mergers are mandatory events, so they are handled like all other mandatory events.

***

### For stock and cash mergers, what would we receive as NTAs?

You should receive 3 NTA events:

* 1 for the removal of the original security
* 1 for the allocation of new shares
* 1 for the allocation of cash

A sample is added below. This was a stock-and-cash merger with 5 shares of `384CVR015` and `$9.95` allocated for every `1 share` of `GRCL`:

**Removal of original security:**

```Text json
{  
    "id": "",  
    "qty": -284.678660686,  
    "price": 6.04,  
    "status": "correct",  
    "symbol": "GRCL",  
    "entry_type": "MA",  
    "net_amount": 0,  
    "description": "Stock Merger 5 384CVR015 for 1 GRCL",  
    "settle_date": "2024-02-29",  
    "system_date": "2024-02-29",  
    "per_share_amount": null  
}
```

**Allocation of new shares:**

```Text json
{  
    "id": "",  
    "qty": 1423.39330343,  
    "price": 1.21,  
    "status": "correct",  
    "symbol": "384CVR015",  
    "entry_type": "MA",  
    "net_amount": 0,  
    "description": "Stock Merger 5 384CVR015 for 1 GRCL",  
    "settle_date": "2024-02-29",  
    "system_date": "2024-02-29",  
    "per_share_amount": null  
}
```

In the removal & allocation of shares events, the quantity field represents the number of shares removed or allocated.

**Allocation of cash:**

```Text json
{  
    "id": "",  
    "qty": 0,  
    "price": null,  
    "status": "executed",  
    "symbol": "GRCL",  
    "entry_type": "MA",  
    "net_amount": 2832.55,  
    "description": "Stock Cash Merger 5 384CVR015 and $9.95 for 1 GRCL",  
    "settle_date": "2024-02-29",  
    "system_date": "2024-02-29",  
    "per_share_amount": null  
}
```

In the cash events, `net_amount` will reflect the cash amount allocated.

***

### At a user level, are cash mergers always for 100% of the position, or are there cases where a user might keep 50% of their position and receive cash for the remaining 50%?

On a stock and cash merger, all shares of the old security are removed. The new stock and cash allocation are based on a ratio determined by the company based on current market conditions.

***

### Does Alpaca handle recapitalization?

Alpaca does not currently handle debt instruments. Recapitalization events deal with debt instruments and, accordingly, are not available on Alpaca.

***

### How does Alpaca handle tax withholding?

We receive a net rate per share from DTC based on the country of the company.

1. If it is a foreign company, then there may be a foreign dividend withholding tax that is withheld from the payment we receive from DTC.  This payment would represent the `DIV` NTA entry.
2. With a foreign partner, there may be an additional withholding (the `DIVNRA` entry) based on their country and the withholding percentage for that country.  If the company that paid the dividend has a tax exempt foreign status, then the `DIVNRA` entry may not apply.

In summary, you would receive a `DIV` event (the dividend) and a `DIVNRA` (the tax withholding) event. Noting that if a `DIVNRA` value is `< 0.01`, however, you will not receive a `DIVNRA` activity.

***

### Are there any cases where Alpaca does not withhold taxes on dividends?

If the company is a foreign company, then there may not be any `DIVNRA` withholdings

***

### Does the amount sent in the DIV event include the tax? In other words, to calculate the final amount, the amount in the DIVNRA event needs to be deducted from the amount on DIV event.

Yes, the amount sent in the `DIV` event is without the tax `DIVNRA`, so you need to determine the net amount after the `DIVNRA` by taking the `DIV` and reducing it by the `DIVNRA`.

***

### Are symbol changes notified via the SSE Events?

No, as of now the symbol changes need to be seen via the <Anchor label="Assets API" title="https://docs.alpaca.markets/reference/getassets" href="https://docs.alpaca.markets/reference/getassets">Assets API</Anchor>. Syncing at regular intervals is what is recommended to make sure you are up-to-date with the symbol changes.

***

### Do we have a new asset object, if there is a symbol change?

The answer is a YES and a NO. The reason for that is, if there is simply a symbol change without the CUSIP being updated, in that case, we just update the existing asset by updating the Symbol. If there is a CUSIP change, the current asset becomes INACTIVE and a new Asset Object is added the the response of the <Anchor label="Assets API" title="https://docs.alpaca.markets/reference/getassets" href="https://docs.alpaca.markets/reference/getassets">Assets API</Anchor>.

***

### What happens when a stock split occurs?

For reverse splits all GTC orders will be canceled that were in the market with a trade date prior to the effective date of the reverse split.\
For forward splits, GTC buy limits and sell stops are adjusted. The price and quantity will be adjusted. Other orders will not be adjusted.

Please note that this piece is for general informational purposes only. The examples above are for illustrative purposes only. Alpaca does not provide investment, tax, or legal advice. Please consult your own independent advisor as to any investment, tax, or legal statements made herein.

<br />

### How can I tell an order was canceled by a corporate action?

Alpaca cancels open GTC orders on symbols that have an upcoming mandatory corporate action (e.g. splits, symbol/CUSIP change, merger). This behavior is enabled per correspondent (check with your CSM team if this has been enabled or not) .

You will not see the cause on the REST `GET /orders` response — the order's `status` is simply `canceled`. To distinguish CA-driven cancels from user-driven cancels, listen to the [Trade Events SSE](https://docs.alpaca.markets/reference/subscribetotradev2sse) and inspect the top-level `reason` field:

* `reason = "CORPORATE_ACTION"` on a `canceled` event → cancel was initiated by CA processing.
* `reason` absent → user- or TIF-driven cancel.