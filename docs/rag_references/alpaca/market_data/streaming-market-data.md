# WebSocket Stream

Source: https://docs.alpaca.markets/us/docs/streaming-market-data.md

---
updatedAt: 2026-08-27T13:45:07.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# WebSocket Stream

This API provides a [WebSocket](https://en.wikipedia.org/wiki/WebSocket) stream for real-time market data. This allows you to receive the most up-to-date market information, which can be used to power your trading strategies.

The WebSocket stream provides real-time updates of the following market data:

* [Stocks](https://docs.alpaca.markets/docs/real-time-stock-pricing-data)
* [Crypto](https://docs.alpaca.markets/docs/real-time-crypto-pricing-data)
* [Options](https://docs.alpaca.markets/docs/real-time-option-data)
* [News](https://docs.alpaca.markets/docs/streaming-real-time-news)

# Steps to use the stream

To use the WebSocket stream follow these steps:

## Connection

To establish a connection use the stream URL depending on the data you'd like to consume. The general schema of the URL is

```
wss://stream.data.alpaca.markets/{version}/{feed}
```

Sandbox URL:

```
wss://stream.data.sandbox.alpaca.markets/{version}/{feed}
```

Any attempt to access a data feed not available for your subscription will result in an error during authentication.

<Callout icon="📘" theme="info">
  ### Test stream

  We provide a test stream that is available all the time, even outside market hours, on this URL:

  ```
  wss://stream.data.alpaca.markets/v2/test
  ```

  Use the symbol "FAKEPACA" when trying out this test stream.
</Callout>

Upon successfully connecting, you will receive the welcome message:

```json
[{"T":"success","msg":"connected"}]
```

<Callout icon="🚧" theme="warn">
  ### Connection limit

  The number of connections to a single endpoint from a user is limited based on the user's subscription, but in many subscriptions (or without one) this limit is 1. If you try to open a second connection, you'll get this error:

  ```json
  [{"T":"error","code":406,"msg":"connection limit exceeded"}]
  ```
</Callout>

## Authentication

You can authenticate during the WebSocket opening handshake or by sending an authentication message after connecting.

### Authenticate with HTTP headers

You can authenticate during the WebSocket opening handshake.

#### Trading API

Use your Trading API key ID and secret key:

```shell
websocat wss://stream.data.alpaca.markets/v2/test \
  -H="APCA-API-KEY-ID: {KEY_ID}" \
  -H="APCA-API-SECRET-KEY: {SECRET_KEY}"
```

#### Broker API

The recommended Broker API authentication method is an access token obtained through the [Client Credentials](https://docs.alpaca.markets/docs/authentication#client-credentials) authentication flow:

```shell
websocat wss://stream.data.alpaca.markets/v2/test \
  -H="Authorization: Bearer {ACCESS_TOKEN}"
```

Legacy Broker API credentials can use HTTP Basic authentication:

```shell
websocat wss://stream.data.alpaca.markets/v2/test \
  -H="Authorization: Basic {BASE64_CREDENTIALS}"
```

<br /> `{BASE64_CREDENTIALS}` is the base64 encoding of `{KEY_ID}:{SECRET_KEY}` string.

#### Alpaca Connect

Applications can use the OAuth access token obtained on behalf of the user:

```shell
websocat wss://stream.data.alpaca.markets/v2/test \
  -H="Authorization: Bearer {OAUTH_ACCESS_TOKEN}"
```

### Authenticate via message

Alternatively, you can authenticate by sending a message after opening the
WebSocket connection. You must authenticate within 10 seconds.

#### Trading API

Send your Trading API key ID and secret key:

```json
{"action":"auth","key":"{KEY_ID}","secret":"{SECRET_KEY}"}
```

#### Broker API

When using an AuthX access token obtained through the client credentials flow, use the literal string `access_token` as the key:

```json
{"action":"auth","key":"access_token","secret":"{ACCESS_TOKEN}"}
```

Legacy Broker API credentials can continue to send the key ID and secret key:

```json
{"action":"auth","key":"{KEY_ID}","secret":"{SECRET_KEY}"}
```

#### Alpaca Connect

For an Alpaca Connect application, use the literal string `oauth` as the key and the user's OAuth access token as the secret:

```json
{"action":"auth","key":"oauth","secret":"{OAUTH_ACCESS_TOKEN}"}
```

### Authentication response

After successful authentication, the server responds:

```json
[{"T":"success","msg":"authenticated"}]
```

Keep in mind that most users can have only 1 active stream connection. If that connection is used by another 3rd party application, you will receive an error: 406 and “connection limit exceeded” message. Similarly, if the user wants to access their stream from an API or another 3rd party application, they will also receive the same error message.

## Subscription

Congratulations, you are ready to receive real-time market data!

You can send one or more subscription messages. The general format of the subscribe message is this:

```json
{
  "action": "subscribe",
  "<channel1>": ["<SYMBOL1>"],
  "<channel2>": ["<SYMBOL2>","<SYMBOL3>"],
  "<channel3>": ["*"]
}
```

You can subscribe to a particular symbol or to every symbol using the `*` wildcard. A subscribe message should contain what subscription you want to add to your current subscriptions in your session so you don’t have to send what you’re already subscribed to.

For example in the test stream, you can send this message:

```json
{"action":"subscribe","trades":["FAKEPACA"]}
```

The available channels are described for each streaming endpoints separately.

Much like subscribe you can also send an unsubscribe message that subtracts the list of subscriptions specified from your current set of subscriptions.

```json
{"action":"unsubscribe","quotes":["FAKEPACA"]}
```

After subscribing or unsubscribing you will receive a message that describes your current list of subscriptions.

```json
[{"T":"subscription","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":["*"],"updatedBars":[],"dailyBars":["VOO"],"statuses":["*"],"lulds":[],"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
```

You will always receive your entire list of subscriptions, as illustrated by the sample communication excerpt below:

```json
> {"action": "subscribe", "trades": ["AAPL"], "quotes": ["AMD", "CLDR"], "bars": ["*"]}
< [{"T":"subscription","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":["*"],"updatedBars":[],"dailyBars":[],"statuses":[],"lulds":[],"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
...
> {"action": "unsubscribe", "bars": ["*"]}
< [{"T":"subscription","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":[],"updatedBars":[],"dailyBars":[],"statuses":[],"lulds":[],"corrections":["AAPL"],"cancelErrors":["AAPL"]}]
```

# Messages

## Format

Every message you receive from the server will be in the format:

```json json
[{"T": "{message_type}", {contents}},...]
```

Control messages (i.e. where `T` is `error`, `success` or `subscription`) always arrive in arrays of size one to make their processing easier.

Data points however may arrive in arrays that have a length that is greater than one. This is to facilitate clients whose connection is not fast enough to handle data points sent one by one. Our server buffers the outgoing messages but slow clients may get disconnected if their buffer becomes full.

## Content type

You can use the `Content-Type` header to switch between text and binary message [data frame](https://datatracker.ietf.org/doc/html/rfc6455#section-5.6):

* `Content-Type: application/json`
* `Content-Type: application/msgpack`

## Encoding and Compression

Messages over the websocket are in encoded as clear text.

To reduce bandwidth requirements we have implemented compression as per [RFC-7692](https://datatracker.ietf.org/doc/html/rfc7692). [Our SDKs](https://docs.alpaca.markets/us/docs/sdks-and-tools) handle this for you so in most cases you won’t have to implement anything yourself.

## Errors

You may receive an error during your session. Below are the general errors you may run into.

| Code | Message                                | Description                                                                                                                                                                                                                                                          |
| :--- | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400  | invalid syntax                         | The message you sent to the server did not follow the specification.<br />:warning: This can also be sent if the symbol in your subscription message is in invalid format.                                                                                           |
| 401  | not authenticated                      | You have attempted to subscribe or unsubscribe before [authentication](https://docs.alpaca.markets/docs/streaming-market-data#authentication).                                                                                                                       |
| 402  | auth failed                            | You have provided invalid authentication credentials.                                                                                                                                                                                                                |
| 403  | already authenticated                  | You have already successfully authenticated during your current session.                                                                                                                                                                                             |
| 404  | auth timeout                           | You failed to successfully authenticate after connecting. You only have a few seconds to authenticate after connecting.                                                                                                                                              |
| 405  | symbol limit exceeded                  | The symbol subscription request you sent would put you over the limit set by your subscription package. If this happens your symbol subscriptions are the same as they were before you sent the request that failed.                                                 |
| 406  | connection limit exceeded              | You already have the number of sessions allowed by your subscription.                                                                                                                                                                                                |
| 407  | slow client                            | You may receive this if you are too slow to process the messages sent by the server. Please note that this is not guaranteed to arrive before you are disconnected to avoid keeping slow connections active forever.                                                 |
| 409  | insufficient subscription              | You have attempted to access a data source not available in your subscription package.                                                                                                                                                                               |
| 410  | invalid subscribe action for this feed | You tried to subscribe to channels not available in the stream, for example to `bars` in the [option stream](https://docs.alpaca.markets/docs/real-time-option-data) or to `trades` in the [news stream](https://docs.alpaca.markets/docs/streaming-real-time-news). |
| 500  | internal error                         | An unexpected error occurred on our end. Please let us know if this happens.                                                                                                                                                                                         |

Beside these there can be some endpoint specific errors, for example in the [option stream](https://docs.alpaca.markets/docs/real-time-option-data#errors).

# Example

Here's a complete example of the test stream using the [wscat](https://github.com/websockets/wscat) cli tool:

```json
$ wscat -c wss://stream.data.alpaca.markets/v2/test
Connected (press CTRL+C to quit)
< [{"T":"success","msg":"connected"}]
> {"action":"auth","key":"<YOUR API KEY>","secret":"<YOUR API SECRET>"}
< [{"T":"success","msg":"authenticated"}]
> {"action":"subscribe","bars":["FAKEPACA"],"quotes":["FAKEPACA"]}
< [{"T":"subscription","trades":[],"quotes":["FAKEPACA"],"bars":["FAKEPACA"]}]
< [{"T":"q","S":"FAKEPACA","bx":"O","bp":133.85,"bs":4,"ax":"R","ap":135.77,"as":5,"c":["R"],"z":"A","t":"2024-07-24T07:56:53.639713735Z"}]
< [{"T":"q","S":"FAKEPACA","bx":"O","bp":133.85,"bs":4,"ax":"R","ap":135.77,"as":5,"c":["R"],"z":"A","t":"2024-07-24T07:56:58.641207127Z"}]
< [{"T":"b","S":"FAKEPACA","o":132.65,"h":136,"l":132.12,"c":134.65,"v":205,"t":"2024-07-24T07:56:00Z","n":16,"vw":133.7}]
```