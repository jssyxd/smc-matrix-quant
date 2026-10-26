# About Connect API

Source: https://docs.alpaca.markets/us/docs/about-connect-api.md

---
updatedAt: 2026-04-24T17:44:05.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# About Connect API

Develop applications on Alpaca’s platform using OAuth2. Let 10M+ users with an Alpaca brokerage account connect to your app.

Alpaca’s OAuth allows you to seamlessly integrate financial markets into your application and expand your audience to millions of brokerage accounts on Alpaca’s platform

Read Register Your App to learn how you can register your app. In addition, you can visit OAuth Integration Guide to learn more about using OAuth to connect your applications with Alpaca.

# Broker Partners

Broker partners are able to create their own OAuth service. Allow your end users to use OAuth apps like TradingView through your Broker API application. Learn more about OAuth with Broker API in the [Broker API reference](https://docs.alpaca.markets/docs/about-broker-api)

<br />

# Non-Registered and Fintech Partners

Alpaca Connect allows non-registered firms, developers and fintech companies to build trading apps on Alpaca’s platform. Using OAuth, your application can connect to Alpaca brokerage accounts . Apps ranging from algorithmic trading and charting to crypto and more are  published on the Alpaca Connect Marketplace once they are approved by Alpaca Compliance.

<br />

# Terms of Access and Use

* You must read the terms and register in order to connect and use Alpaca’s APIs
* All API clients must authenticate with OAuth 2.0
* You may not imply that the app was developed by Alpaca.
* If you are building a commercial application that makes money (including ads, in-app purchases, etc), you must disclose it in the registration form and receive written approval.
* To allow live trading for other users, the app needs to be approved by Alpaca. Please create your application via the Alpaca Dashboard under the [Alpaca Connect](https://app.alpaca.markets/connect) tab. For further details, please review [Registering Your App](https://docs.alpaca.markets/update/docs/registering-your-app)
* For any additional questions, please reach out to <Support@alpaca.markets>

<br />

> ❗️ This is not an offer, solicitation of an offer, or advice to open a brokerage account.
>
> Disclosure can be found [here](https://alpaca.markets/#disclosures)

# FAQs

### Q: What can an OAuth app do?

A: OAuth allows you to manage your end-user’s Alpaca brokerage account on their behalf. This means you can create many types of financial services including automated investing, portfolio analytics and much more.

### Q: Should I use OAuth or Broker API?

A: OAuth allows you to expand your audience to users with Alpaca brokerage accounts. On the other hand, Broker API allows you to build an application fully within your environment. Users sign up for a brokerage account under your application. If you want to create your own brokerage, automated investment app, or any app where you want to own your users, use the Broker API. If you want to build your trading service on Alpaca’s platform, use OAuth.

### Q: How secure is OAuth?

A: OAuth2 itself is very secure. However you must make sure to follow good practices in how you handle tokens. Make sure to never publicly expose your client secret and access tokens.

### Q: How to get OAuth App live?

A: You will need to register your app in the OAuth apps section of the dashboard. Learn more about [Registering Your App](https://docs.alpaca.markets/update/docs/registering-your-app)

### Q: I’m developing an app/service targeting non-US users. Can we integrate with Alpaca’s OAuth API?

A: Alpaca’s platform supports brokerage accounts for international users. When you build an app on OAuth, all users on Alpaca’s platform will be able to use your service, including international users.

<br />