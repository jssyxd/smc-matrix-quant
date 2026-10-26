# CUSIP length constraints corrected on fixed income assets

Source: https://docs.alpaca.markets/us/changelog/2026-09-23-cusip-length-ff53e0d.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# CUSIP length constraints corrected on fixed income assets

## Broker API

The `cusip` field on the `us_treasury` and `us_corporate` schemas now has `minLength` and `maxLength` of 9, matching its documented nine-character CUSIP format and `^[A-Z0-9]{9}$` pattern. Previously the length bounds were 12, so no value could satisfy both the pattern and the length check.

* `cusip` on `us_treasury` and `us_corporate`: length is now 9.
* The sibling `isin` fields keep their 12-character constraints.

Generated clients and validators can now accept the nine-character CUSIP values the API actually returns.

### Affected Endpoints

* `GET /v1/assets/fixed_income/us_treasuries`
* `GET /v1/assets/fixed_income/us_corporates`