# Identity schema corrected for income bounds and "tax_id_type"

Source: https://docs.alpaca.markets/us/changelog/2026-09-17-identity-schema-9f16422.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Identity schema corrected for income bounds and "tax_id_type"

## Broker API

The `Identity` schema now matches what the API actually returns:

* `annual_income_min`, `annual_income_max`, `liquid_net_worth_min`, `liquid_net_worth_max`, `total_net_worth_min`, and `total_net_worth_max` are documented as decimal strings (`type: string`, `format: decimal`), consistent with other monetary fields such as `cash` and `buying_power`. Examples have been added for each.
* `tax_id_type` is no longer unconditionally required and may be `null` on read. It is required on write only when `tax_id` is supplied; some accounts return identity data without it.

### Affected Endpoints

* `GET /v1/accounts`
* `POST /v1/accounts`
* `GET /v1/accounts/{account_id}`
* `PATCH /v1/accounts/{account_id}`