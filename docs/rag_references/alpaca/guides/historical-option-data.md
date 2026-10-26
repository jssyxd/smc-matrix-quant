# Historical Option Data

Source: https://docs.alpaca.markets/us/docs/historical-option-data.md

---
updatedAt: 2025-09-24T23:32:21.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical Option Data

This API provides historical market data for options. Check the [API Reference](https://docs.alpaca.markets/reference/optionbars) for the detailed descriptions of all the endpoints.

> 🚧 Data availability
>
> Currently we only offer historical option data since February 2024.

# Data sources

Similarly to stocks, Alpaca offers two different data sources for options:

| Source                                       | Description                                                                                                                                                                                                                                                                                               |
| :------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Indicative**                               | Indicative Pricing Feed is a free derivative of the original OPRA feed: the quotes are not actual OPRA quotes, they’re just indicative derivatives. The trades are also derivatives and they’re delayed by 15 minutes.                                                                                    |
| **OPRA (Options Price Reporting Authority)** | OPRA is the consolidated BBO feed of OPRA. [OPRA Plan](https://www.opraplan.com/document-library) defines the BBO as the highest bid and lowest offer for a series of options available in one or more of the options markets maintained by the parties. OPRA feed is only available to subscribed users. |