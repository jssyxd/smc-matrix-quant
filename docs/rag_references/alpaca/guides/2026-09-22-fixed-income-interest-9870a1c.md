# New "interest_type", "order_id", and "parent_id" on fixed income interest activities

Source: https://docs.alpaca.markets/us/changelog/2026-09-22-fixed-income-interest-9870a1c.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# New "interest_type", "order_id", and "parent_id" on fixed income interest activities

Adds fields to the fixed income interest (INT/FI) activity schema so coupon and accrued interest can be distinguished and linked to their originating fill:

* A required `interest_type` field (`coupon` or `accrued`).
* Optional `order_id` and `parent_id` on trade-accrued interest so the interest activity can be linked to the fill.
* A new `FixedIncomeInterestType` enum.
* Documents the three variants: coupon, accrued-on-call, and trade accrued.

## Broker API

* `GET /v1/accounts/activities`
* `GET /v1/accounts/activities/{activity_type}`
* `GET /v2beta1/accounts/{account_id}/events/activities/{event_id}`
* `GET /v2beta1/events/activities`

## Trading API

* `GET /v2/account/activities`
* `GET /v2/account/activities/{activity_type}`
* `GET /v2beta1/events/activities`