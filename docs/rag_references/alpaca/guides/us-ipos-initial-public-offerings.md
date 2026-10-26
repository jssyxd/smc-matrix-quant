# US IPOs (Initial Public Offerings)

Source: https://docs.alpaca.markets/us/docs/us-ipos-initial-public-offerings.md

---
updatedAt: 2026-05-19T15:00:58.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# US IPOs (Initial Public Offerings)

### What is IPO Investing?

IPO stands for Initial Public Offering. IPO investing provides the chance to buy shares at their first listing, before they become available on the secondary market.

### How do IPO orders work?

For an upcoming IPO, users submit a conditional order to buy (COB) based on an estimated price range, specifying the dollar amount they wish to invest. The final IPO price is set by the underwriter on the morning of the IPO, when the allocation process happens.

### Which types of orders are supported for IPOs?

Only market orders with a notional amount (dollar amount) with time in force: GTC are accepted.

### Are fractional orders or fractional shares supported?

No, fractional orders and fractional shares are not supported or allocated for IPOs. Orders will be filled in whole shares according to the notional value submitted in the COB. If the final share allocation does not use the full amount submitted, any unused buying power will be returned to the account after the allocation is completed.

### What is the lifecycle of an IPO order?

Orders can be placed once the order submission window has opened for an offering. This window generally lasts between 2-3 days. During this time, new orders can be placed and existing ones can be modified/cancelled. Before the allocation happens, a 60 minute window will be announced, which signals the final order modification/cancellation window has started and no new orders can be placed. Once this 60 minute window ends, orders become binding. If an order is canceled, the reserved buying power is released.

All of these events will be sent through Alpaca’s Broker API SSE.

### How are the funds reserved during the order lifecycle?

Once a COB is submitted and accepted, the equivalent of its notional value is reserved from the account’s buying power. Upon allocation, if the order is partially filled, the remaining buying power (initial notional value - allocated value) will be released. If the order isn’t filled at all, the whole buying power will be released back to the account.

### Can an end-user place multiple orders for the same IPO offering?

No, an end-user can only have one order per IPO offering. That order can be modified or canceled until the 60 minute window closes, when the conditional order becomes binding. However, end-users can place conditional orders on multiple IPO offerings at the same time.

### What’s the minimum value of a Conditional Order to Buy?

The minimum order is usually $100. However, this can be subject to change, depending on each offering and its underwriters.

### Are IPO shares marginable?

No. IPO assets are non-marginable until 30 days after the IPO date.

### Is it considered a day trade if IPO shares are sold on the same day they are allocated?

Yes. Selling IPO shares on the same day the company is listed is considered a day trade.

### Are there any additional clearing, settlement, or pass-through costs beyond our standard order fees?

No, there are no additional fees.

### How does trading work on the secondary market on IPO day?

Alpaca will allow only limit orders to be entered until the opening cross (when the exchange matches buy and sell orders to determine the first public trading price), which occurs when the IPO stock begins trading on the secondary market. Once the stock starts trading on the secondary market, it will behave like any other US-listed stock, and all standard order types will be available.

### Which IPOs will be available through Alpaca?

Alpaca aims to provide access to a broad range of public offerings. However, underwriter syndicates and issuers have discretion over the final allocation of IPOs, and they may meet their distribution goals with other selling groups. As a result, certain high-demand offerings may not be available through our platform.

Moreover, IPOs have both a retail and non-retail split of shares. Alpaca only participates in the allocations directed towards retail customers.

### What are some examples of previous IPOs that Alpaca's selling group was a part of?

Alpaca's selling group has participated in IPOs such as Gemini, Figure, Bullish, LiftOff, Aevex.

### How does the allocation process work?

The process for allocating shares to retail investors during an IPO is fundamentally governed by the specific rules established by the underwriters and issuers for that particular offering.

Alpaca follows an allocation engine aimed at providing a fair distribution of available shares in accordance to the supply & demand for each IPO offering. This allocation engine is required to follow the specific rules defined by the underwriter.

The allocation process is designed to try to partially fill every order coming in, even the smallest ones, whenever possible. Afterwards, the remaining allocation will be distributed on a pro-rata basis.

### Are IPO shares guaranteed?

