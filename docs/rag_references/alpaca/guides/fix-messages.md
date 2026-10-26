# FIX Specification

Source: https://docs.alpaca.markets/us/docs/fix-messages.md

---
updatedAt: 2026-07-30T05:01:09.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# FIX Specification

This document describes the implementation of the FIX 4.2 protocol used by Alpaca to enable order entry via FIX.

Version 1.2.0

## Supported Message Types

| Message                                                                           | MsgType | Description                                                                       |
| --------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------- |
| [Logon](#logon-a)                                                                 | A       | Sent by FIX client to authenticate and establish the FIX session                  |
| [Heartbeat](#heartbeat-0)                                                         | 0       | Sent by either client or server at preset interval within the working FIX session |
| [Test Request](#test-request-1)                                                   | 1       | Sent to force a heartbeat from the opposing application                           |
| [Resend Request](#resend-request-2)                                               | 2       | To request retransmission of messages which were missed                           |
| [Reject](#reject-3)                                                               | 3       | Response to a message that could not be processed                                 |
| [Sequence Reset](#sequence-reset-4)                                               | 4       | To reset the FIX session sequence number                                          |
| [Logout](#logout-5)                                                               | 5       | To safely disconnect the connected FIX session                                    |
| [New Order - Single](#new-order---single-d)                                       | D       | To submit a new single order (equity or single-leg option)                        |
| [New Order - Multileg](#new-order---multileg-ab)                                  | AB      | To submit a new multi-leg order (e.g. option spreads, covered calls)              |
| [Execution Report](#execution-report-8)                                           | 8       | Sent whenever the state of the order changes                                      |
| [Order Cancel Request](#order-cancel-request-f)                                   | F       | To request cancellation of an order (single-leg or multileg)                      |
| [Order Cancel/Replace Request](#order-cancelreplace-request-g)                    | G       | To request modification of a single-leg order                                     |
| [Multileg Order Cancel/Replace Request](#multileg-order-cancelreplace-request-ac) | AC      | To request modification of a multi-leg order                                      |
| [Order Cancel Reject](#order-cancel-reject-9)                                     | 9       | Sent if a cancel or cancel/replace request (F, G, or AC) could not be executed    |

## Message Header

All messages should contain the following tags in the header:

| Tag | Field        | Mandatory | Description                                                                                                                        |
| --- | ------------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 8   | BeginString  | Y         | FIX.4.2                                                                                                                            |
| 9   | BodyLength   | Y         | Size of the message body in bytes                                                                                                  |
| 34  | MsgSeqNum    | Y         | Message sequence number                                                                                                            |
| 35  | MsgType      | Y         | Message type, should be one of the types supported in this doc                                                                     |
| 49  | SenderCompID | Y         | Provided by Alpaca, must be present in all FIX messages. This will be returned as TargetCompID (56) in all FIX messages to clients |
| 52  | SendingTime  | Y         | UTC timestamp of message transmission. Precision supported: Millis, Micros, Nanos                                                  |
| 56  | TargetCompID | Y         | Provided by Alpaca, must be present in all FIX messages. This will be returned as SenderCompID (49) in all FIX messages to clients |

## Message Trailer

All messages should contain the following tags in the trailer:

| Tag | Field    | Mandatory | Description                                                                                            |
| --- | -------- | --------- | ------------------------------------------------------------------------------------------------------ |
| 10  | CheckSum | Y         | Last field in the messages with trailing `<SOH>`. Value calculated by the FIX engine from message data |

## Logon (A)

| Tag | Field           | Mandatory | Description                                            |
| :-- | :-------------- | :-------- | :----------------------------------------------------- |
| 35  | MsgType         | Y         | A - For Logon                                          |
| 98  | EncryptMethod   | Y         | 0 - None, only accepted value                          |
| 108 | HeartBtInt      | Y         | Must be set to `30` for 30 seconds                     |
| 141 | ResetSeqNumFlag | N         | Y - Resets both sender and target sequence number to 1 |

**Example FIX Message**

```text Logon (A)
|8=FIX.4.2|9=73|35=A|34=1|49=SENDER|52=20240524-16:02:42.003|56=ALPACA|98=0|108=30|141=Y|10=131|
```

## Heartbeat (0)

Sent by either client or server if no message has been received since the last heartbeat interval. This is also sent in response to a Test Request (1).

| Tag | Field     | Mandatory | Description                                                            |
| --- | --------- | --------- | ---------------------------------------------------------------------- |
| 35  | MsgType   | Y         | 0 - For Heartbeat                                                      |
| 112 | TestReqID | N         | Required only when Heartbeat is sent in response to a Test Request (1) |

**Example FIX Message**

```text Heartbeat
|8=FIX.4.2|9=91|35=0|49=SENDER|56=ALPACA|34=2|52=20230330-16:52:321.029|10=049|
```

## Test Request (1)

May be sent by either client or server, to force a Heartbeat (0) from the other party.

| Tag | Field     | Mandatory | Description                                              |
| --- | --------- | --------- | -------------------------------------------------------- |
| 35  | MsgType   | Y         | 1 - For Test Request                                     |
| 112 | TestReqID | Y         | Identifier to be returned in the resulting Heartbeat (0) |

**Example FIX Message**

```text Test Request
|8=FIX.4.2|9=91|35=1|49=SENDER|56=ALPACA|34=2|52=20230330-16:52:321.029|112=TEST|10=049|
```

## Resend Request (2)

Sent to request retransmission of messages which were missed.

| Tag | Field      | Mandatory | Description                                     |
| --- | ---------- | --------- | ----------------------------------------------- |
| 35  | MsgType    | Y         | 2 - For Resend Request                          |
| 7   | BeginSeqNo | Y         | Beginning sequence number of requested messages |
| 16  | EndSeqNo   | Y         | Ending sequence number of requested messages    |

**Example FIX Message**

```text Resend Request
|8=FIX.4.2|9=66|7=9|16=36|34=12|35=2|49=SENDER|52=20230627-14:10:21.769|56=ALPACA|10=126|
```

## Reject (3)

Sent when a message is rejected or cannot be processed by the FIX server.

| Tag | Field               | Mandatory | Description                                                                                                                                                                                                                                                                                                                                                                                      |
| :-- | :------------------ | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType             | Y         | 3 - For Reject                                                                                                                                                                                                                                                                                                                                                                                   |
| 45  | RefSeqNum           | Y         | Sequence number of the rejected message                                                                                                                                                                                                                                                                                                                                                          |
| 58  | Text                | N         | Reason for rejection                                                                                                                                                                                                                                                                                                                                                                             |
| 371 | RefTagID            | N         | The tag number of the FIX field being referenced                                                                                                                                                                                                                                                                                                                                                 |
| 372 | RefMsgType          | N         | The MsgType (35) of the FIX message being referenced                                                                                                                                                                                                                                                                                                                                             |
| 373 | SessionRejectReason | N         | Reject reason codes.<br />0 - Invalid tag number<br />1 - Required tag missing<br />2 - Tag not defined for this message type<br />3 - Unsupported Message Type<br />4 - Tag specified without a value<br />5 - Value is incorrect (out of range) for this tag<br />6 - Incorrect data format for value<br />9 - CompID problem<br />10 - SendingTime accuracy problem<br />11 - Invalid MsgType |

**Example FIX Message**

```text Reject
|8=FIX.4.2|9=0134|35=3|34=44196|49=ALPACA|56=TARGET|52=20230330-20:18:38.039|58=0005 Tag specified without a value|45=44196|371=11|372=8|373=4|10=092|
```

## Sequence Reset (4)

Sent to reset the incoming sequence number on the other side. The sequence reset should be used only to increase the sequence number. Any request to decrease the sequence number will result in a Reject (3) message.

| Tag | Field       | Mandatory | Description                                                                                                                                            |
| :-- | :---------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType     | Y         | 4 - For Sequence Reset                                                                                                                                 |
| 36  | NewSeqNo    | Y         | New sequence number                                                                                                                                    |
| 123 | GapFillFlag | N         | N - Sequence reset to recover from an out-of-sequence condition, MsgSeqNum(34) is ignored<br />Y - Gap fill message, MsgSeqNum(34) field must be valid |

**Example FIX Message**

```text Sequence Reset
|8=FIX.4.2|9=61|34=12|35=4|36=9|49=SENDER|52=20230627-14:14:51.732|56=ALPACA|10=156|
```

## Logout (5)

May be sent by either client or server, to terminate the session. The other party would respond with a confirming Logout  message as an acknowledgement.

| Tag | Field   | Mandatory | Description    |
| --- | ------- | --------- | -------------- |
| 35  | MsgType | Y         | 5 - For Logout |

**Example FIX Message**

```text Logout
|8=FIX.4.2|9=56|34=12|35=5|49=SENDER|52=20230627-14:16:50.690|56=ALPACA|10=197|
```

## New Order - Single (D)

Sent by the client to submit a new single order.

| Tag | Field             | Mandatory | Description                                                                                                                                                                                                                                                                                                |
| :-- | :---------------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType           | Y         | D - For New Order - Single                                                                                                                                                                                                                                                                                 |
| 1   | Account           | Y         | Account number                                                                                                                                                                                                                                                                                             |
| 11  | ClOrdID           | Y         | Unique identifier of the order assigned by the client (must be no longer than 48 characters)                                                                                                                                                                                                               |
| 12  | Commission        | N         | Commission to collect from the account holder                                                                                                                                                                                                                                                              |
| 13  | CommType          | N         | 1 - per share<br />2 - percentage, 5% should be represented as .05<br />3 - absolute                                                                                                                                                                                                                       |
| 18  | ExecInst          | N         | 1 - Not held<br />5 - Held                                                                                                                                                                                                                                                                                 |
| 21  | HandlInst         | Y         | 1 - Automated execution with no broker intervention, only accepted value                                                                                                                                                                                                                                   |
| 38  | OrderQty          | N         | Number of shares to trade, required if CashOrderQty (152) is not set                                                                                                                                                                                                                                       |
| 40  | OrdType           | Y         | 1 - Market<br />2 - Limit<br />3 - Stop<br />4 - Stop limit<br />5 - Market on close<br />B - Limit on close                                                                                                                                                                                               |
| 44  | Price             | N         | Required for Limit `40=2` and Stop Limit `40=4` orders                                                                                                                                                                                                                                                     |
| 54  | Side              | Y         | 1 - Buy<br />2 - Sell                                                                                                                                                                                                                                                                                      |
| 55  | Symbol            | Y         | Ticker symbol                                                                                                                                                                                                                                                                                              |
| 59  | TimeInForce       | Y         | 0 - Day (day)<br />1 - Good Till Cancel (gtc)<br />2 - At the Opening (opg)<br />3 - Immediate or Cancel (ioc)<br />4 - Fill or Kill (fok)<br />7 - At the Close (cls)                                                                                                                                     |
| 168 | EffectiveTime     | N         | UTC timestamp at which the order becomes eligible for execution. If omitted, the order is effective immediately. A future EffectiveTime does not guarantee immediate routing or execution; applicable trading-session rules and all other order validations continue to apply. Precision supported: Second |
| 60  | TransactTime      | Y         | UTC timestamp of order creation by client                                                                                                                                                                                                                                                                  |
| 77  | OpenClose         | N         | Indicates whether the resulting position from the trade would be an opening or closing position.<br />O - Open<br />C - Close                                                                                                                                                                              |
| 99  | StopPx            | N         | Required for Stop `40=3` and Stop Limit `40=4` orders                                                                                                                                                                                                                                                      |
| 109 | ClientID          | N         | Sub-account tag for omnibus accounts                                                                                                                                                                                                                                                                       |
| 152 | CashOrderQty      | N         | Notional value to trade, required if OrderQty (38) is not set                                                                                                                                                                                                                                              |
| 336 | TradingSessionID  | N         | 8 - Extended Hours<br />Required for extended hours orders only                                                                                                                                                                                                                                            |
| 167 | SecurityType      | N         | CS - Common Stock (default when absent)<br />OPT - Option<br />Required to be `OPT` to submit a single-leg option order                                                                                                                                                                                    |
| 200 | MaturityMonthYear | N         | Expiration month and year in `YYYYMM` format.<br />Required when `167=OPT`                                                                                                                                                                                                                                 |
| 201 | PutOrCall         | N         | 0 - Put<br />1 - Call<br />Required when `167=OPT`                                                                                                                                                                                                                                                         |
| 202 | StrikePrice       | N         | Strike price of the option contract (up to 3 decimal places).<br />Required when `167=OPT`                                                                                                                                                                                                                 |
| 205 | MaturityDay       | N         | Expiration day of month (1-31).<br />Required when `167=OPT`                                                                                                                                                                                                                                               |

**Notes on effective-time orders**

* Please contact to your Alpaca technical representative to enable this feature.
* EffectiveTime supports day limit/stop\_limit orders including extended\_hours
* The order cannot be filled before EffectiveTime.
* stop\_limit orders are not evaluated for stop triggering before EffectiveTime.
* The order may be canceled before EffectiveTime.
* If EffectiveTime falls outside a trading session for which the order is eligible, the order is held until the next eligible session.
* Reaching EffectiveTime does not guarantee execution. Price, liquidity, trading-session eligibility, and other validation still apply.
* EffectiveTime must be expressed in UTC using FIX UTCTimestamp format. Precision supported: Second
* An order may have OrderStatus(39) = New and ExecType (150) = New before its EffectiveTime. In this case, New means that Alpaca has accepted the order; it does not mean the order is currently eligible for execution.

**Notes on single-leg option orders**

* When `SecurityType (167) = OPT`, the option contract is identified by the combination of `Symbol (55)` (underlying root, e.g. `AAPL`), `MaturityMonthYear (200)`, `MaturityDay (205)`, `PutOrCall (201)` and `StrikePrice (202)`.
* `OpenClose (77)` should be supplied to disambiguate the position effect (open vs. close). When omitted, position intent is inferred from `Side (54)`: `Buy` → buy-to-open, `Sell` → sell-to-close, `Sell Short (5)` → sell-to-open.
* Option execution reports echo back `SecurityType`, `MaturityMonthYear`, `MaturityDay`, `PutOrCall` and `StrikePrice` along with the standard fields.

**Example FIX Messages**

```text Market order (quantity based)
|8=FIX.4.2|9=139|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=1|49=SENDER|52=20230613-14:01:37.330|54=1|55=SPY|56=ALPACA|59=1|10=030|
```
```text Market order (notional based)
|8=FIX.4.2|9=141|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|40=1|49=SENDER|52=20230613-14:43:47.572|54=1|55=SPY|56=ALPACA|59=0|152=100|10=130|
```
```text Limit order
|8=FIX.4.2|9=149|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=2|44=350.78|49=SENDER|52=20230613-14:45:58.303|54=1|55=SPY|56=ALPACA|59=0|10=005|
```
```text Stop order
|8=FIX.4.2|9=149|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=3|49=SENDER|52=20230613-14:50:51.223|54=1|55=SPY|56=ALPACA|59=0|99=350.78|10=006|
```
```text Stop limit order
|8=FIX.4.2|9=159|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=4|44=350.78|49=SENDER|52=20230613-15:26:35.992|54=1|55=SPY|56=ALPACA|59=0|99=350.78|10=246|
```
```text Extended Hours Order
|8=FIX.4.2|9=149|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=2|44=350.78|49=SENDER|52=20230613-14:45:58.303|54=1|55=SPY|56=ALPACA|59=5|10=005|
```
```text Option order (Buy-to-Open 2 META Jan-17-2025 100 Call @ limit 2.15)
|8=FIX.4.2|9=185|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=2|40=2|44=2.15|49=SENDER|52=20240910-14:45:58.303|54=1|55=META|56=ALPACA|59=0|60=20240910-14:45:58.303|77=O|167=OPT|200=202501|201=1|202=100|205=17|10=011|
```
```text EffectiveTime order
|8=FIX.4.2|9=149|1=TEST_ACCOUNT|11=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|34=12|35=D|38=10|40=2|44=350.78|49=SENDER|52=20230613-14:45:58.303|54=1|55=SPY|56=ALPACA|59=0|168=20260727-00:00:00.000|10=005|
```

## Execution Report (8)

Sent by the server whenever an order receives an update. Each execution report contains field OrdStatus (39) which is used to convey the current status of the order as understood by Alpaca, as well as fields ExecType (150) and ExecTransType (20) which describe the purpose of the message.

| Tag | Field                 | Mandatory | Description                                                                                                                                                                                                                                                                                                                                                                        |
| :-- | :-------------------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType               | Y         | 8 - For Execution Report                                                                                                                                                                                                                                                                                                                                                           |
| 1   | Account               | Y         | Account number                                                                                                                                                                                                                                                                                                                                                                     |
| 6   | AvgPx                 | Y         | Average price of all fills on this order                                                                                                                                                                                                                                                                                                                                           |
| 11  | ClOrdID               | Y         | Unique identifier of the order as assigned by the client                                                                                                                                                                                                                                                                                                                           |
| 12  | Commission            | N         | Monetary commission value charged on a fill/partial fill                                                                                                                                                                                                                                                                                                                           |
| 14  | CumQty                | Y         | Filled quantity on the order                                                                                                                                                                                                                                                                                                                                                       |
| 15  | Currency              | N         | Account base currency, default USD                                                                                                                                                                                                                                                                                                                                                 |
| 17  | ExecID                | Y         | Unique identifier of the execution assigned by Alpaca                                                                                                                                                                                                                                                                                                                              |
| 19  | ExecRefID             | N         | ExecID (17) of the original execution being canceled or corrected when `20=1` or `20=2`                                                                                                                                                                                                                                                                                            |
| 20  | ExecTransType         | Y         | Transaction type.<br />0 - New<br />1 - Cancel<br />2 - Correct<br />3 - Status, for Restated (D) message upon stop trigger                                                                                                                                                                                                                                                        |
| 30  | LastMkt               | N         | Market of execution for this fill                                                                                                                                                                                                                                                                                                                                                  |
| 31  | LastPx                | N         | Price of this fill                                                                                                                                                                                                                                                                                                                                                                 |
| 32  | LastShares            | N         | Quantity traded on this fill                                                                                                                                                                                                                                                                                                                                                       |
| 37  | OrderID               | Y         | Unique identifier of the order assigned by Alpaca                                                                                                                                                                                                                                                                                                                                  |
| 38  | OrderQty              | N         | Either CashOrderQty (152) or OrderQty (38) is provided                                                                                                                                                                                                                                                                                                                             |
| 39  | OrdStatus             | Y         | Identifies current status of order.<br />0 - New<br />1 - Partially filled<br />2 - Filled<br />3 - Done for day<br />4 - Canceled<br />5 - Replaced<br />6 - Pending Cancel<br />8 - Rejected<br />A - Pending New<br />C - Expired<br />E - Pending Replace                                                                                                                      |
| 40  | OrdType               | N         | Same as specified on the order.<br />1 - Market<br />2 - Limit<br />3 - Stop<br />4 - Stop limit<br />5 - Market on close<br />B - Limit on close                                                                                                                                                                                                                                  |
| 41  | OrigClOrdID           | N         | ClOrdID (11) of the original order in cancel and cancel/replace requests                                                                                                                                                                                                                                                                                                           |
| 44  | Price                 | N         | Sent when specified on the order                                                                                                                                                                                                                                                                                                                                                   |
| 54  | Side                  | Y         | 1 - Buy<br />2 - Sell                                                                                                                                                                                                                                                                                                                                                              |
| 55  | Symbol                | Y         | Ticker symbol                                                                                                                                                                                                                                                                                                                                                                      |
| 58  | Text                  | N         | Contains reject reason when `150=8`                                                                                                                                                                                                                                                                                                                                                |
| 59  | TimeInForce           | N         | Same as specified on the order.<br />0 - Day (day)<br />1 - Good Till Cancel (gtc)<br />2 - At the Opening (opg)<br />3 - Immediate or Cancel (ioc)<br />4 - Fill or Kill (fok)<br />7 - At the Close (cls)                                                                                                                                                                        |
| 168 | EffectiveTime         | N         | Effective time associated with the order. Populated when EffectiveTime (168) was supplied on the original order.                                                                                                                                                                                                                                                                   |
| 60  | TransactTime          | N         | Server time in UTC when execution occurred, nanoseconds precision                                                                                                                                                                                                                                                                                                                  |
| 99  | StopPx                | N         | Sent when specified on the order                                                                                                                                                                                                                                                                                                                                                   |
| 150 | ExecType              | Y         | Describes the type of execution report.<br />0 - New<br />1 - Partial fill<br />2 - Fill<br />3 - Done for day<br />4 - Canceled<br />5 - Replaced<br />6 - Pending Cancel, ack for Order Cancel Request (F)<br />8 - Rejected<br />A - Pending New<br />C - Expired<br />D - Restated, for stop price triggers<br />E - Pending Replace, ack for Order Cancel/Replace Request (G) |
| 151 | LeavesQty             | Y         | Unfilled quantity on the order. When order is closed (filled, done for day, canceled, replaced, rejected, expired) value could be 0                                                                                                                                                                                                                                                |
| 152 | CashOrderQty          | N         | Either CashOrderQty (152) or OrderQty (38) is provided. Specifies the notional amount conveyed on the order                                                                                                                                                                                                                                                                        |
| 378 | ExecRestatementReason | N         | Populated when ExecType (150) = Restated (D).<br />100 - Stop triggered, for stop and stop limit orders                                                                                                                                                                                                                                                                            |
| 77  | OpenClose             | N         | Position effect of the execution.<br />O - Open<br />C - Close<br />Always populated on leg execution reports for multileg orders                                                                                                                                                                                                                                                  |
| 167 | SecurityType          | N         | CS - Common Stock<br />OPT - Option<br />MLEG - Multileg Instrument (parent execution reports of multileg orders)                                                                                                                                                                                                                                                                  |
| 200 | MaturityMonthYear     | N         | Populated for option executions (`167=OPT`)                                                                                                                                                                                                                                                                                                                                        |
| 201 | PutOrCall             | N         | Populated for option executions (`167=OPT`).<br />0 - Put<br />1 - Call                                                                                                                                                                                                                                                                                                            |
| 202 | StrikePrice           | N         | Populated for option executions (`167=OPT`)                                                                                                                                                                                                                                                                                                                                        |
| 205 | MaturityDay           | N         | Populated for option executions (`167=OPT`)                                                                                                                                                                                                                                                                                                                                        |
| 442 | MultiLegReportingType | N         | Set only on executions emitted from multileg parent orders.<br />2 - Individual leg of a multi-leg security (one execution report per leg)<br />3 - Multi-leg security (parent-level execution report)                                                                                                                                                                             |
| 654 | LegRefID              | N         | Identifier of the leg this execution report corresponds to.<br />Populated on leg execution reports (`442=2`); matches the LegRefID supplied on the parent order                                                                                                                                                                                                                   |
| 555 | NoLegs                | N         | Number of legs in the NoLegs repeating group.<br />Populated on parent execution reports (`442=3`). See [New Order - Multileg (AB)](#new-order---multileg-ab) for repeating group fields                                                                                                                                                                                           |

**Notes on execution reports for multileg orders**

Each state transition for a multileg parent order produces:

* One execution report per leg with `MultiLegReportingType (442) = 2` (Individual leg). Leg execution reports carry the leg's `LegRefID (654)`, `Side (54)`, `OrderQty (38) = parent_qty * LegRatioQty`, option tags (when the leg is an option) and `OpenClose (77)` for the leg's position effect.
* Optionally, one parent-level execution report with `MultiLegReportingType (442) = 3` and `SecurityType (167) = MLEG`. Parent execution reports include the `NoLegs (555)` repeating group describing all legs and use the parent's `ClOrdID (11)` and `OrderID (37)`. Whether parent-level execution reports are sent is agreed at session onboarding.

For fills, leg-level `LastPx (31)` and `LastShares (32)` reflect the per-leg execution, while the parent execution report's `LastPx (31)` reflects the net spread price (sum of buy-leg prices minus sum of sell-leg prices, scaled by leg ratios) and `LastShares (32)` reflects the number of completed spread units.

**Example FIX Messages**

```text Pending New
|8=FIX.4.2|9=216|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=A|40=1|49=ALPACA|52=20230615-18:14:29.702|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:14:29.702|150=A|151=10|10=088|
```
```text New
|8=FIX.4.2|9=216|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=0|40=1|49=ALPACA|52=20230615-18:14:45.263|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:14:45.263|150=0|151=10|10=054|
```
```text Partial Fill
|8=FIX.4.2|9=251|1=TEST_ACCOUNT|6=350.78|14=5|15=USD|17=694bc450-3ca6-461e-8566-f977dcec9e2d|31=350.78|32=5|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=1|40=1|49=ALPACA|52=20230615-18:15:00.622|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:15:00.622|150=1|151=5|10=185|
```
```text Fill
|8=FIX.4.2|9=253|1=TEST_ACCOUNT|6=350.78|14=10|15=USD|17=694bc450-3ca6-461e-8566-f977dcec9e2d|31=350.78|32=10|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=2|40=1|49=ALPACA|52=20230615-18:15:21.920|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:15:21.920|150=2|151=0|10=024|
```
```text Pending Replace
|8=FIX.4.2|9=216|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=E|40=1|49=ALPACA|52=20230615-18:26:53.971|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:26:53.971|150=E|151=10|10=112|
```
```text Replaced
|8=FIX.4.2|9=256|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=5|40=1|41=56fcd203-7a97-430d-b14c-b0d9a7f59f2f|49=ALPACA|52=20230615-18:15:38.108|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:15:38.108|150=5|151=10|10=144|
```
```text Pending Cancel
|8=FIX.4.2|9=216|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=6|40=1|49=ALPACA|52=20230615-18:24:50.191|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:24:50.191|150=6|151=10|10=060|
```
```text Canceled
|8=FIX.4.2|9=216|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=4|40=1|49=ALPACA|52=20230615-18:17:45.813|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:17:45.813|150=4|151=10|10=070|
```
```text Rejected
|8=FIX.4.2|9=227|1=TEST_ACCOUNT|17=694bc450-3ca6-461e-8566-f977dcec9e2d|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=8|40=1|49=ALPACA|52=20230615-18:15:51.825|54=1|55=SPY|56=SENDER|59=0|60=20230615-18:15:51.825|103=Price too low|150=8|10=191|
```
```text Option Fill (META Jan-17-2025 100 Call)
|8=FIX.4.2|9=296|1=TEST_ACCOUNT|6=2.15|14=2|15=USD|17=694bc450-3ca6-461e-8566-f977dcec9e2d|31=2.15|32=2|34=12|35=8|37=c5bfc5f6-163d-450e-bb4a-fb25188cde8e|39=2|40=2|44=2.15|49=ALPACA|52=20240910-14:46:01.220|54=1|55=META|56=SENDER|59=0|60=20240910-14:46:01.220|77=O|150=2|151=0|167=OPT|200=202501|201=1|202=100|205=17|10=189|
```
```text Multileg Leg Execution Report (call leg, partial fill)
|8=FIX.4.2|9=320|1=TEST_ACCOUNT|6=79.25|11=PARENT_CLORDID|14=1|15=USD|17=4d6a8e2d-b86a-4ab9-9d3b-3a4dc6f5fa1c|31=79.25|32=1|34=18|35=8|37=ORDER_ID|39=1|40=2|44=10.5|49=ALPACA|52=20240910-15:00:00.001|54=1|55=AAPL|56=SENDER|59=0|60=20240910-15:00:00.001|77=O|150=1|151=1|167=OPT|200=202501|201=1|202=100|205=17|442=2|654=0|10=180|
```
```text Multileg Parent Execution Report (filled spread)
|8=FIX.4.2|9=412|1=TEST_ACCOUNT|6=77.75|11=PARENT_CLORDID|14=2|15=USD|17=2bbf38f6-89f1-4f25-bb70-9f1e3ad7c1aa|31=77.75|32=2|34=22|35=8|37=ORDER_ID|39=2|40=2|44=10.5|49=ALPACA|52=20240910-15:00:05.500|56=SENDER|59=0|60=20240910-15:00:05.500|150=2|151=0|167=MLEG|442=3|555=2|600=AAPL|608=OC|611=20250117|612=100|624=1|623=1|564=O|654=0|600=AAPL|608=OP|611=20250117|612=100|624=2|623=1|564=O|654=1|10=224|
```

## Order Cancel Request (F)

Sent by the client to request cancellation of an order. The same message type is used to cancel both single-leg (equity/option) and multi-leg orders. For multileg orders, `SecurityType (167)` should be set to `MLEG` and `Symbol (55)` should be the underlying root symbol of the parent order.

| Tag | Field        | Mandatory | Description                                                                    |
| --- | ------------ | --------- | ------------------------------------------------------------------------------ |
| 35  | MsgType      | Y         | F - For Order Cancel Request                                                   |
| 1   | Account      | Y         | Account number                                                                 |
| 11  | ClOrdID      | Y         | Unique identifier of cancel request assigned by the client                     |
| 41  | OrigClOrdID  | Y         | ClOrdID (11) of the order to be canceled as assigned by the client             |
| 54  | Side         | Y         | As specified on the order to be canceled                                       |
| 55  | Symbol       | Y         | As specified on the order to be canceled (underlying root symbol for multileg) |
| 60  | TransactTime | Y         | UTC timestamp when cancel request was initiated                                |
| 167 | SecurityType | N         | `OPT` for option orders, `MLEG` for multileg orders                            |

To acknowledge this message, an Execution Report (8) with `150=6` is sent immediately followed by an Execution Report (8) with `150=4` or an Order Cancel Reject (9) message. Sometimes an Order Cancel Reject (9) message might be sent directly without sending an Execution Report (8) with `150=6`. For multileg orders, the acknowledgements are generated for each leg (`442=2`) and, when enabled, at the parent level (`442=3`).

**Example FIX Messages**

```text Cancel Request
|8=FIX.4.2|9=190|35=F|34=5|49=SENDER|52=20240524-16:02:44.709|56=ALPACA|1=account1|11=b165965d-0c9d-467e-a174-ee30f3fe6dbe|41=b5db0b8e-bbc1-4906-aff8-c58d18ba3398|54=1|55=AAPL|60=20240524-16:02:44.709206406|10=226|
```

## Order Cancel/Replace Request (G)

Sent by the client to request modification of a single-leg (equity or single-leg option) order. To modify a multi-leg order, use [Multileg Order Cancel/Replace Request (AC)](#multileg-order-cancelreplace-request-ac) instead.

| Tag | Field        | Mandatory | Description                                                                                              |
| --- | ------------ | --------- | -------------------------------------------------------------------------------------------------------- |
| 35  | MsgType      | Y         | G - For Order Cancel/Replace Request                                                                     |
| 1   | Account      | Y         | Account number                                                                                           |
| 11  | ClOrdID      | Y         | Unique identifier of the replacement order assigned by the client (must be no longer than 48 characters) |
| 21  | HandlInst    | Y         | 1 - Automated execution with no broker intervention, only accepted value                                 |
| 38  | OrderQty     | N         | Modified quantity for the order                                                                          |
| 40  | OrdType      | Y         | As specified on the original order                                                                       |
| 41  | OrigClOrdID  | Y         | ClOrdID (11) of the order to be modified as assigned by the client                                       |
| 44  | Price        | N         | Modified price for the order                                                                             |
| 54  | Side         | Y         | As specified on the original order                                                                       |
| 55  | Symbol       | Y         | As specified on the original order                                                                       |
| 59  | TimeInForce  | N         | Modified time in force for the order                                                                     |
| 60  | TransactTime | Y         | UTC timestamp when cancel/replace request was initiated                                                  |
| 99  | StopPx       | N         | Modified stop price for the order                                                                        |

**Example FIX Messages**

```text Cancel/Replace Request
|8=FIX.4.2|9=212|35=G|34=21|49=SENDER|52=20240524-16:16:58.956|56=ALPACA|1=account1|11=45169819-088a-4089-9758-f28e830e95f0|21=3|40=2|41=f001f209-2c3e-42e3-9ab1-10e74ee39fe5|44=1.50000|54=1|55=AAPL|60=20240524-16:16:58.956849295|10=173|
```

## Order Cancel Reject (9)

Sent by the server if the Order Cancel Request (F) or Order Cancel/Replace Request (G) message could not be honored. Some common reject scenarios include:

* when order is already filled or closed
* when a previous Order Cancel Request (F) or Order Cancel/Replace Request (G) is pending for this order

| Tag | Field            | Mandatory | Description                                                                                                                                                                                |
| :-- | :--------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType          | Y         | 9 - For Order Cancel Reject                                                                                                                                                                |
| 1   | Account          | Y         | Account number                                                                                                                                                                             |
| 11  | ClOrdID          | Y         | Unique identifier of cancel or cancel/replace request as assigned by the client                                                                                                            |
| 37  | OrderID          | Y         | Unique identifier of the order as assigned by Alpaca for which the cancel or cancel/replace request was rejected                                                                           |
| 39  | OrdStatus        | Y         | Order status after this cancel reject is applied                                                                                                                                           |
| 41  | OrigClOrdID      | Y         | ClOrdID (11) of the order for which the cancel or cancel/replace request was rejected                                                                                                      |
| 58  | Text             | N         | Reject reason                                                                                                                                                                              |
| 60  | TransactTime     | N         | Server time in UTC when cancel or replace reject occurred                                                                                                                                  |
| 102 | CxlRejReason     | N         | Code to identify reason for cancel rejection.<br />0 - Too late to cancel<br />1 - Unknown order<br />2 - Broker Option<br />3 - Order already in Pending Cancel or Pending Replace status |
| 434 | CxlRejResponseTo | Y         | 1 - Response to Order Cancel Request (F)<br />2 - Response to Order Cancel/Replace Request (G)                                                                                             |

**Example FIX Messages**

```text Cancel Reject
|8=FIX.4.2|9=220|35=9|34=18|49=ALPACA|52=20240524-16:02:46.215|56=SENDER|1=account1|11=a7860828-4dc5-4f8f-bfb1-8fbca8855c88|37=f50af678-bba4-44ea-9b23-0fc452ed4921|39=6|41=2c017b79-a843-4146-a2b7-3bf83af89482|58=TOO_LATE_TO_CANCEL|434=1|10=116|
```
```text Cancel/Replace Reject
|8=FIX.4.2|9=198|35=9|34=45|49=ALPACA|52=20240524-16:16:59.085|56=SENDER|1=account1|11=5cdf9082-067b-4497-a90c-f5e8c666409b|37=UNKNOWN|39=8|41=c7feaf5a-54d2-458d-8ab2-9b2f337a28ec|58=replace pending for order|434=2|10=179|
```

## New Order - Multileg (AB)

Sent by the client to submit a new multi-leg order such as an option spread, straddle, strangle, or covered call. Although the FIX session operates on `BeginString=FIX.4.2`, the `NewOrderMultileg` message (`35=AB`) and its `NoLegs` repeating group follow the FIX 4.4 specification.

Each leg may be either an option contract or an equity (for strategies that combine equity with options such as covered calls). The order is submitted as a single multileg request, and acknowledgements are returned at both the leg level and (optionally) the parent level — see [Execution Report (8)](#execution-report-8) for details.

| Tag  | Field             | Mandatory | Description                                                                                                                                                                               |
| :--- | :---------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35   | MsgType           | Y         | AB - For New Order Multileg                                                                                                                                                               |
| 1    | Account           | Y         | Account number                                                                                                                                                                            |
| 11   | ClOrdID           | Y         | Unique identifier of the parent order assigned by the client (must be no longer than 64 characters)                                                                                       |
| 18   | ExecInst          | N         | 1 - Not held<br />5 - Held                                                                                                                                                                |
| 21   | HandlInst         | Y         | 1 - Automated execution with no broker intervention, only accepted value                                                                                                                  |
| 38   | OrderQty          | Y         | Number of spread units to trade. Per-leg quantity is `OrderQty * LegRatioQty (623)`                                                                                                       |
| 40   | OrdType           | Y         | 1 - Market<br />2 - Limit<br />3 - Stop<br />4 - Stop limit<br />5 - Market on close<br />B - Limit on close                                                                              |
| 44   | Price             | N         | Net debit/credit price per spread unit. Required for Limit (`40=2`) and Stop Limit (`40=4`) orders                                                                                        |
| 55   | Symbol            | Y         | Underlying root symbol common to all legs (e.g. `AAPL`)                                                                                                                                   |
| 59   | TimeInForce       | Y         | 0 - Day (day)<br />1 - Good Till Cancel (gtc)<br />2 - At the Opening (opg)<br />3 - Immediate or Cancel (ioc)<br />4 - Fill or Kill (fok)<br />7 - At the Close (cls)                    |
| 60   | TransactTime      | Y         | UTC timestamp of order creation by client                                                                                                                                                 |
| 99   | StopPx            | N         | Required for Stop (`40=3`) and Stop Limit (`40=4`) orders                                                                                                                                 |
| 152  | CashOrderQty      | N         | Notional value to trade                                                                                                                                                                   |
| 167  | SecurityType      | N         | MLEG - Multileg Instrument (recommended)                                                                                                                                                  |
| 555  | NoLegs            | Y         | Number of legs in the order. Must be **at least 2**. The repeating group fields below are repeated `NoLegs` times. Side (54) must NOT be supplied at the parent level for multileg orders |
| →600 | LegSymbol         | Y         | Per-leg symbol. For option legs, the underlying root (e.g. `AAPL`); for equity legs, the equity ticker                                                                                    |
| →608 | LegCFICode        | Y         | OC - Option Call<br />OP - Option Put<br />ES - Equity (for strategies like covered calls)                                                                                                |
| →611 | LegMaturityDate   | N         | Expiration date in `YYYYMMDD` format.<br />Required for option legs (`LegCFICode = OC` or `OP`)                                                                                           |
| →612 | LegStrikePrice    | N         | Strike price of the option leg.<br />Required for option legs (`LegCFICode = OC` or `OP`)                                                                                                 |
| →623 | LegRatioQty       | Y         | Ratio of this leg relative to the parent OrderQty. Must be positive. Per-leg quantity = `OrderQty * LegRatioQty`                                                                          |
| →624 | LegSide           | Y         | 1 - Buy<br />2 - Sell                                                                                                                                                                     |
| →654 | LegRefID          | Y         | Client-assigned per-leg identifier, unique within the order (max 32 characters). Echoed back on every leg execution report                                                                |
| →564 | LegPositionEffect | N         | O - Open<br />C - Close<br />Combined with `LegSide` to derive the per-leg position intent. When omitted, intent is inferred from `LegSide` (Buy → open, Sell → close)                    |

**Notes**

* Multileg orders that include `Side (54)` at the parent level, have fewer than 2 legs, or are missing any required leg field are rejected with a Business Message Reject (code 9001).
* Each leg's execution report echoes the `LegRefID (654)` supplied on the order, so leg-level acknowledgements can be correlated with the originating leg.
* MOC (`40=5`) and LOC (`40=B`) order types are equivalent to submitting `OrdType` Market / Limit with `TimeInForce (59) = 7` (At the Close).

**Example FIX Message**

```text Multileg Limit (long call vertical: buy 100C @ ask, sell 105C @ bid, net debit limit 10.50)
|8=FIX.4.2|9=350|35=AB|34=42|49=SENDER|52=20240910-15:00:00.000|56=ALPACA|1=account1|11=spread-001|21=1|38=2|40=2|44=10.5|55=AAPL|59=0|60=20240910-15:00:00.000|167=MLEG|555=2|600=AAPL|654=0|608=OC|611=20250117|612=100|624=1|623=1|564=O|600=AAPL|654=1|608=OC|611=20250117|612=105|624=2|623=1|564=O|10=147|
```

## Multileg Order Cancel/Replace Request (AC)

Sent by the client to request modification of a multi-leg order. Like [New Order - Multileg (AB)](#new-order---multileg-ab), the message body follows the FIX 4.4 specification while the session remains on `BeginString=FIX.4.2`.

The replacement message must re-supply the complete `NoLegs` repeating group. Replacing a multileg order will produce a `Pending Replace` (`150=E`) and then a `Replaced` (`150=5`) execution report for each leg, and (when enabled) at the parent level.

| Tag | Field        | Mandatory | Description                                                                                                                                                                                                                                   |
| :-- | :----------- | :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35  | MsgType      | Y         | AC - For Multileg Order Cancel/Replace Request                                                                                                                                                                                                |
| 1   | Account      | Y         | Account number                                                                                                                                                                                                                                |
| 11  | ClOrdID      | Y         | Unique identifier of the replacement order assigned by the client (must be no longer than 64 characters)                                                                                                                                      |
| 21  | HandlInst    | Y         | 1 - Automated execution with no broker intervention, only accepted value                                                                                                                                                                      |
| 38  | OrderQty     | N         | Modified spread quantity for the order                                                                                                                                                                                                        |
| 40  | OrdType      | Y         | As specified on the original order                                                                                                                                                                                                            |
| 41  | OrigClOrdID  | Y         | ClOrdID (11) of the parent order being modified                                                                                                                                                                                               |
| 44  | Price        | N         | Modified net price per spread unit                                                                                                                                                                                                            |
| 55  | Symbol       | Y         | Underlying root symbol (as on the original order)                                                                                                                                                                                             |
| 59  | TimeInForce  | N         | Modified time in force for the order                                                                                                                                                                                                          |
| 60  | TransactTime | Y         | UTC timestamp when cancel/replace request was initiated                                                                                                                                                                                       |
| 99  | StopPx       | N         | Modified stop price for the order                                                                                                                                                                                                             |
| 167 | SecurityType | N         | MLEG - Multileg Instrument (recommended)                                                                                                                                                                                                      |
| 555 | NoLegs       | Y         | Re-supply the full leg list (≥ 2 legs). Side (54) must NOT be supplied at the parent level. See [New Order - Multileg (AB)](#new-order---multileg-ab) for the repeating group fields (`600`, `608`, `611`, `612`, `623`, `624`, `654`, `564`) |

**Notes**

* Submitting a Multileg Cancel/Replace while a previous replace is still pending for the same `OrigClOrdID` is rejected with an [Order Cancel Reject (9)](#order-cancel-reject-9) (`text=replace pending for order`).
* The `NoLegs` group is validated with the same rules as the new-order message; rejections are returned via Business Message Reject (code 9001).

**Example FIX Message**

```text Multileg Cancel/Replace (raise net limit from 10.50 to 11.00)
|8=FIX.4.2|9=370|35=AC|34=58|49=SENDER|52=20240910-15:05:00.000|56=ALPACA|1=account1|11=spread-001-rep|21=1|38=2|40=2|41=spread-001|44=11.0|55=AAPL|60=20240910-15:05:00.000|167=MLEG|555=2|600=AAPL|654=0|608=OC|611=20250117|612=100|624=1|623=1|564=O|600=AAPL|654=1|608=OC|611=20250117|612=105|624=2|623=1|564=O|10=189|
```

## Version History

<Table align={[null,"left",null]}>
  <thead>
    <tr>
      <th>
        Version
      </th>

      <th>
        Date<br />(DD/MM/YYYY)
      </th>

      <th>
        Change
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        0.1.0
      </td>

      <td>
        08/05/2024
      </td>

      <td>
        Document Creation
      </td>
    </tr>

    <tr>
      <td>
        0.1.1
      </td>

      <td>
        24/05/2024
      </td>

      <td>
        Changed FIX version to FIX.4.2<br />Removed ApplVerID (1128) from Message Header<br />Added ClOrdID (11) and OrigClOrdID (41) as required in Order Cancel Request (F) and Order Cancel/Replace Request (G)<br />Removed OrderID (37) from Order Cancel Request (F) and Order Cancel/Replace Request (G)<br />Added OrderQty (38) to Order Cancel/Replace Request (G)<br />Updated FIX examples
      </td>
    </tr>

    <tr>
      <td>
        0.1.2
      </td>

      <td>
        12/06/2024
      </td>

      <td>
        Removed Account (1) and RawData (96) from Logon (A) message<br />Added RefTagID (371), RefMsgType (372) and SessionRejectReason (373) to Reject (3) message<br />Added HandlInst (21), TransactTime (60) and OpenClose (77) to New Order - Single (D)<br />Added 1 (per share) as an accepted value for CommType (13) in New Order - Single (D)<br />Updated AvgPx (6) to mandatory in Execution Report (8)<br />Added Commission (12), ExecRefID (19), ExecTransType (20), LastMkt (30), OrderQty (38) and CashOrderQty (152) to Execution Report (8)<br />Removed OrdRejReason (103) from Execution Report (8)<br />Updated possible values for ExecType (150) in Execution Report (8)
      </td>
    </tr>

    <tr>
      <td>
        1.0.0
      </td>

      <td>
        13/06/2024
      </td>

      <td>
        Added Side (54), Symbol (55) and TransactTime (60) to Order Cancel Request (F)<br />Added OrderID (37) to Order Cancel Reject (9)<br />Added HandlInst (21), OrdType (40), Side (54), Symbol (55) and TransactTime (60) to Order Cancel/Replace Request (G)
      </td>
    </tr>

    <tr>
      <td>
        1.0.1
      </td>

      <td>
        04/09/2024
      </td>

      <td>
        Added Market on close (5) and Limit on close (B) as values for OrdType (40) on New Order - Single (D)<br />Added At the Close (7) as a value for TimeInForce (59) on New Order - Single (D)
      </td>
    </tr>

    <tr>
      <td>
        1.0.2
      </td>

      <td>
        08/10/2024
      </td>

      <td>
        Added Restated (D) as value for ExecType (150) on Execution Report (8)<br />Added ExecRestatementReason (378) to Execution Report (8)<br />Added Status (3) as value for ExecTransType (20) on Execution Report (8)<br />Added TransactTime (60) to Order Cancel Reject (9)
      </td>
    </tr>

    <tr>
      <td>
        1.0.3
      </td>

      <td>
        14/01/2025
      </td>

      <td>
        Added Good Till Crossing (5) as a value for TimeInForce (59) on New Order - Single (D)<br />Added ClientID (109) to New Order - Single (D)
      </td>
    </tr>

    <tr>
      <td>
        1.0.4
      </td>

      <td>
        03/04/2025
      </td>

      <td>
        Removed Good Till Crossing (5) as a valid value for TimeInForce (59) on New Order - Single (D)<br />Added TradingSessionID (336) to New Order - Single (D)
      </td>
    </tr>

    <tr>
      <td>
        1.1.0
      </td>

      <td>
        11/05/2026
      </td>

      <td>
        Added Options L3 support:<br />Added SecurityType (167), MaturityMonthYear (200), PutOrCall (201), StrikePrice (202) and MaturityDay (205) to New Order - Single (D) for single-leg option orders<br />Added SecurityType (167), MaturityMonthYear (200), PutOrCall (201), StrikePrice (202), MaturityDay (205), OpenClose (77), MultiLegReportingType (442), LegRefID (654) and NoLegs (555) to Execution Report (8)<br />Added SecurityType (167) to Order Cancel Request (F) to support cancellation of multileg and option orders<br />Added New Order - Multileg (AB) message with the NoLegs (555) repeating group (LegSymbol 600, LegCFICode 608, LegMaturityDate 611, LegStrikePrice 612, LegRatioQty 623, LegSide 624, LegRefID 654, LegPositionEffect 564)<br />Added Multileg Order Cancel/Replace Request (AC) message
      </td>
    </tr>

    <tr>
      <td>
        1.2.0
      </td>

      <td>
        30/07/2026
      </td>

      <td>
        Added EffectiveTime (168) to New Order - Single (D)
        Added EffectiveTime (168) to Execution Report (8)
      </td>
    </tr>
  </tbody>
</Table>

<br />