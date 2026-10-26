# JNLC upgrade

Source: https://docs.alpaca.markets/us/changelog/jnlc-v2-upgrade.md

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# JNLC upgrade

## This is a reminder that we will be upgrading all partners to JNLC v2 on September 21, 2026.

<br />

As shared previously, this does not involve any change to the API endpoints that you have been using. However, there will be some changes to the JNLC status flow, including a new status (`activity_created`, which will come after the `executed` status), so please ensure that your systems handle unknown statuses.<br />

There is no action needed to respond to this new status. The buying power update will still occur when the journal reaches the existing `executed` status.

<br />

Please review the updated journal status flow in our <Anchor target="_blank" href="https://docs.alpaca.markets/us/docs/funding-via-journals">documentation</Anchor> and reach out to your customer success manager with any questions, or to request an extension.

<br />

The Alpaca Team

Cheers,

<Image src="https://files.readme.io/b03b8a9abfe98d705f2ac7ba3311f92fd08827f5d476332029aa73d8420c6176-alpaca-logo.png" width="10%" />