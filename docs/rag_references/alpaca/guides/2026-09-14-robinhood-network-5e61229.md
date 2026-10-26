# New "robinhood" value on the tokenization network enum

Source: https://docs.alpaca.markets/us/changelog/2026-09-14-robinhood-network-5e61229.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# New "robinhood" value on the tokenization network enum

`robinhood` has been added to the `TokenizationNetwork` enum. Tokenization requests can now be submitted for and returned with this network.

## Broker API

* `GET /v1/accounts/{account_id}/tokenization/requests`
* `GET /v1/accounts/{account_id}/tokenization/requests/{tokenization_request_id}`
* `GET /v1/accounts/{account_id}/tokenization/requests:by_client_request_id`
* `GET /v1/accounts/{account_id}/tokenization/requests:by_issuer_request_id`
* `POST /v1/accounts/{account_id}/tokenization/mint`
* `POST /v1/accounts/{account_id}/tokenization/callback/mint`
* `POST /v1/accounts/{account_id}/tokenization/callback/redeem`

## Trading API

* `GET /v2/tokenization/requests`
* `GET /v2/tokenization/requests/{tokenization_request_id}`
* `GET /v2/tokenization/requests:by_client_request_id`
* `POST /v2/tokenization/mint`