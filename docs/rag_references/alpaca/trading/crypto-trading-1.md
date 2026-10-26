# Crypto Trading

Source: https://docs.alpaca.markets/us/docs/crypto-trading-1.md

---
updatedAt: 2026-04-20T20:41:19.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Crypto Trading

Alpaca supports crypto trading 24 hours a day, every day. Crypto is available for testing in sandbox, in case you want to allow your users to trade crypto please reach out to the Sales or Developer Success team.

<Callout icon="🌍" theme="default">
  ### To view the supported US regions for crypto trading, click [here](https://alpaca.markets/support/what-regions-support-cryptocurrency-trading).
</Callout>

# Enabling Crypto for an Account

To enable crypto trading for an account, the crypto agreements must be signed by the user. All account balances will represent the crypto trading activities.

In the case of new users, the crypto agreement can be submitted via the Accounts API where `crypto_agreement` is part of the agreements attribute.

*Part of the request*

```json
{
  "agreements": [
    {
      "agreement": "crypto_agreement",
      "signed_at": "2023-01-01T18:09:33Z"
    }
  ]
}
```

In the case of existing users the account has to be updated with the `crypto_agreement` which can be submitted on the `PATCH /v1/accounts/{account_id}` endpoint.

*Part of the request*

```json
{
  "agreements": [
    {
      "agreement": "crypto_agreement",
      "signed_at": "2023-01-01T18:13:44Z",
      "ip_address": "185.13.21.99"
    }
  ]
}
```

Once the crypto agreement is added to the user account no further edits can be made to the agreements.

To determine whether the account is all set to start trading crypto, use the `crypto_status` attribute from the Account API endpoint response object.

*Sample Response*

```json
{
  "id": "9feee08f-22d2-4804-89c1-bf01166aad52",
  "account_number": "943690069",
  "status": "ACTIVE",
  "crypto_status": "ACTIVE"
}
```

| Attribute          | Description                                    |
| :----------------- | :--------------------------------------------- |
| INACTIVE           | Account not enabled to trade crypto live       |
| ACTIVE             | Crypto account is active and can start trading |
| SUBMISSION\_FAILED | Account submissions has failed                 |

# Supported Assets

We have over 20 coins available to trade via our APIs. We constantly evaluate the list and aim to to grow the number of supported currencies.

Tradable cryptocurrencies can be identified through the [Assets API](/reference/getassets) where the asset entity has `class = crypto` and `tradable = true`.

```json
{
  "id": "64bbff51-59d6-4b3c-9351-13ad85e3c752",
  "class": "crypto",
  "exchange": "CRXL",
  "symbol": "BTC/USD",
  "name": "Bitcoin",
  "status": "active",
  "tradable": true,
  "marginable": false,
  "shortable": false,
  "easy_to_borrow": false,
  "fractionable": true
}
```

Please note that the symbol appears with `USD`, such as `BTC/USD` instead of `BTC`.

> 🚧 Crypto Fee Revenue Notice
>
> If you enable non-USD crypto trading you will receive fees in the quote currency. Currently, non-USD quote crypto assets are BTC, USDC and USDT. As a broker business you would need to be ready to handle collecting crypto fees plus taking care of the necessary conversions if needed.

## Minimum Order Size

The minimum quantity value that is accepted in an order. This value is calculated dynamically based on the selected notional equivalent minimum, based on the last close price of the relevant asset(s). The maximum decimal places accepted is 9 i.e 0.000000001 for all crypto assets.

For `USD` pairs, the minimum order size calculation is: 10/USD asset price.

For `BTC`, `ETH` and `USDT` pairs, the minimum order size is `0.000000002`.

## Min Trade Increment

The minimum quantity allowed to be added to the `min_order_size`. E.g. if 0.1 we accept an order for 1.1 but we won’t accept 0.9 because it’s under the `min_order_size`. The maximum decimal places accepted are 9 i.e 0.000000001 for all crypto assets.

Price Increment: The minimum notional value that is accepted in an order. Similar to Min Order Size but for notional orders. The maximum decimal places accepted are 9 i.e 0.000000001 for all crypto assets.

All cryptocurrency assets are fractionable but the supported decimal points vary depending on the cryptocurrency.

# Supported Orders

When submitting crypto orders through the Orders API, Market, Limit and Stop Limit orders are supported while the supported `time_in_force` values are `gtc`, and `ioc`. We accept fractional orders as well with either `notional` or `qty` provided.