Receiving an allocation of IPO shares is not guaranteed. The distribution process is managed by the offering's lead underwriters, and demand for new issues often exceeds the available supply. For this reason, Alpaca cannot guarantee that any particular conditional order will be filled.

### Can the final price be outside of the initial price range?

Yes, the initial price range serves as a guide for where underwriters expect an offering to price. For highly anticipated offerings, the final price can often be up to 20% outside of the price range. Orders are placed in dollar amounts specifically because the final price is not determined until the offering completes. All orders in our system remain valid for any price range below the range or up to 20% above it.

### What happens if an IPO offering gets postponed/cancelled?

The orders will be canceled and the process will restart from the beginning. All unused buying power will be returned to the account.

### Can trading be halted on IPO day?

Yes, IPO stocks may be temporarily halted due to volatility. This is a normal mechanism used by exchanges to maintain orderly markets.

### What is the timeline of the IPO allocation process?

Below is an example of an IPO timeline. Please note that not all IPOs follow this timeline, and they’re always subject to change.

| Step | Event                               | Description                                                                          | Date & Time (ET)              |
| :--- | :---------------------------------- | :----------------------------------------------------------------------------------- | :---------------------------- |
| 1    | Order Entry Window Opens            | Investors begin submitting Conditional Offers to Buy (COBs).                         | Monday, June 9 at 9:00 AM     |
| 2    | 60-Minute Notice Sent               | Final withdrawal/modification window before pricing. COBs become binding after this. | Wednesday, June 11 at 3:00 PM |
| 3    | Allocation Engine Runs              | Allocation algorithm executed based on demand and allocation.                        | Thursday, June 12 at 7:01 AM  |
| 4    | Alpaca sends allocations to partner | Allocation info sent to partner via API                                              | Thursday, June 12 at 7:30 AM  |
| 5    | IPO Date                            | Stock starts trading on listing exchange                                             | Thursday, June 12 at 11:00 AM |
| 6    | Allocations Settled                 | Shares delivered via DTC to partner clearing accounts (T+1)                          | Friday, June 13               |

*Example timeline of an IPO, always subject to change.*

### What is required when displaying available IPOs?

1. Company name
2. Ticker
3. Prospectus
4. Anticipated IPO date
5. Price Range
6. Risk disclaimer
7. FINRA rules:
   * <Anchor label="5131" target="_blank" href="https://www.finra.org/rules-guidance/rulebooks/finra-rules/5131">5131</Anchor> - restrictions on purchases by industry insiders
   * <Anchor label="5130" target="_blank" href="https://www.finra.org/rules-guidance/rulebooks/finra-rules/5130">5130</Anchor> - new issue allocation rules including spinning/flipping

All of this information is available through Alpaca’s API.

Please contact your Customer Success Manager for more information.

### Can international partners participate in IPOs?

Yes, Alpaca allows international partners to participate in IPOs. However, please refer to your local regulations to make sure you are in accordance with the local legislation.

### Does Alpaca have an anti-flipping policy?

Alpaca does not enforce an anti-flipping policy. However, Alpaca recommends that users hold IPO shares for 30 days before selling. Alpaca will monitor for abuse (such as constant flipping), which could result in future limitations.

### Are there any special compliance requirements?

End-users participating in IPOs will have to acknowledge and accept FINRA rules <Anchor label="5131" target="_blank" href="https://www.finra.org/rules-guidance/rulebooks/finra-rules/5131">5131</Anchor> and <Anchor label="5130" target="_blank" href="https://www.finra.org/rules-guidance/rulebooks/finra-rules/5130">5130</Anchor> before entering in any orders.

### How can I enable IPO Investing?

Please contact your Customer Success Manager for details on the steps required to enable IPO access for your correspondent.

***

### Disclosures

*Investments in initial public offerings (“IPOs”) involve significant risks and are not suitable for all investors. IPO securities have no prior public trading history, and the offering price may not reflect the market price following the offering. The market price of IPO securities may be volatile, and investors may lose part or all of their investment.*

*Information regarding an IPO issuer may be limited, and the issuer may have a limited operating history or may not be profitable. There can be no assurance that an active or liquid trading market will develop.*

*This material is provided for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy securities. Any offer will be made solely by means of a prospectus filed with the U.S. Securities and Exchange Commission. Investors should carefully review the prospectus, including the risk factors described therein, before investing.*