# Tokenization Guide for Authorized Participant

Source: https://docs.alpaca.markets/us/docs/tokenization-guide-for-authorized-participant.md

---
updatedAt: 2026-09-22T08:16:35.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Tokenization Guide for Authorized Participant

The Instant Tokenization Network (ITN) is a platform designed to streamline and accelerate the process of in-kind creation and redemption of tokenized assets. The goal of the ITN is to enable efficient, secure, and rapid conversion of real-world and digital assets to and from various tokens issued by partners on the network. The network acts as instant settlement rails for market participants to programmatically rebalance inventory thereby stitching together fragmented tokenized asset liquidity across the industry. This document will guide the **Authorized Participant** on how to start using Alpaca’s Instant Tokenization Network.

# Overview

Before you can start integrating into Alpaca's ITN (Instant Tokenization Network) as an authorized participant, there are multiple steps that you need to complete:

1. Sign up as an authorized participant with the issuer(s) directly so that you are allowed to mint and redeem their tokens.
2. Integrate into Alpaca's Broker API or Trading API offering to buy and sell stocks on an account in your name at Alpaca. This would allow Alpaca to move stocks to/from your account during the token mint and redeem flows.

Once you have completed the above, this document will guide you to integrate into ITN as an AP. You will need to:

* Provide Alpaca's integration team with:
  * The email address you used when signing up with the issuer(s) as an AP.
  * The Alpaca account number that you expect stock to be moved to/from.
  * Alpaca's integration team will need to perform a handshake process with the issuer to link your Alpaca account to your Issuer account.
