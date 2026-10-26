# Working with /assets

Source: https://docs.alpaca.markets/us/docs/working-with-assets.md

---
updatedAt: 2026-08-18T22:29:46.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Working with /assets

Learn how to use the `/assets` endpoint to learn more about assets available on Alpaca. Both Securities and Crypto can be retrieved from the `/assets` endpoint.

# Get a List of Assets

If you send a `GET` request to our `/v2/assets` endpoint, you’ll receive a list of US equities.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

trading_client = TradingClient('api-key', 'secret-key')

# search for US equities
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

assets = trading_client.get_all_assets(search_params)
```
```javascript JavaScript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Get a list of all active assets.
const activeAssets = alpaca
  .getAssets({
    status: "active",
  })
  .then((activeAssets) => {
    // Filter the assets down to just those on NASDAQ.
    const nasdaqAssets = activeAssets.filter(
      (asset) => asset.exchange == "NASDAQ"
    );
    console.log(nasdaqAssets);
  });
```
```csharp C#
using Alpaca.Markets;
using System;
using System.Linq;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var assets = await client.ListAssetsAsync(
    new AssetsRequest { AssetStatus = AssetStatus.Active });
var nasdaqAssets = assets.Where(asset => asset.Exchange == Exchange.Nasdaq);

foreach (var asset in nasdaqAssets)
{
    Console.WriteLine($"{asset.Symbol}: {asset.Name}");
}
```
```go Go
package main

import (
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Get a list of all active assets.
	status := "active"
	assets, err := alpaca.ListAssets(&status)
	if err != nil {
		panic(err)
	}

	// Filter the assets down to just those on NASDAQ.
	nasdaq_assets := []alpaca.Asset{}
	for _, asset := range assets {
		if asset.Exchange == "NASDAQ" {
			nasdaq_assets = append(nasdaq_assets, asset)
		}
	}
}
```

# See If a Particular Asset is Tradable on Alpaca

By sending a symbol along with our request, we can get the information about just one asset. This is useful if we just want to make sure that a particular asset is tradable before we attempt to buy it.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

trading_client = TradingClient('api-key', 'secret-key')

# search for AAPL
aapl_asset = trading_client.get_asset('AAPL')

if aapl_asset.tradable:
    print('We can trade AAPL.')
```
```javascript JavaScript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Check if AAPL is tradable on the Alpaca platform.
alpaca.getAsset("AAPL").then((aaplAsset) => {
  if (aaplAsset.tradable) {
    console.log("We can trade AAPL.");
  }
});
```
```csharp C#
using Alpaca.Markets;
using System;
using System.Net;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

try
{
    var asset = await client.GetAssetAsync("AAPL");
    Console.WriteLine(
        asset.IsTradable
            ? "We can trade AAPL."
            : "AAPL is not currently tradable.");
}
catch (RestClientErrorException exception)
    when (exception.HttpStatusCode == HttpStatusCode.NotFound)
{
    Console.WriteLine("Asset not found for AAPL.");
}
```
```go Go
package main

import (
	"fmt"
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Check if AAPL is tradable on the Alpaca platform.
	asset, err := alpaca.GetAsset("AAPL")
	if err != nil {
		fmt.Println("Asset not found for AAPL.")
	} else if asset.Tradable {
		fmt.Println("We can trade AAPL.")
	}
}
```