## Required Disclosures

Below you will find required disclosure templates to safely support crypto in your applications as a broker with Alpaca.

### Onboarding Disclosures

When onboarding your users as a broker offering crypto the following disclosure is required. During your onboarding flow make sure the user is able to read and affirmatively acknowledge, such as through a separate checkbox, the following text:

I have read, understood, and agree to be bound by Alpaca Crypto LLC and \[your legal entity] account terms, and all other terms, disclosures and disclaimers applicable to me, as referenced in the Alpaca Crypto Agreement. I also acknowledge that the Alpaca Crypto Agreement contains a pre-dispute arbitration clause in Section 26.

### Buy/Sell Order Screen Disclosures

As a broker enabling the placement of cryptocurrency orders, the following disclosures should appear on the user’s order entry screen, on the app or website, immediately prior to the user submitting the buy or sell order.

#### Buy Order Disclosure

By placing an order to buy \[$ amount of / number of ] \[cryptocurrency], you are directing and authorizing Alpaca Securities LLC to transfer funds necessary to cover the purchase costs from your Alpaca Securities LLC account into your Alpaca Crypto LLC account. Cryptocurrency services are facilitated by Alpaca Crypto LLC. Cryptocurrencies are not securities and are not FDIC insured or protected by SIPC. [Disclosures](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://files.alpaca.markets/disclosures/library/CryptoRiskDisclosures.pdf).

#### Sell Order Disclosure

By placing an order to sell \[$ amount of / number of ] \[cryptocurrency], you are directing and authorizing Alpaca Crypto LLC to transfer settled funds from the sale into your Alpaca Securities LLC account. Cryptocurrency services are facilitated by Alpaca Crypto LLC. Cryptocurrencies are not securities and are not FDIC insured or protected by SIPC. Disclosures.

#### Crypto Pairs Order Disclosure

By placing an order, you are directing and authorizing Alpaca Crypto LLC to exchange \[X amount of Cryptocurrency] for \[Y amount of cryptocurrency]. Cryptocurrency services are facilitated by Alpaca Crypto LLC. Cryptocurrencies are not securities and are not FDIC insured or protected by SIPC.

# Margin and Short Selling

Cryptocurrencies are non-marginable. This means that you cannot use leverage to buy them and orders are evaluated against `non_marginable_buying_power`.

Cryptocurrencies are not shortable.

# Trading Hours

Crypto trading is offered for 24 hours everyday and your orders will be executed throughout the day.

# Trading Limits

Currently, an order (buy or sell) must not exceed $200k in notional. This is per an order.

# Crypto Order Commissions

Brokers can charge a commission on each crypto order by including a commission parameter when submitting orders. Commission support for crypto now includes both notional and bps (basis points) commission types. The amount is specified either in the quote currency of the trading pair (for notional) or as a percentage in bps.

To enable commission support, brokers must first contact Alpaca to configure their commission structure. Once set up, the commission amount can be provided in each order request, and it will also appear in the order entity of the API response.

On all orders (regardless of commission type), the commission charged will be prorated on each execution if the order has multiple executions. For example, if 10% of the order is filled in one execution, then the commission for that execution will be 10% of the total commission.

### Commission types:

* Notional: Charges commission on a per-order basis. When the commission\_type field is omitted from the order request, this is used as the default.
* Bps: The percent commission to charge the end user on the order (expressed in basis points). Alpaca will convert the order to a notional amount for calculating the commission.

# Market Data

Alpaca provides crypto data from multiple venues.

Crypto data providers utilized by Alpaca:

| Exchange | Exchange Code          |
| :------- | :--------------------- |
| `CBSE`   | Coinbase               |
| `CRXL`   | Alpaca Crypto Exchange |
| `FLCX`   | Falcon X               |

# Features

## Price Band Protection

The price band validation in Alpaca will prevent trades from executing outside a predefined percentage range around an external reference price. Ensures market stability and prevents extreme price fluctuations due to erroneous trades. External reference prices are derived as a weighted average from `Coinbase`, `FalconX`, and `StillmanDigital`.

Orders that would execute at an invalid price will be automatically canceled with following reasons.

1. canceled due to reference price stale – Order was canceled because the reference price used for price band validation was outdated.
2. canceled due to price band protection. Index price: `<index_price>` Price band: `<price_band>`%, Rejected price: `<maker_order_price>` – Order was about to execute at a price exceeding the allowed range