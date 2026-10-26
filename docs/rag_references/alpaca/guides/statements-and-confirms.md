# Statements and Confirms

Source: https://docs.alpaca.markets/us/docs/statements-and-confirms.md

---
updatedAt: 2026-02-19T07:18:59.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Statements and Confirms

# Requirements

Under the FINRA and SEC rules, Alpaca is required to ensure the customer statements and trade confirms are delivered correctly in time to the end customers. That being said, the actual communication and delivery do not have to be done by Alpaca directly. Very often, you want to own the full user experiences and to be responsible for these communications, which is totally possible.

# Document API Integration

You can retrieve the generated reports in PDF format through the [Documents API](https://docs.alpaca.markets/reference/downloaddocfromaccount). You can store the files on your storage if it is required for your regulation purpose, or you can let your customers download the files using the URL returned in the API response. If you are a fully-disclosed broker-dealer, you can insert your firm logo, name and address in the PDF template. Please send those data to Alpaca.

If you need even more customization on the template, we are currently working on the new API endpoint which will return only the data points so that you can build fully-customized documents with your own template. Alpaca still needs to review your final version of customized documents before delivering to the end customers for the first time.