# Account Status Events for KYCaaS

Source: https://docs.alpaca.markets/us/docs/account-status-events-for-kycaas.md

---
updatedAt: 2026-08-20T19:34:32.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Account Status Events for KYCaaS

Partners using Alpaca's KYC service can receive account status changes in real time through [Account Status Events](https://docs.alpaca.markets/us/reference/suscribetoaccountstatussse). An account moving to `ACTION_REQUIRED` or `APPROVAL_PENDING` may require additional review, information, or documentation before it can be opened.

## KYC result payload

Account status events include only properties that changed, so `kyc_results` may be omitted when the event is unrelated to KYC. When present, `kyc_results` or any of its result categories may be `null`.

The `accept`, `indeterminate`, and `reject` fields are sets represented as JSON objects. Each property name is a KYC reason identifier, and its value is always an empty object (`{}`) carrying no additional data:

```json
{
  "account_id": "4db36989-6565-4011-9126-39fe6b3d9bf6",
  "status_to": "ACTION_REQUIRED",
  "kyc_results": {
    "accept": {},
    "indeterminate": {
      "IDENTITY_VERIFICATION": {}
    },
    "reject": null,
    "additional_information": "Please provide a valid government-issued identity document.",
    "summary": "fail"
  }
}
```

Read the reason identifier from the property name, not from the empty object value. Interpret each reason together with its enclosing result category and `additional_information`. The set of identifiers is extensible, so integrations must tolerate and preserve identifiers that are not listed below.

## Result categories

| Category        | Meaning                                                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `accept`        | No action is needed for the reason unless Alpaca separately requests it.                                                            |
| `indeterminate` | Additional review, information, or documentation may be required before the account can be opened.                                  |
| `reject`        | The KYC result was rejected. Some reasons may not be remediable; follow `additional_information` or other instructions from Alpaca. |

The enclosing category determines the required response. For example, a reason in `accept` does not require action even if the same reason would require information when returned in `indeterminate`.

## Documentation requirements

When one of these reasons appears in `indeterminate` or `reject`, use `additional_information` to confirm the exact request before collecting or submitting documents.

| KYC reason identifier   | Government-issued ID | Tax ID document | Statement, such as a utility bill | Live selfie |
| ----------------------- | -------------------- | --------------- | --------------------------------- | ----------- |
| `IDENTITY_VERIFICATION` | Required             |                 |                                   |             |
| `TAX_IDENTIFICATION`    |                      | Required        |                                   |             |
| `ADDRESS_VERIFICATION`  | May be requested     |                 | May be requested                  |             |
| `DATE_OF_BIRTH`         | Required             |                 |                                   |             |
| `SELFIE_VERIFICATION`   |                      |                 |                                   | Required    |

## Additional information requirements

| KYC reason identifier | Additional information that may be required             |
| --------------------- | ------------------------------------------------------- |
| `PEP`                 | Job title, occupation, and address                      |
| `FAMILY_MEMBER_PEP`   | Name of the politically exposed immediate family member |
| `CONTROL_PERSON`      | Company name, address, and email                        |
| `AFFILIATED`          | Firm name, address, and email                           |
| `VISA_TYPE_OTHER`     | Visa type and expiration date                           |
| `W8BEN_CORRECTION`    | An updated W-8BEN with corrected information            |
| `OTHER`               | The information requested in `additional_information`   |

For the full, evolving list of documented KYC reason identifiers and their meanings, see the [Account Status Events API reference](https://docs.alpaca.markets/us/reference/suscribetoaccountstatussse).