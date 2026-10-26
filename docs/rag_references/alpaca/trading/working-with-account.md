# Working with /account

Source: https://docs.alpaca.markets/us/docs/working-with-account.md

---
updatedAt: 2026-08-18T22:31:04.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Working with /account

Learn how to use the /account endpoint to learn about the state of your account

# View Account Information

By sending a `GET` request to our `/v2/account` endpoint, you can see various information about your account, such as the amount of buying power available.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

trading_client = TradingClient('api-key', 'secret-key')

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))
```
```javascript JavaScript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Get our account information.
alpaca.getAccount().then((account) => {
  // Check if our account is restricted from trading.
  if (account.trading_blocked) {
    console.log("Account is currently restricted from trading.");
  }

  // Check how much money we can use to open new positions.
  console.log(`$${account.buying_power} is available as buying power.`);
});
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var account = await client.GetAccountAsync();
if (account.IsTradingBlocked)
{
    Console.WriteLine("Account is currently restricted from trading.");
}

Console.WriteLine($"{account.BuyingPower} is available as buying power.");
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
	// Get our account information.
	account, err := alpaca.GetAccount()
	if err != nil {
		panic(err)
	}

	// Check if our account is restricted from trading.
	if account.TradingBlocked {
		fmt.Println("Account is currently restricted from trading.")
	}

	// Check how much money we can use to open new positions.
	fmt.Printf("%v is available as buying power.\n", account.BuyingPower)
}
```

# View Gain/Loss of Portfolio

You can use the information from the account endpoint to do things like calculating the daily profit or loss of your account.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

trading_client = TradingClient('api-key', 'secret-key')

# Get our account information.
account = trading_client.get_account()

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')
```
```javascript JavaScript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Get account information.
alpaca.getAccount().then((account) => {
  // Calculate the difference between current balance and balance at the last market close.
  const balanceChange = account.equity - account.last_equity;

  console.log("Today's portfolio balance change:", balanceChange);
});
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var account = await client.GetAccountAsync();
var balanceChange = account.Equity - account.LastEquity;
Console.WriteLine($"Today's portfolio balance change: {balanceChange}");
```
```go Go
package main

import (
	"fmt"
	"log"

	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
)

func main() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")

	// Get account information.
	account, err := alpaca.GetAccount()
	if err != nil {
		log.Fatalln(err)
	}

	// Calculate the difference between current balance and balance at the last market close.
	balanceChange := account.Equity.Sub(account.LastEquity)

	fmt.Println("Today's portfolio balance change:", balanceChange)
}
```