* Integrate with 1 Alpaca endpoint that you will utilize to initiate the token minting flow:
  * [Mint Request](https://docs.alpaca.markets/docs/tokenization-guide-for-authorized-participant#alpacas-mint-request)
* Optionally, you can also query the history of your tokenization requests via the [List Tokenization Requests](https://docs.alpaca.markets/docs/tokenization-guide-for-authorized-participant#list-tokenization-requests) endpoint documented at the end of this guide.

# Quantity Precision

Alpaca accepts up to **9 decimal places** for underlying securities quantities. Any mint request with a `qty` exceeding 9 decimals will be rejected with a `400 Bad Request`.

The same 9-decimal cap also applies to the Issuer when it submits a redeem request to Alpaca on your behalf. When your token's on-chain precision exceeds this (e.g. 18 decimals on Ethereum), the Issuer will typically round the underlying-security redemption quantity **down** to 9 decimals, so a trivially small residual token amount may remain unconverted on each redemption.

# Mint Endpoint and Workflow

The token minting flow has multiple steps that begin when you, as an AP, request token minting from Alpaca. The steps are explained below & depicted in Figure 1 to help you visualize. Any referenced endpoints are also documented below.

1. Once the handshake process mentioned earlier is completed, you will be able to request minting of tokenized assets using [Alpaca's mint request endpoint](https://docs.alpaca.markets/docs/tokenization-guide-for-authorized-participant#alpacas-mint-request).
2. The mint request is validated by both Alpaca and the Issuer.
   1. Alpaca will validate that you:
      1. Are an AP authorized for tokenizations.
      2. Have enough underlying position to mint on your registered Alpaca account.
   2. The Issuer will validate that:
      1. The wallet address you provided is registered to the AP.
      2. The requested token is available on the requested network.
3. Upon successful validation of the mint request, Alpaca transfers the requested quantity of the underlying security from your Alpaca account into the Issuer's Alpaca account.
4. Alpaca confirms with the Issuer that the underlying security has been transferred to their account.
5. The issuer then deposits the tokenized assets in the wallet address you've provided on the mint request.
6. Finally, the Issuer informs Alpaca of the successful deposit of tokens in the AP’s wallet address.

<Image align="center" caption="Figure 1. Minting a tokenized asset" src="https://files.readme.io/a23b585ba0b7474a3b1b825ab4bec1429ae6c6dd4b4bd3a9832c5eb51768ac5e-3f7824e1f515ce0e46b759d7a4f4052cc4e5a0c736e2b33a3671b251c0c162b5-Minting_Redeeming2x.png" />

#### Alpaca's Mint Request

More details in full [API reference](https://docs.alpaca.markets/reference/posttokenizationmintbroker).

**Endpoint**

```html
POST /v1/accounts/:account_id/tokenization/mint
```

| Field       | Description                                                                  |
| :---------- | :--------------------------------------------------------------------------- |
| account\_id | Your Alpaca account\_id that Alpaca linked to your AP account at the issuer. |

**Body**

```json
{
  "underlying_symbol": "AAPL",
  "qty": "1.23",
  "issuer": "xstocks",
  "network": "solana",
  "wallet_address": "0x1234567A",
  "client_request_id": "my-mint-ref-001"
}
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        underlying_symbol
      </td>

      <td>
        Underlying asset symbol
      </td>
    </tr>

    <tr>
      <td>
        qty
      </td>

      <td>
        The underlying quantity to convert into the tokenized asset. The value can be fractional.
      </td>
    </tr>

    <tr>
      <td>
        issuer
      </td>

      <td>
        The tokenized asset's Issuer. Valid values are:

        * binance
        * coinbase
        * ondo
        * st0x
        * xstocks
      </td>
    </tr>

    <tr>
      <td>
        network
      </td>

      <td>
        The token's blockchain's network. Valid values are:

        * arbitrum

        * base

        * binance

        * cronos

        * ethereum

        * hypercore

        * hyperevm

        * mantle

        * robinhood

        * solana

        * ton

        * tron
      </td>
    </tr>

    <tr>
      <td>
        wallet_address
      </td>

      <td>
        The destination wallet address where the tokenized assets should be deposited.

        <br />

        **Important Note:** You will need to check with the issuer whether this wallet address has to be whitelisted on their platform, and if so you will need to whitelist the address before you can use it as part of a mint request.
      </td>
    </tr>

    <tr>
      <td>
        client_request_id
      </td>

      <td>
        Optional. A client-supplied correlation label, echoed back on the response. At most 128 characters, printable ASCII only, no leading or trailing whitespace.
      </td>
    </tr>
  </tbody>
</Table>

**Idempotency**

Mint submissions are safe to retry using an optional `Idempotency-Key` HTTP header, so that a retry (for example after a network timeout) does not create a duplicate mint:

```http
Idempotency-Key: <your-unique-key>
```

* When present, the value must be between 1 and 128 characters after trimming surrounding whitespace, and contain only printable ASCII characters (no spaces). A malformed key is rejected with `400 Bad Request`.
* If Alpaca has already processed a request with the same `Idempotency-Key` **and an identical body**, the original response is replayed instead of creating a new mint request, and Alpaca sets the `Idempotent-Replayed: true` response header. A replay of a request that was originally `rejected` is returned with `400 Bad Request`.
* Reusing the same `Idempotency-Key` with a **different body** is rejected with `422 Unprocessable Entity`.

**Response**

**Body**

```json
{
  "tokenization_request_id": "14d484e3-46f9-4e11-99ac-6fee0d4455c7",
  "created_at":"2025-09-12T17:28:48.642437-04:00",
  "status": "pending",
  "underlying_symbol": "AAPL",
  "token_symbol": "AAPLx",
  "qty": "3",
  "issuer": "xstocks",
  "network": "solana",
  "client_request_id": "my-mint-ref-001"
}
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        tokenization_request_id
      </td>

      <td>
        Unique request identifier assigned by Alpaca
      </td>
    </tr>

    <tr>
      <td>
        created_at
      </td>

      <td>
        Timestamp when Alpaca received the mint request
      </td>
    </tr>

    <tr>
      <td>
        status
      </td>

      <td>
        Current status of the mint request:

        * pending
        * completed
        * rejected
      </td>
    </tr>

    <tr>
      <td>
        underlying_symbol
      </td>

      <td>
        The underlying asset symbol
      </td>
    </tr>

    <tr>
      <td>
        token_symbol
      </td>

      <td>
        The tokenized asset symbol
      </td>
    </tr>

    <tr>
      <td>
        qty
      </td>

      <td>
        The underlying quantity to convert into the tokenized asset. It can be fractional.
      </td>
    </tr>

    <tr>
      <td>
        issuer
      </td>

      <td>
        The tokenized asset's issuer. Valid values are:

        * binance
        * coinbase
        * ondo
        * st0x
        * xstocks
      </td>
    </tr>

    <tr>
      <td>
        network
      </td>

      <td>
        The token's blockchain network. Valid values are:

        * arbitrum

        * base

        * binance

        * cronos

        * ethereum

        * hypercore

        * hyperevm

        * mantle

        * robinhood

        * solana

        * ton

        * tron
      </td>
    </tr>

    <tr>
      <td>
        client_request_id
      </td>

      <td>
        The correlation label you supplied on the mint request, echoed back. Omitted if you did not supply one.
      </td>
    </tr>
  </tbody>
</Table>

**Status Codes**

| Status | Description                                                                                   |
| :----- | :-------------------------------------------------------------------------------------------- |
| 200    | OK - Mint request created successfully                                                        |
| 400    | Bad request (e.g. malformed input, insufficient position, or account not authorized to mint). |
| 401    | Authentication credentials are missing or invalid.                                            |
| 403    | Caller is not authorized to perform this operation.                                           |
| 422    | Invalid Parameters - One or more parameters provided are invalid.                             |

# Redeem Workflow

The token redeem flow has multiple steps that begin when you, as an AP, deposit tokens to an issuer's redemption wallet address. The steps are explained below & depicted in Figure 2 to help you visualize.

1. The token redemption process will be initiated by the AP by moving their tokens into the Issuer’s redemption wallet address. The Issuer will remove these tokens from circulation.
2. The Issuer will then notify Alpaca that an AP has redeemed their tokens. The issuer will provide multiple fields to Alpaca as documented [here](https://docs.alpaca.markets/docs/tokenization-guide-for-issuer#alpacas-redeem-request-endpoint).
3. Finally, Alpaca will transfer the underlying asset from the Issuer’s Alpaca account into the AP’s Alpaca account.

<Image align="center" caption="Figure 2. Redeeming a tokenized asset" src="https://files.readme.io/3263fe54e35d13d4b3c214298696e9c5d2498a10ea1eb0bb22759627044aa10c-661cc0f3b3881fcdf4d87de2ca7866efe56bea8f8e250965836952699552ea5f-Minting_Redeeming2x_2.png" />

# Additional Useful Endpoints

#### List Tokenization Requests

You can use the following endpoint to list the tokenization requests performed on the Instant Tokenization Network platform. For more details, check full [API reference](https://docs.alpaca.markets/reference/gettokenizationrequestsbroker).

**Request**

**Endpoint**

```html
GET /v1/accounts/:account_id/tokenization/requests
```

**Response**

**Body**

```json
[
   {
    "tokenization_request_id": "12345-678-90AB",
    "created_at":"2025-09-12T17:28:48.642437-04:00",
    "updated_at":"2025-09-12T17:28:48.642437-04:00",
    "type": "redeem",
    "status": "completed",
    "underlying_symbol": "TSLA",
    "token_symbol" : "TSLAx",
    "qty" : "123.45",
    "issuer" : "xstocks",
    "network": "solana",
    "wallet_address": "0x1234567A",
    "tx_hash" : "0x1234567A",
    "fees" : "0.567"
  },
  {
    "tokenization_request_id": "12345-678-90AB",
    "created_at":"2025-09-12T17:28:48.642437-04:00",
    "updated_at":"2025-09-12T17:28:48.642437-04:00",
    "type": "redeem",
    "status": "completed",
    "underlying_symbol": "TSLA",
    "token_symbol" : "TSLAx",
    "qty" : "123.45",
    "issuer" : "xstocks",
    "network": "solana",
    "wallet_address": "0x1234567A",
    "tx_hash" : "0x1234567A",
    "fees" : "0.567"
  },
  {
    "tokenization_request_id": "12345-678-90AB",
    "created_at":"2025-09-12T17:28:48.642437-04:00",
    "updated_at":"2025-09-12T17:28:48.642437-04:00",
    "type": "redeem",
    "status": "completed",
    "underlying_symbol": "TSLA",
    "token_symbol" : "TSLAx",
    "qty" : "123.45",
    "issuer" : "xstocks",
    "network": "solana",
    "wallet_address": "0x1234567A",
    "tx_hash" : "0x1234567A",
    "fees" : "0.567"
  }
]
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        tokenization_request_id
      </td>

      <td>
        Unique request identifier assigned by Alpaca
      </td>
    </tr>

    <tr>
      <td>
        created_at
      </td>

      <td>
        Timestamp when the request was created
      </td>
    </tr>

    <tr>
      <td>
        updated_at
      </td>

      <td>
        Timestamp when the request was last updated
      </td>
    </tr>

    <tr>
      <td>
        type
      </td>

      <td>
        Tokenization request type. Valid values are:

        * mint
        * redeem
      </td>
    </tr>

    <tr>
      <td>
        status
      </td>

      <td>
        Current status of the tokenization request:

        * pending
        * completed
        * rejected
      </td>
    </tr>

    <tr>
      <td>
        underlying_symbol
      </td>

      <td>
        The underlying asset symbol
      </td>
    </tr>

    <tr>
      <td>
        token_symbol
      </td>

      <td>
        The token asset symbol
      </td>
    </tr>

    <tr>
      <td>
        qty
      </td>

      <td>
        The quantity for this request
      </td>
    </tr>

    <tr>
      <td>
        issuer
      </td>

      <td>
        The tokenized asset's Issuer. Valid values are:

        * binance
        * coinbase
        * ondo
        * st0x
        * xstocks
      </td>
    </tr>

    <tr>
      <td>
        network
      </td>

      <td>
        The token's blockchain's network. Valid values are:

        * arbitrum

        * base

        * binance

        * cronos

        * ethereum

        * hypercore

        * hyperevm

        * mantle

        * robinhood

        * solana

        * ton

        * tron
      </td>
    </tr>

    <tr>
      <td>
        wallet_address
      </td>

      <td>
        The wallet address associated with this request
      </td>
    </tr>

    <tr>
      <td>
        tx_hash
      </td>

      <td>
        The transaction hash on the blockchain
      </td>
    </tr>

    <tr>
      <td>
        fees
      </td>

      <td>
        The fees charged for this tokenization request
      </td>
    </tr>

    <tr>
      <td>
        client_request_id
      </td>

      <td>
        The correlation label you supplied on the original mint request, echoed back. Present on mint requests where you supplied one.
      </td>
    </tr>
  </tbody>
</Table>

#### Get a Tokenization Request by ID

Fetch a single tokenization request by the Alpaca-assigned `tokenization_request_id`. Returns the same object as a single entry in the [List Tokenization Requests](#list-tokenization-requests) response.

**Request**

**Endpoint**

```html
GET /v1/accounts/:account_id/tokenization/requests/:tokenization_request_id
```

| Field                     | Description                                             |
| :------------------------ | :------------------------------------------------------ |
| account\_id               | Your Alpaca account\_id.                                |
| tokenization\_request\_id | The Alpaca-assigned identifier of the request to fetch. |

**Status Codes**

| Status | Description                                                         |
| :----- | :------------------------------------------------------------------ |
| 200    | OK                                                                  |
| 401    | Authentication credentials are missing or invalid.                  |
| 404    | No tokenization request with that id exists for your account.       |
| 422    | Invalid Parameters - `tokenization_request_id` is not a valid UUID. |

#### Get a Tokenization Request by Client Request ID

Fetch a single tokenization request by the `client_request_id` you supplied on the original mint request. Returns the same object as a single entry in the [List Tokenization Requests](#list-tokenization-requests) response.

**Request**

**Endpoint**

```html
GET /v1/accounts/:account_id/tokenization/requests:by_client_request_id?client_request_id=<your-value>
```

| Field               | Description                                                                          |
| :------------------ | :----------------------------------------------------------------------------------- |
| account\_id         | Your Alpaca account\_id.                                                             |
| client\_request\_id | The correlation label you supplied on the mint request, passed as a query parameter. |

**Status Codes**

| Status | Description                                                                    |
| :----- | :----------------------------------------------------------------------------- |
| 200    | OK                                                                             |
| 401    | Authentication credentials are missing or invalid.                             |
| 404    | No tokenization request with that `client_request_id` exists for your account. |
| 422    | Invalid Parameters - the `client_request_id` query parameter is missing.       |

# Glossary

* **Authorized Participant**: An entity licensed to conduct digital asset business in the tokenized asset, e.g xstocks. The Issuer only sells tokenized assets to Authorized Participants (AP). The AP can sell the tokenized assets to their clients.
* **Issuer**: Financial entity which purchases the underlying equity securities, wraps them and creates/issues tokens which are backed by the same.
* **Mint**: The act of converting underlying equity securities into tokenized assets.
* **Redeem**: The act of converting tokenized assets into their underlying equity securities.

<br />

*Alpaca's Instant Tokenization Network is owned and developed by AlpacaDB, Inc. and Alpaca Crypto LLC.
Additional geographic restrictions may apply for tokenization services based on local regulatory requirements. Neither Alpaca Crypto LLC nor Alpaca Securities LLC are the issuer of, nor directly involved in, the tokenization of any assets. Tokenization is performed by a third party. Tokenized assets do not represent direct equity ownership in any underlying company or issuer. Instead, tokenized assets generally provide economic exposure to the equity securities of an underlying issuer. As such, holders of tokenized assets have no voting rights, dividend entitlements, or legal claims to the underlying company shares or any residual assets in the event of the underlying company’s liquidation or insolvency, unless explicitly stated otherwise. All investments involve risk. For more information, please see our Tokenization Risk <Anchor label="Disclosure" target="_blank" href="https://files.alpaca.markets/disclosures/library/Tokenization+Disclosure.pdf">Disclosure</Anchor>.*