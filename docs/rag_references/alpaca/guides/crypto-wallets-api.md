# Crypto Wallets API

Source: https://docs.alpaca.markets/us/docs/crypto-wallets-api.md

---
updatedAt: 2026-09-01T15:10:00.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Crypto Wallets API

*Please note you have to reach out to Alpaca to enable Crypto Wallets API access. Please reach out to your Customer Success Manager or your Sales Representative to enable this feature for you.*

## **Overview**

The Alpaca Crypto Wallets API enables you to deposit, withdraw, and manage cryptocurrency assets within your Alpaca account. This document explains how to use Alpaca’s Crypto Wallets API to test fund accounts with crypto assets (like USDC), verify transfers, and begin trading.

## **Supported Assets**

### **Supported Testnets & Faucets (Sandbox)**

To test deposit and withdrawal flows for different assets across supported blockchain networks, you can use the following testnet faucets. Always ensure you’re requesting tokens and interacting on the correct network (e.g., Ethereum Sepolia, Solana Devnet).

**Stablecoins**

* **USDC (Testnet/Devnet Support)**
  * Networks: Ethereum Sepolia, Solana Devnet
  * Faucet: [Circle Testnet Faucet](https://faucet.circle.com/)
* **USDG (Testnet Support)**
  * Networks: Ethereum Sepolia, Solana Devnet
  * Faucet: [Paxos Faucet](https://faucet.paxos.com/)
* **USDT (Testnet)**
  * Network: Ethereum Sepolia
  * Faucet:
    * [WeenusTokenFaucet GitHub](https://github.com/bokkypoobah/WeenusTokenFaucet?tab=readme-ov-file#testnet-ether-faucets)
    * Contract Address: [0x7439...fB9 on Etherscan](https://sepolia.etherscan.io/address/0x7439E9Bb6D8a84dd3A23fe621A30F95403F87fB9#code)

**BTC (Testnet)**

* **tBTC** — [Bitcoin Testnet4 Faucet](https://faucet.testnet4.dev/)

**Solana (Devnet)**

* [Solana Devnet Faucet – Airdrop SOL](https://faucet.solana.com/)

**ETH (Sepolia)**

* [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)

* [Google Cloud Sepolia Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)

* [QuickNode Faucet](https://faucet.quicknode.com/ethereum)

**XRP (Testnet)**

* [XRPL Tesnet Faucet](https://test.bithomp.com/en/faucet)

***

## **Getting Started: Sandbox Testing Guide**

### **Step 1: Generate Your Funding Wallet Address**

Create or retrieve your crypto funding wallet address for the desired asset:

[`GET /v1/accounts/{account_id}/wallets?asset=USDC&network=ethereum`](https://docs.alpaca.markets/reference/listcryptofundingwallets-1)

**Response:**

```json
{
    "asset_id": "5d0de74f-827b-41a7-9f74-9c07c08fe55f",
    "address": "0x42a76C83014e886e639768D84EAF3573b1876844",
    "created_at": "2025-08-07T08:52:40.656166Z"
}
```

### **Step 2: Fund Your Wallet (Sandbox)**

#### **For USDC Testing:**

1. Visit the **Circle Sepolia Faucet**: <https://faucet.circle.com>
2. Paste your wallet address from Step 1
3. Click **Send**
4. Wait for \~12 block confirmations (typically 2-3 minutes)

### **Step 3: Verifying Deposits**

Monitor incoming transfers to confirm your deposit:

#### Option 1: Poll transfers API

[`GET /v1/accounts/{account_id}/wallets/transfers`](https://docs.alpaca.markets/reference/listcryptofundingtransfers-1)

**Response:**

```json
[
    {
        "id": "876b1c4f-df5e-4d1b-beaa-81af7f7bd02c",
        "tx_hash": "0xaca1f6ba105a68771d966b4ce17e0992ad3d8030d127cdb18e113efa3a864992",
        "direction": "INCOMING",
        "amount": "10",
        "usd_value": "9.99707",
        "chain": "ETH",
        "asset": "USDC",
        "from_address": "0x3C3380cdFb94dFEEaA41cAD9F58254AE380d752D",
        "to_address": "0x42a76C83014e886e639768D84EAF3573b1876844",
        "status": "COMPLETE",
        "created_at": "2025-08-07T10:31:41.964121Z",
        "network_fee": "0",
        "fees": "0"
    },
    {
        "id": "bf31ecca-e28c-4f9a-8e81-12bbf79836fd",
        "tx_hash": "0x849de6f0f225c18b58f3dea5a76a42a0dcba4902ce069147bb0dcd585a3e699b",
        "direction": "INCOMING",
        "amount": "5",
        "usd_value": "4.998794999999999",
        "chain": "ETH",
        "asset": "USDC",
        "from_address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
        "to_address": "0x42a76C83014e886e639768D84EAF3573b1876844",
        "status": "COMPLETE",
        "created_at": "2025-08-08T11:13:26.263719Z",
        "network_fee": "0",
        "fees": "0"
    }
]

```

**Status Values:**

* `PROCESSING`: Transaction submitted to blockchain
* `COMPLETE`: Funds available for trading
* `FAILED`: Transaction failed

#### Option 2: [NTA SSE event](https://docs.alpaca.markets/reference/get-v1-events-nta)

Sample event showing incoming deposit:

```json
{
    "id": "a6a3f62c-d4dd-4b6f-9b3a-fb65892c9695",
    "qty": 10,
    "cusip": "USDC12345",
    "status": "executed",
    "symbol": "USDCUSD",
    "entry_type": "OCT",
    "net_amount": 0,
    "description": "Deposit Transaction, transfer_id: 296f3a5b-72e8-4ec6-b1fe-77048e77e87f, tx_hash: 0x97fa0e98598d7bedf2871bc1846daa076cddafaa9046b3697b6cd89ca7304932",
    "settle_date": "2025-09-19",
    "system_date": "2025-09-19",
    "price": "0.9997",
    "per_share_amount": null,
    "account_id": "34c18dbe-0983-4e61-b493-9578714dae23",
    "at": "2025-09-19T08:09:01.061337Z",
    "event_ulid": "01K5GG9ZC5A3CVKP5QEZ79PVEX"
}

```

<br />

### **Step 4: Trading with Deposited Assets (Optional)**

Convert your deposited crypto to USD buying power by selling against USD:

[`POST /v1/trading/accounts/{account_id}/orders`](https://docs.alpaca.markets/reference/createorderforaccount)

**Request Body:**

```json
{
  "symbol": "USDC/USD",
  "qty": "50",
  "side": "sell",
  "type": "market", 
  "time_in_force": "day"
}
```

### **Step 5: Start Trading**

Once your USDC converts to USD buying power, you can:

* Trade equities and ETFs
* Trade other crypto pairs

In order to check your USD buying power, you can call [Retrieve Trading Details for an Account](https://docs.alpaca.markets/reference/gettradingaccount-1) API endpoint, and look for `buying_power`.

***

## **Withdrawing Crypto Assets**

### **Overview**

Withdrawing cryptocurrency from your Alpaca account requires a multi-step process to ensure fund safety:

1. **Whitelist** the destination address with travel rule information
2. **Verify** whitelist approval status
3. **Request** withdrawal to approved address
4. **Monitor** withdrawal status

### **Step 1: Whitelist Destination Address**

Before withdrawing, you must whitelist the destination wallet address with travel rule information. Depending on the  type of wallet you're sending funds to and the jurisdiction of the exchange it is hosted at, we may be required to collect more information. We have provided examples of methods you can use provide travel rule information. Any method can use either natural person or entity names. See the "Entity information" section below for more information.

[`POST v1/accounts/{account_id}/wallets/whitelists`](https://docs.alpaca.markets/reference/createwhitelistedaddress-1)

**Example 1: self hosted/non-custodial wallet**

Self-hosted in this context refers to a wallet that is not hosted by an exchange.

```json
{
  "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
  "asset": "USDC",
  "travel_rule_info": {
    "beneficiary_is_self_hosted": true,
    "beneficiary_given_name": "John",
    "beneficiary_family_name": "Doe"
  }
}
```

**Example 2: an exchange found via the search endpoint (preferred method)**

Please use our <Anchor target="_blank" href="https://docs.alpaca.markets/v1.4.2/reference/searchvasps-1">`Search for VASPs`</Anchor> endpoint to find the VASP DID for the exchange that your wallet address belongs to. *The VASP DID listed below is for our U.S. exchange.*

```json
{
  "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
  "asset": "USDC",
  "travel_rule_info": {
    "beneficiary_vasp_id": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
    "beneficiary_given_name": "John",
    "beneficiary_family_name": "Doe"
  }
}
```

**Example 3: an unlisted exchange**

If your exchange cannot be found via the Search for VASPs endpoint, you may supply information about the exchange manually.

```json
{
  "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
  "asset": "USDC",
  "travel_rule_info": {
    "beneficiary_manual_entry": {
        "vasp_name": "The Unlisted Exchange",
        "vasp_website": "https://unlisted.exchange"
    },
    "beneficiary_given_name": "John",
    "beneficiary_family_name": "Doe"
  }
}
```

**Entity information**

You may fill in the `beneficiary_entity_name` if your beneficiary is an entity. Note that you *cannot* submit both `beneficiary_given_name` and `beneficiary_family_name` in addition to the entity name. You must pick either of the options.

Failure to provide correct beneficiary information can lead to your withdrawal getting rejected by your counterparty exchange (if applicable). Please see the request payload below for whitelisting a wallet address with entity information and a VASP ID found via the <Anchor target="_blank" href="https://docs.alpaca.markets/v1.4.2/reference/searchvasps-1">`Search for VASPs`</Anchor> endpoint. You may also provide entity information with examples 1 and 3 from earlier, replacing the natural person with your entity's name.

```json
{
  "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
  "asset": "USDC",
  "travel_rule_info": {
    "beneficiary_vasp_id": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
    "beneficiary_entity_name": "Alpaca Crypto LLC"
  }
}
```

**Success response:**

```json
[
    {
        "id": "45efdedd-28cd-4665-98b4-601d5f34ae0a",
        "chain": "ETH",
        "asset": "USDC",
        "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
        "created_at": "2025-08-07T13:16:46.49111Z",
      	"status": "PENDING",
      	"travel_rule_info": {
            "beneficiary_vasp_id": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
            "beneficiary_entity_name": "Alpaca Crypto LLC"
        }
    }
]
```

**Error response -&#x20;**`BENEFICIARY_NAME_REQUIRED`**:**

This error will be returned if you've either not provided a natural person or entity name for your beneficiary, or you've included both. Please pick only one option as per the `ONE_OF` requirement.

```json
{
    "error_code": "BENEFICIARY_NAME_REQUIRED",
    "message": "Please provide the beneficiary's name. Select one of the following options.",
    "next_actions": [
        {
            "name": "supply_beneficiaryName_naturalPerson",
            "description": "Provide the recipient's first and last name.",
            "type": "ONE_OF",
            "required_fields": [
                {
                    "field": "beneficiary_given_name",
                    "value_type": "string",
                    "description": "The recipient's first name."
                },
                {
                    "field": "beneficiary_family_name",
                    "value_type": "string",
                    "description": "The recipient's last name."
                }
            ]
        },
        {
            "name": "supply_beneficiaryName_legalEntity",
            "description": "Provide the entity's legal name.",
            "type": "ONE_OF",
            "required_fields": [
                {
                    "field": "beneficiary_entity_name",
                    "value_type": "string",
                    "description": "The legal name of the receiving entity."
                }
            ]
        }
    ]
}
```

**Error response -&#x20;**`TRAVEL_RULE_ACTION_REQUIRED`**:**

This error will be returned if we're missing information from your travel rule information payload. This specific error payload will be sent if you're withdrawing funds to a Canadian exchange, but can also be shown in other scenarios with other `next_actions`.

```json
{
  "error_code": "TRAVEL_RULE_ACTION_REQUIRED",
  "message": "We require more information to whitelist this wallet address. Please provide the requested information.",
  "next_actions": [
    {
      "name": "supply_beneficiaryGeographicAddress",
      "description": "The receiver's geographic address.",
      "type": "REQUIRED",
      "required_fields": [
        {
          "field": "beneficiary_geographic_address_street_name",
          "value_type": "string",
          "description": "The receiver's street name.",
        },
        {
          "field": "beneficiary_geographic_address_post_code",
          "value_type": "string",
          "description": "The receiver's post code.",
        },
        {
          "field": "beneficiary_geographic_address_town_name",
          "value_type": "string",
          "description": "The receiver's town name.",
        },
        {
          "field": "beneficiary_geographic_address_country",
          "value_type": "string",
          "description": "The receiver's country as an ISO 3166 Alpha-2 string (two letters only).",
        },
        {
          "field": "beneficiary_geographic_address_building_number",
          "value_type": "string",
          "description": "The receiver's building number. Use 'UNKNOWN' if you are unsure.",
        }
      ]
    }
  ]
}
```

**Error response -&#x20;**`UNKNOWN_VASP`**:**

This error will be returned if we couldn't find the VASP ID you provided or if your manual entry matched with multiple VASP IDs. This can happen if your beneficiary's exchange has multiple entities.

```json
{
    "error_code": "UNKNOWN_VASP",
    "message": "We are unable to find the requested VASP.",
    "next_actions": [
        {
            "name": "select_vasp",
            "type": "REQUIRED",
            "description": "Select the beneficiary's VASP from our directory. Use the '/v1/wallets/travel-rule/vasps' endpoint to search. Submit the chosen 'id' in the 'travel_rule_info.beneficiary_vasp_id' field.",
            "required_fields": [
                {
                    "field": "beneficiary_vasp_id",
                    "value_type": "string",
                    "description": "The beneficiary's VASP ID.",
                }
            ]
        }
    ]
}
```

**Error response -&#x20;**`ADDRESS_BELONGS_TO_VASP`**:**

This error will be returned if you declared an known exchange wallet as self-hosted. In order to fix the error, you must  use the details provided in your travel rule information declaration.

```json
{
  "error_code": "ADDRESS_BELONGS_TO_VASP",
  "message": "We have detected that the address you specified belongs to Alpaca (US) (did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4)",
  "next_actions": [
    {
      "name": "remove_self_hosted_declaration",
      "type": "REQUIRED",
      "description": "You must remove the `self-hosted` declaration.",
      "required_fields": [
        {
          "field": "beneficiary_is_self_hosted",
          "value_type": "bool",
          "description": "True if the destination is a self-hosted (unhosted).",
          "options": [
            {
              "value": "false",
              "description": "The destination is not a self-hosted wallet."
            }
          ]
        }
      ]
    },
    {
      "name": "set_beneficiary_vasp_did",
      "type": "REQUIRED",
      "description": "You must set `beneficiary_vasp_id` as displayed below.",
      "required_fields": [
        {
          "field": "beneficiary_vasp_id",
          "value_type": "string",
          "description": "The detected beneficiary's VASP ID.",
          "options": [
            {
              "value": "did:ethr:0xf1c002f9e7ca88018d6dcf1e86403fb2f5f055f4",
              "description": "The beneficiary's VASP ID"
            }
          ]
        }
      ]
    }
  ]
}
```

### **Step 2: Check Whitelist Approval Status**

Monitor your whitelisted addresses to confirm approval (within 24 hours):

[`GET v1/accounts/{account_id}/wallets/whitelists`](https://docs.alpaca.markets/reference/listwhitelistedaddress-1)

**Response:**

```json
[
    {
        "id": "45efdedd-28cd-4665-98b4-601d5f34ae0a",
        "chain": "ETH",
        "asset": "USDC",
        "address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
        "created_at": "2025-08-07T13:16:46.49111Z",
        "status": "APPROVED"
    }
]

```

### **Step 3: Request Withdrawal**

Once approved, create a withdrawal transfer:

[`POST /v1/accounts/{account_id}/wallets/transfers`](https://docs.alpaca.markets/reference/createcryptotransferforaccount-1)

**Request Body:**

```json
{
 "amount": "55",
 "address": "34c18dbe-0983-4e61-b493-9578714dae23",
 "asset": "USDC"
}
```

**Response:**

```json
{
    "id": "f8fe06fe-702e-4d79-802c-f31cb1677f7c",
    "tx_hash": null,
    "direction": "OUTGOING",
    "amount": "55",
    "usd_value": "54.9725",
    "chain": "ETH",
    "asset": "USDC",
    "from_address": "0xA0D2C7210D7e2112A4F7888B8658CB579226dB3B",
    "to_address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
    "status": "PROCESSING",
    "created_at": "2025-09-19T08:37:25.436307Z",
    "network_fee": "20",
    "fees": "0.3025"
}

```

### **Step 4: Monitor Withdrawal Status**

Track your withdrawal progress:

#### Option 1: Poll transfers API

[`GET /v1/accounts/{account_id}/wallets/transfers`](https://docs.alpaca.markets/reference/listcryptofundingtransfers-1)

**Response:**

```json
[ {
        "id": "f8fe06fe-702e-4d79-802c-f31cb1677f7c",
        "tx_hash": null,
        "direction": "OUTGOING",
        "amount": "55",
        "usd_value": "54.9725",
        "chain": "ETH",
        "asset": "USDC",
        "from_address": "0xA0D2C7210D7e2112A4F7888B8658CB579226dB3B",
        "to_address": "0xf38Ecf5764fD2dEcB0dd9C1E7513a0b6eC0dD08a",
        "status": "PROCESSING",
        "created_at": "2025-09-19T08:37:25.436307Z",
        "network_fee": "0",
        "fees": "0.3025"
    }
]

```

#### Option 2: [NTA SSE event](https://docs.alpaca.markets/reference/get-v1-events-nta)

Sample event showing outgoing withdrawals:

```json
{
    "id": "a554262e-71dc-4a02-a0c0-271bcb9480e4",
    "qty": -54.6975,
    "cusip": "USDC12345",
    "status": "executed",
    "symbol": "USDCUSD",
    "entry_type": "OCT",
    "net_amount": 0,
    "description": "Withdrawal Transaction, transfer_id: f8fe06fe-702e-4d79-802c-f31cb1677f7c, tx_hash: 0xceaf451d26a11aa43681e6f9336987325b6c1c347d64f59b45811050d8789a24",
    "settle_date": "2025-09-19",
    "system_date": "2025-09-19",
    "price": "0.9995",
    "per_share_amount": null,
    "account_id": "34c18dbe-0983-4e61-b493-9578714dae23",
    "at": "2025-09-19T08:46:59.821881Z",
    "event_ulid": "01K5GJFGQDE4WQME5F38ZTXSTS"
}

```

You can also expect to see `CFEE` depending on your correspondent configuration linked to the withdrawal transactions.

```json
{
    "id": "5abfdea7-de14-4985-8632-428e8ffb7aa5",
    "qty": 1.3475,
    "cusip": "USDC12345",
    "status": "executed",
    "symbol": "USDCUSD",
    "entry_type": "CFEE",
    "net_amount": 0,
    "description": "Wallet Correspondent Transaction Fee, transfer_id: f8fe06fe-702e-4d79-802c-f31cb1677f7c, tx_hash: 0xceaf451d26a11aa43681e6f9336987325b6c1c347d64f59b45811050d8789a24",
    "settle_date": "2025-09-19",
    "system_date": "2025-09-19",
    "price": "0.9995",
    "per_share_amount": null,
    "account_id": "34c18dbe-0983-4e61-b493-9578714dae23",
    "at": "2025-09-19T08:46:59.819319Z",
    "event_ulid": "01K5GJFGQBCWVHV4YDV13QW68V"
}

{
    "id": "106a8e17-af4f-4dd1-a0a7-463ea035cb12",
    "qty": -0.275,
    "cusip": "USDC12345",
    "status": "executed",
    "symbol": "USDCUSD",
    "entry_type": "CFEE",
    "net_amount": 0,
    "description": "Wallet Transaction Fee, transfer_id: f8fe06fe-702e-4d79-802c-f31cb1677f7c, tx_hash: 0xceaf451d26a11aa43681e6f9336987325b6c1c347d64f59b45811050d8789a24",
    "settle_date": "2025-09-19",
    "system_date": "2025-09-19",
    "price": "0.9995",
    "per_share_amount": null,
    "account_id": "34c18dbe-0983-4e61-b493-9578714dae23",
    "at": "2025-09-19T08:46:59.821196Z",
    "event_ulid": "01K5GJFGQDDT69PTT6K37N1CQN"
}

{
    "id": "472f9c57-22b7-41a0-82b2-396e51fb99cf",
    "qty": -1.375,
    "cusip": "USDC12345",
    "status": "executed",
    "symbol": "USDCUSD",
    "entry_type": "CFEE",
    "net_amount": 0,
    "description": "Wallet Correspondent Transaction Income, transfer_id: f8fe06fe-702e-4d79-802c-f31cb1677f7c, tx_hash: 0xceaf451d26a11aa43681e6f9336987325b6c1c347d64f59b45811050d8789a24",
    "settle_date": "2025-09-19",
    "system_date": "2025-09-19",
    "price": "0.9995",
    "per_share_amount": null,
    "account_id": "34c18dbe-0983-4e61-b493-9578714dae23",
    "at": "2025-09-19T08:46:59.821937Z",
    "event_ulid": "01K5GJFGQDE5RGMVCJBDS42K0P"
}

```