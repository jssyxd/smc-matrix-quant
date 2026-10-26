# Historical API

Source: https://docs.alpaca.markets/us/docs/historical-api.md

---
updatedAt: 2025-09-24T23:32:19.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical API

This RESTful API provides historical market data through the HTTP protocol. This allows you to query historical market information, which can be used for charting, backtesting and to power your trading strategies.

Historical market data is available for the following types:

* [Stocks](https://docs.alpaca.markets/docs/historical-stock-data-1)
* [Crypto](https://docs.alpaca.markets/docs/historical-crypto-data-1)
* [Options](https://docs.alpaca.markets/docs/historical-option-data)
* [News](https://docs.alpaca.markets/docs/historical-news-data)

# Base URL

The Base URL for the historical endpoints is

```
https://data.alpaca.markets/{version}
```

Sandbox URL (for broker partners):

```
https://data.sandbox.alpaca.markets/{version}
```