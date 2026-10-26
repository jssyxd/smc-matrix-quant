# New "total_amount" field on funding wallet transfers

Source: https://docs.alpaca.markets/us/changelog/2026-09-21-total-amount-e615dcb.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# New "total_amount" field on funding wallet transfers

## Broker API

Adds the `total_amount` field to the `FundingWalletTransfer` schema.

* For outgoing transfers, `total_amount` is the total amount debited from the account (requested amount plus fees).
* For incoming transfers, `total_amount` is the requested amount.
* The `original_amount` field is deprecated and will be removed on 2026-12-21. Use `total_amount` for the actual amount debited from the account.

### Affected Endpoints

* `POST /v1beta/accounts/{account_id}/funding_wallet/withdrawal`
* `GET /v1beta/accounts/{account_id}/funding_wallet/transfers/{transfer_id}`
* `GET /v1beta/accounts/{account_id}/funding_wallet/transfers`