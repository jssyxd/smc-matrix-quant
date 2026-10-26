# Historical News Data

Source: https://docs.alpaca.markets/us/docs/historical-news-data.md

---
updatedAt: 2025-09-24T23:32:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Historical News Data

This API provides historical news data dating back to 2015. You can expect to receive an average of 130+ news articles per day. All news data is currently provided directly by [Benzinga](https://www.benzinga.com/). With a single endpoint, you can request news for both stocks and cryptocurrency tickers. Check the [API Reference](https://docs.alpaca.markets/reference/news-3) for the detailed descriptions the endpoint.

# Use Cases

News API is a versatile tool that can be used to support a variety of use cases, such as building an app with the Broker API or Algorithmic Trading using Sentiment Analysis on News with the Trading API.

1. **News Widgets**

   News API can be used to create visual news widgets for web and mobile apps. These widgets can be used to display the latest news for any stock or crypto symbol, and they include different sized images to give your app a visual appeal.
2. **News Sentiment Analysis**\
   News API can be used to train models that can determine the sentiment of a given headline or news content. This can be done by using historical data from News API to train the model on a variety of different sentiment labels.
3. **Realtime Trading on News**\
   [Real-time news over WebSockets](https://docs.alpaca.markets/edit/streaming-real-time-news) can be used to enable your trading algorithms to react to the latest news across any stock or cryptocurrency.