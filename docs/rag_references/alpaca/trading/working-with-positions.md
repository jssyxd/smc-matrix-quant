# Working with /positions

Source: https://docs.alpaca.markets/us/docs/working-with-positions.md

---
updatedAt: 2026-08-18T22:29:55.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Working with /positions

You can view the positions in your portfolio by making a `GET` request to the `/v2/positions` endpoint. If you specify a symbol, you’ll see only your position for the associated stock.

```python
from alpaca.trading.client import TradingClient

trading_client = TradingClient('api-key', 'secret-key')

# Get our position in AAPL.
aapl_position = trading_client.get_open_position('AAPL')

# Get a list of all of our positions.
portfolio = trading_client.get_all_positions()

# Print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
```
```javascript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Get our position in AAPL.
aaplPosition = alpaca.getPosition("AAPL");

// Get a list of all of our positions.
alpaca.getPositions().then((portfolio) => {
  // Print the quantity of shares for each position.
  portfolio.forEach(function (position) {
    console.log(`${position.qty} shares of ${position.symbol}`);
  });
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
    var aaplPosition = await client.GetPositionAsync("AAPL");
    Console.WriteLine($"AAPL position: {aaplPosition.Quantity} shares.");
}
catch (RestClientErrorException exception)
    when (exception.HttpStatusCode == HttpStatusCode.NotFound)
{
    Console.WriteLine("No open AAPL position.");
}

var positions = await client.ListPositionsAsync();
foreach (var position in positions)
{
    Console.WriteLine($"{position.Quantity} shares of {position.Symbol}.");
}
```
```go
package main

import (
	"fmt"
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Get our position in AAPL.
	aapl_position, err := alpaca.GetPosition("AAPL")
	if err != nil {
		fmt.Println("No AAPL position.")
	} else {
		fmt.Printf("AAPL position: %v shares.\n", aapl_position.Qty)
	}

	// Get a list of all of our positions.
	positions, err := alpaca.ListPositions()
	if err != nil {
		fmt.Println("No positions found.")
	} else {
		// Print the quantity of shares for each position.
		for _, position := range positions {
			fmt.Printf("%v shares in %s", position.Qty, position.Symbol)
		}
	}
}
```

The current price reflected will be based on the following:

**4:00 am ET - 9:30 am ET** - Last trade based on the premarket

**9:30 am ET - 4pm ET** - Last trade

**4:00 pm ET - 10:00 pm ET** - Last trade based on after-hours trading

**10 pm ET - 4:00 am ET next trading day** - Official closing price from the primary exchange at 4 pm ET.