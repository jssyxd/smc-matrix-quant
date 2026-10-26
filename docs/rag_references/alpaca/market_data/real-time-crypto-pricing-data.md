# Real-time Crypto Data

Source: https://docs.alpaca.markets/us/docs/real-time-crypto-pricing-data.md

---
updatedAt: 2025-11-14T05:48:34.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Real-time Crypto Data

Crypto Data API provides websocket streaming for trades, quotes, orderbooks, minute bars and daily bars. This helps receive the most up to date market information that could help your trading strategy to act upon certain market movements.

Alpaca executes your crypto orders in its own exchange, and also supports Kraken, which is another crypto exchange. Therefore, `v1beta3` crypto market data endpoint distributes data from Alpaca and Kraken.

You can find the general description of the real-time WebSocket Stream [here](https://docs.alpaca.markets/docs/streaming-market-data). This page focuses on the crypto stream.

> 👍 Advanced Websockets Tutorial
>
> Check out our tutorial [Advanced Live Websocket Crypto Data Streams in Python](https://alpaca.markets/learn/advanced-live-websocket-crypto-data-streams-in-python/) for some tips on handling live crypto data stream in Python.

# URL

The URL for the crypto stream is

```
wss://stream.data.alpaca.markets/v1beta3/crypto/{loc}
```

Sandbox URL:

```
wss://stream.data.sandbox.alpaca.markets/v1beta3/crypto/{loc}
```

Possible values `{loc}` can have are:

* us - Alpaca US
* us-1 - Kraken US
* eu-1 - Kraken EU

The location us-1 represents the states listed below:

1. AL (Alabama)
2. AK (Alaska)
3. AR (Arkansas)
4. CO (Colorado)
5. DC (District of Columbia)
6. DE (Delaware)
7. FL (Florida)
8. HI (Hawaii)
9. LA (Louisiana)
10. MN (Minnesota)
11. NV (Nevada)
12. NH (New Hampshire)
13. NJ (New Jersey)
14. NM (New Mexico)
15. OK (Oklahoma)
16. OR (Oregon)
17. PA (Pennsylvania)
18. PR (Puerto Rico)
19. TN (Tennessee)
20. TX (Texas)
21. VA (Virginia)
22. WI (Wisconsin)
23. WY (Wyoming)

Please note that, at the moment `us-1` and `eu-1` stream Kraken market data (which is another crypto exchange), but the providers may change over time.

Multiple data points may arrive in each message received from the server. These data points have the following formats, depending on their type.

# Channels

## Trades

### Schema

| Attribute | Type   | Notes                                                                                                   |
| :-------- | :----- | :------------------------------------------------------------------------------------------------------ |
| `T`       | string | message type, always “t”                                                                                |
| `S`       | string | symbol                                                                                                  |
| `p`       | number | trade price                                                                                             |
| `s`       | number | trade size                                                                                              |
| `t`       | string | [RFC-3339](https://datatracker.ietf.org/doc/html/rfc3339) formatted timestamp with nanosecond precision |
| `i`       | int    | trade ID                                                                                                |
| `tks`     | string | taker side: B for buyer, S for seller                                                                   |

### Example

```json
{
  "T": "t",
  "S": "AVAX/USD",
  "p": 47.299,
  "s": 29.205707815,
  "t": "2024-03-12T10:27:48.858228144Z",
  "i": 3447222699101865076,
  "tks": "S"
}
```

## Quotes

### Schema

| Attribute | Type   | Notes                                                                                                   |
| :-------- | :----- | :------------------------------------------------------------------------------------------------------ |
| `T`       | string | message type, always “q”                                                                                |
| `S`       | string | symbol                                                                                                  |
| `bp`      | number | bid price                                                                                               |
| `bs`      | number | bid size                                                                                                |
| `ap`      | number | ask price                                                                                               |
| `as`      | number | ask size                                                                                                |
| `t`       | string | [RFC-3339](https://datatracker.ietf.org/doc/html/rfc3339) formatted timestamp with nanosecond precision |

### Example

```json
{
  "T": "q",
  "S": "BAT/USD",
  "bp": 0.35718,
  "bs": 13445.46,
  "ap": 0.3581,
  "as": 13561.902,
  "t": "2024-03-12T10:29:43.111588173Z"
}
```

## Bars

> 📘 Crypto bars contain quote mid-prices
>
> Due to the volatility of some currencies, including lack of trade volume at any given time, we include the quote midpoint prices in the bars to offer a better data experience. If in a bar no trade happens, the volume will be 0, but the prices will be determined by the quote prices.

There are three separate channels where you can stream trade aggregates (bars).

#### Minute Bars (`bars`)

Minute bars are emitted right after each minute mark. They contain the trades and quote midpoints from the previous minute.

#### Daily Bars (`dailyBars`)

Daily bars are emitted right after each minute mark after the market opens. The daily bars contain all trades and quote midprices until the time they were emitted.

#### Updated Bars (`updatedBars`)

Updated bars are emitted after each half-minute mark if a “late” trade arrived after the previous minute mark. For example if a trade with a timestamp of `16:49:59.998` arrived right after `16:50:00`, just after `16:50:30` an updated bar with `t` set to `16:49:00` will be sent containing that trade, possibly updating the previous bar’s closing price and volume.

### Schema

| Attribute | Type   | Description                                                                   |
| :-------- | :----- | :---------------------------------------------------------------------------- |
| `T`       | string | message type: “b”, “d” or “u”                                                 |
| `S`       | string | symbol                                                                        |
| `o`       | number | open price                                                                    |
| `h`       | number | high price                                                                    |
| `l`       | number | low price                                                                     |
| `c`       | number | close price                                                                   |
| `v`       | int    | volume                                                                        |
| `t`       | string | [RFC-3339](https://datatracker.ietf.org/doc/html/rfc3339) formatted timestamp |

### Example

```json
{
  "T": "b",
  "S": "BTC/USD",
  "o": 71856.1435,
  "h": 71856.1435,
  "l": 71856.1435,
  "c": 71856.1435,
  "v": 0,
  "t": "2024-03-12T10:37:00Z",
  "n": 0,
  "vw": 0
}
```

## Orderbooks

### Schema

| Attribute | Type    | Notes                                                                                                                                                                                                        |
| :-------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `T`       | string  | message type, always “o”                                                                                                                                                                                     |
| `S`       | string  | symbol                                                                                                                                                                                                       |
| `t`       | string  | [RFC-3339](https://datatracker.ietf.org/doc/html/rfc3339) formatted timestamp with nanosecond precision                                                                                                      |
| `b`       | array   | bids: array of `p` (price) and `s` pairs. If `s` is zero, it means that that bid entry was removed from the orderbook. Otherwise it was added or updated.                                                    |
| `a`       | array   | asks: array of `p` (price) and `s` pairs. If `s` is zero, it means that that ask entry was removed from the orderbook. Otherwise it was added or updated.                                                    |
| `r`       | boolean | reset: if true, the orderbook message contains the whole server side orderbook. This indicates to the client that they should reset their orderbook. Typically sent as the first message after subscription. |

### Example

#### Initial full orderbook

```json
{
  "T": "o",
  "S": "BTC/USD",
  "t": "2024-03-12T10:38:50.79613221Z",
  "b": [
    {
      "p": 71859.53,
      "s": 0.27994
    },
    {
      "p": 71849.4,
      "s": 0.553986
    },
    {
      "p": 71820.469,
      "s": 0.83495
    },
   ...
  ],
  "a": [
    {
      "p": 71939.7,
      "s": 0.83953
    },
    {
      "p": 71940.4,
      "s": 0.28025
    },
    {
      "p": 71950.715,
      "s": 0.555928
    },
    ...
  ],
  "r": true
}
```

`r` is true, meaning that this message contains the whole BTC/USD orderbook. It's truncated here for readability, the actual book has a lot more bids & asks.

#### Update message

```json json
{
  "T": "o",
  "S": "MKR/USD",
  "t": "2024-03-12T10:39:39.445492807Z",
  "b": [],
  "a": [
    {
      "p": 2614.587,
      "s": 12.5308
    }
  ]
}
```

This means that the ask price level 2614.587 was changed to 12.5308. If there were previously no 2614.587 ask entry in the orderbook, then it should be added, if there were, its size should be updated.

#### Remove message

```json
{
  "T": "o",
  "S": "CRV/USD",
  "t": "2024-03-12T10:39:40.501160019Z",
  "b": [
    {
      "p": 0.7904,
      "s": 0
    }
  ],
  "a": []
}
```

This means that the 0.7904 bid price level should be removed from the orderbook.

# Example

```
$ wscat -c wss://stream.data.alpaca.markets/v1beta3/crypto/us
connected (press CTRL+C to quit)
< [{"T":"success","msg":"connected"}]
> {"action": "auth", "key": "**\***", "secret": "**\***"}
< [{"T":"success","msg":"authenticated"}]
> {"action": "subscribe", "bars": ["BTC/USD"]}
< [{"T":"subscription","trades":[],"quotes":[],"orderbooks":[],"bars":["BTC/USD"],"updatedBars":[],"dailyBars":[]}]
< [{"T":"b","S":"BTC/USD","o":26675.04,"h":26695.36,"l":26668.79,"c":26688.7,"v":3.227759152,"t":"2023-03-17T12:28:00Z","n":93,"vw":26679.5912436798}]
< [{"T":"b","S":"BTC/USD","o":26687.9,"h":26692.91,"l":26628.55,"c":26651.39,"v":11.568622108,"t":"2023-03-17T12:29:00Z","n":197,"vw":26651.7679765663}]
```