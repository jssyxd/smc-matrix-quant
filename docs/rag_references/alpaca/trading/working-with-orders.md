# Working with /orders

Source: https://docs.alpaca.markets/us/docs/working-with-orders.md

---
updatedAt: 2026-08-18T22:29:50.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Working with /orders

Learn how to submit orders to Alpaca.

This page contains examples of some of the things you can do with order objects through our API. For additional help understanding different types of orders and how they behave once they’re placed, please check out the Orders on Alpaca page.

# Place New Orders

Orders can be placed with a `POST` request to our `/v2/orders` endpoint.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('api-key', 'secret-key', paper=True)

# preparing market order
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=0.023,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

# preparing limit order
limit_order_data = LimitOrderRequest(
                    symbol="BTC/USD",
                    limit_price=17000,
                    notional=4000,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.FOK
                   )

# Limit order
limit_order = trading_client.submit_order(
                order_data=limit_order_data
              )
```
```javascript JavaScript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Submit a market order to buy 1 share of Apple at market price
alpaca.createOrder({
  symbol: "AAPL",
  qty: 1,
  side: "buy",
  type: "market",
  time_in_force: "day",
});

// Submit a limit order to attempt to sell 1 share of AMD at a
// particular price ($20.50) when the market opens
alpaca.createOrder({
  symbol: "AMD",
  qty: 1,
  side: "sell",
  type: "limit",
  time_in_force: "opg",
  limit_price: 20.5,
});
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var marketOrder = await client.PostOrderAsync(MarketOrder.Buy("AAPL", 1));
Console.WriteLine($"Market order {marketOrder.OrderId}: {marketOrder.OrderStatus}");

var limitOrder = await client.PostOrderAsync(
    LimitOrder.Sell("AMD", 1, 20.50M).WithDuration(TimeInForce.Opg));
Console.WriteLine($"Limit order {limitOrder.OrderId}: {limitOrder.OrderStatus}");
```
```go Go
package main

import (
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
	"github.com/shopspring/decimal"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Submit a market order to buy 1 share of Apple at market price
	symbol := "AAPL"
	alpaca.PlaceOrder(alpaca.PlaceOrderRequest{
		AssetKey: &symbol,
		Qty: decimal.NewFromFloat(1),
		Side: alpaca.Buy,
		Type: alpaca.Market,
		TimeInForce: alpaca.Day,
	})

	// Submit a limit order to attempt to sell 1 share of AMD at a
	// particular price ($20.50) when the market opens
	symbol = "AMD"
	alpaca.PlaceOrder(alpaca.PlaceOrderRequest{
		AssetKey: &symbol,
		Qty: decimal.NewFromFloat(1),
		Side: alpaca.Sell,
		Type: alpaca.Limit,
		TimeInForce: alpaca.OPG,
		LimitPrice: decimal.NewFromFloat(20.50),
	})
}
```

# Submit Shorts

Short orders can also be placed for securities which you do not hold an open long position in.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('api-key', 'secret-key', paper=True)

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var order = await client.PostOrderAsync(MarketOrder.Sell("TSLA", 1));
Console.WriteLine($"Short order {order.OrderId}: {order.OrderStatus}");
```

# Using Client Order IDs

`client_order_id` can be used to organize and track specific orders in your client program. Unique `client_order_ids` for different strategies is a good way of running parallel algos across the same account.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('api-key', 'secret-key', paper=True)

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=0.023,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    client_order_id='my_first_order',
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

# Get our order using its Client Order ID.
my_order = trading_client.get_order_by_client_id('my_first_order')
print('Got order #{}'.format(my_order.id))
```
```javascript
const Alpaca = require('@alpacahq/alpaca-trade-api')
const alpaca = new Alpaca()

// Submit a market order and assign it a Client Order ID.
alpaca.createOrder({
    symbol: 'AAPL',
    qty: 1,
    side: 'buy',
    type: 'market',
    time_in_force: 'day',
    client_order_id='my_first_order'
})

// Get our order using its Client Order ID.
alpaca.getOrderByClientOrderId('my_first_order')
    .then((myOrder) => {
        console.log(`Got order #${myOrder.id}.`)
    })
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

const string clientOrderId = "my_first_order";
var submitted = await client.PostOrderAsync(
    MarketOrder.Buy("AAPL", 1).WithClientOrderId(clientOrderId));
var retrieved = await client.GetOrderAsync(clientOrderId);

Console.WriteLine($"Submitted {submitted.OrderId}; retrieved {retrieved.OrderId}.");
```

# Submitting Bracket Orders

Bracket orders allow you to create a chain of orders that react to execution and stock price. For more details, go to Bracket Order Overview.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass

trading_client = TradingClient('api-key', 'secret-key', paper=True)

# preparing bracket order with both stop loss and take profit
bracket__order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=5,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price=400),
                    stop_loss=StopLossRequest(stop_price=300)
                    )

bracket_order = trading_client.submit_order(
                order_data=bracket__order_data
               )

# preparing oto order with stop loss
oto_order_data = LimitOrderRequest(
                    symbol="SPY",
                    qty=5,
                    limit_price=350,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.OTO,
                    stop_loss=StopLossRequest(stop_price=300)
                    )

# Market order
oto_order = trading_client.submit_order(
                order_data=oto_order_data
               )
```
```javascript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

const symbol = "AAPL";
alpaca
  .getBars("minute", symbol, {
    limit: 5,
  })
  .then((barset) => {
    const currentPrice = barset[symbol].slice(-1)[0].closePrice;

    // We could buy a position and add a stop-loss and a take-profit of 5 %
    alpaca.createOrder({
      symbol: symbol,
      qty: 1,
      side: "buy",
      type: "limit",
      time_in_force: "gtc",
      limit_price: currentPrice,
      order_class: "bracket",
      stop_loss: {
        stop_price: currentPrice * 0.95,
        limit_price: currentPrice * 0.94,
      },
      take_profit: {
        limit_price: currentPrice * 1.05,
      },
    });

    // We could buy a position and just add a stop loss of 5 % (OTO Orders)
    alpaca.createOrder({
      symbol: symbol,
      qty: 1,
      side: "buy",
      type: "limit",
      time_in_force: "gtc",
      limit_price: currentPrice,
      order_class: "oto",
      stop_loss: {
        stop_price: currentPrice * 0.95,
      },
    });

    // We could split it to 2 orders. first buy a stock,
    // and then add the stop/profit prices (OCO Orders)
    alpaca.createOrder({
      symbol: symbol,
      qty: 1,
      side: "buy",
      type: "limit",
      time_in_force: "gtc",
      limit_price: currentPrice,
    });

    // wait for it to buy position and then
    alpaca.createOrder({
      symbol: symbol,
      qty: 1,
      side: "sell",
      type: "limit",
      time_in_force: "gtc",
      limit_price: currentPrice,
      order_class: "oco",
      stop_loss: {
        stop_price: currentPrice * 0.95,
      },
      take_profit: {
        limit_price: currentPrice * 1.05,
      },
    });
  });
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var bracketOrder = await client.PostOrderAsync(
    LimitOrder.Buy("AAPL", 1, 150M)
        .WithDuration(TimeInForce.Gtc)
        .Bracket(160M, 140M));
Console.WriteLine($"Bracket order {bracketOrder.OrderId}: {bracketOrder.OrderStatus}");

var otoOrder = await client.PostOrderAsync(
    LimitOrder.Buy("AAPL", 1, 150M)
        .WithDuration(TimeInForce.Gtc)
        .StopLoss(140M));
Console.WriteLine($"OTO order {otoOrder.OrderId}: {otoOrder.OrderStatus}");

var ocoOrder = await client.PostOrderAsync(
    LimitOrder.Sell("AAPL", 1, 160M)
        .WithDuration(TimeInForce.Gtc)
        .OneCancelsOther(140M));
Console.WriteLine($"OCO order {ocoOrder.OrderId}: {ocoOrder.OrderStatus}");
```
```go
package main

import (
    "github.com/alpacahq/alpaca-trade-api-go/alpaca"
    "github.com/alpacahq/alpaca-trade-api-go/common"
    "github.com/shopspring/decimal"
)

func init() {
    API_KEY := "YOUR_API_KEY_HERE"
    API_SECRET := "YOUR_API_SECRET_HERE"
    BASE_URL := "https://paper-api.alpaca.markets"
    // Check for environment variables
    if common.Credentials().ID == "" {
        os.Setenv(common.EnvApiKeyID, API_KEY)
    }
    if common.Credentials().Secret == "" {
        os.Setenv(common.EnvApiSecretKey, API_SECRET)
    }
    alpaca.SetBaseUrl(BASE_URL)
}

func main() {
    // Submit a limit order to buy 1 share of Apple and add
    // StopLoss and TakeProfit orders.
    client := alpaca.NewClient(common.Credentials())
    symbol := "AAPL"
    tpp := decimal.NewFromFloat(320.)
    spp := decimal.NewFromFloat(317.)
    limit := decimal.NewFromFloat(318.)
    tp := &alpaca.TakeProfit{LimitPrice: &tpp}
    sl := &alpaca.StopLoss{
        LimitPrice: nil,
        StopPrice:  &spp,
    }
    req := alpaca.PlaceOrderRequest{
        AccountID:   common.Credentials().ID,
        AssetKey:    &symbol,
        Qty:         decimal.New(1, 0),
        Side:        alpaca.Buy,
        LimitPrice:  &limit,
        TimeInForce: alpaca.GTC,
        Type:        alpaca.Limit,
        OrderClass:  alpaca.Bracket,
        TakeProfit:  tp,
        StopLoss:    sl,
    }
    order, err := client.PlaceOrder(req)
    fmt.Println(order)
    fmt.Println(err)

    // We could buy a position and just add a stop loss (OTO Orders)
    spp := decimal.NewFromFloat(317.)
    limit := decimal.NewFromFloat(318.)
    sl := &alpaca.StopLoss{
        StopPrice:  &spp,
    }
    req := alpaca.PlaceOrderRequest{
        AccountID:   common.Credentials().ID,
        AssetKey:    &symbol,
        Qty:         decimal.New(1, 0),
        Side:        alpaca.Buy,
        LimitPrice:  &limit,
        TimeInForce: alpaca.GTC,
        Type:        alpaca.Limit,
        OrderClass:  alpaca.Oto,
        StopLoss:    sl,
    }
    order, err := client.PlaceOrder(req)
    fmt.Println(order)
    fmt.Println(err)

    // We could split it to 2 orders. first buy a stock,
    // and then add the stop/profit prices (OCO Orders)
    limit := decimal.NewFromFloat(318.)
    req := alpaca.PlaceOrderRequest{
        AccountID:   common.Credentials().ID,
        AssetKey:    &symbol,
        Qty:         decimal.New(1, 0),
        Side:        alpaca.Buy,
        LimitPrice:  &limit,
        TimeInForce: alpaca.GTC,
        Type:        alpaca.Limit,
        OrderClass:  alpaca.Simple,
    }
    order, err := client.PlaceOrder(req)
    fmt.Println(order)
    fmt.Println(err)

    // wait for it to complete and then
    tpp := decimal.NewFromFloat(320.)
    spp := decimal.NewFromFloat(317.)
    tp := &alpaca.TakeProfit{LimitPrice: &tpp}
    sl := &alpaca.StopLoss{
        LimitPrice: nil,
        StopPrice:  &spp,
    }
    req := alpaca.PlaceOrderRequest{
        AccountID:   common.Credentials().ID,
        AssetKey:    &symbol,
        Qty:         decimal.New(1, 0),
        Side:        alpaca.Sell,
        TimeInForce: alpaca.GTC,
        Type:        alpaca.Limit,
        OrderClass:  alpaca.Oco,
        TakeProfit:  tp,
        StopLoss:    sl,
    }
    order, err := client.PlaceOrder(req)
    fmt.Println(order)
    fmt.Println(err)
}
```

# Submitting Trailing Stop Orders

Trailing stop orders allow you to create a stop order that automatically changes the stop price allowing you to maximize your profits while still protecting your position with a stop price. For more details, go to Trailing Stop Order Overview.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('api-key', 'secret-key', paper=True)


trailing_percent_data = TrailingStopOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    trail_percent=1.00 # hwm * 0.99
                    )

trailing_percent_order = trading_client.submit_order(
                order_data=trailing_percent_data
               )


trailing_price_data = TrailingStopOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    trail_price=1.00 # hwm - $1.00
                    )

trailing_price_order = trading_client.submit_order(
                order_data=trailing_price_data
               )
```
```javascript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Submit a market order to buy 1 share of Apple at market price
alpaca.createOrder({
  symbol: "AAPL",
  qty: 1,
  side: "buy",
  type: "market",
  time_in_force: "day",
});

// Submit a trailing stop order to sell 1 share of Apple at a
// trailing stop of
alpaca.createOrder({
  symbol: "AAPL",
  qty: 1,
  side: "sell",
  type: "trailing_stop",
  trail_price: 1.0, // stop price will be hwm - 1.00$
  time_in_force: "day",
});

// Alternatively, you could use trail_percent:
alpaca.createOrder({
  symbol: "AAPL",
  qty: 1,
  side: "sell",
  type: "trailing_stop",
  trail_percent: 1.0, // stop price will be hwm*0.99
  time_in_force: "day",
});
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var order = await client.PostOrderAsync(
    OrderSide.Sell.TrailingStop("AAPL", 1, TrailOffset.InDollars(1.00M)));

Console.WriteLine($"Trailing stop {order.OrderId}: {order.OrderStatus}");
```
```go
package main

import (
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
	"github.com/shopspring/decimal"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Submit a market order to buy 1 share of Apple at market price
	symbol := "AAPL"
	alpaca.PlaceOrder(alpaca.PlaceOrderRequest{
		AssetKey: &symbol,
		Qty: decimal.NewFromFloat(1),
		Side: alpaca.Buy,
		Type: alpaca.Market,
		TimeInForce: alpaca.Day,
	})

	// Submit a trailing stop order to sell 1 share of Apple at a
    // trailing stop of
	symbol = "AAPL"
	alpaca.PlaceOrder(alpaca.PlaceOrderRequest{
		AssetKey: &symbol,
		Qty: decimal.NewFromFloat(1),
		Side: alpaca.Sell,
		Type: alpaca.TrailingStop,
		StopPrice: decimal.NewFromFloat(1.00),  // stop price will be hwm - 1.00$
		TimeInForce: alpaca.Day,
	})

	// Alternatively, you could use trail_percent:
	symbol = "AAPL"
	alpaca.PlaceOrder(alpaca.PlaceOrderRequest{
		AssetKey: &symbol,
		Qty: decimal.NewFromFloat(1),
		Side: alpaca.Sell,
		Type: alpaca.TrailingStop,
		TrailPercent: decimal.NewFromFloat(1.0),  // stop price will be hwm*0.99
		TimeInForce: alpaca.Day,
	})
}
```

# Retrieve All Orders

If you’d like to see a list of your existing orders, you can send a `GET` request to our `/v2/orders` endpoint.

```python Python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

trading_client = TradingClient('api-key', 'secret-key', paper=True)

# Get the last 100 closed orders
get_orders_data = GetOrdersRequest(
    status=QueryOrderStatus.CLOSED,
    limit=100,
    nested=True  # show nested multi-leg orders
)

trading_client.get_orders(filter=get_orders_data)
```
```javascript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Get the last 100 of our closed orders
const closedOrders = alpaca
  .getOrders({
    status: "closed",
    limit: 100,
    nested: true, // show nested multi-leg orders
  })
  .then((closedOrders) => {
    // Get only the closed orders for a particular stock
    const closedAaplOrders = closedOrders.filter(
      (order) => order.symbol == "AAPL"
    );
    console.log(closedAaplOrders);
  });
```
```csharp C#
using Alpaca.Markets;
using System;

var client = Environments.Paper.GetAlpacaTradingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

var closedOrders = await client.ListOrdersAsync(
    new ListOrdersRequest
    {
        LimitOrderNumber = 100,
        OrderStatusFilter = OrderStatusFilter.Closed,
        RollUpNestedOrders = true,
    });

foreach (var order in closedOrders)
{
    Console.WriteLine($"{order.OrderId}: {order.OrderStatus}");
}
```
```go
package main

import (
	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	// Get the last 100 of our closed orders
	status := "closed"
	limit := 100
	nested := true // show nested multi-leg orders
	closed_orders, err := alpaca.ListOrders(&status, nil, &limit, &nested)
	if err != nil {
		panic(err)
	}

	// Get only the closed orders for a particular stock
	var aaplOrders []alpaca.Order
	for _, order := range closed_orders {
		if order.Symbol == "AAPL" {
			aaplOrders = append(aaplOrders, order)
		}
	}
}
```

# Listen for Updates to Orders

You can use Websockets to receive real-time updates about the status of your orders as they change. You can see the full documentation here.

```python Python
from alpaca.trading.stream import TradingStream

stream = TradingStream('api-key', 'secret-key', paper=True)


@conn.on(client_order_id)
async def on_msg(data):
    # Print the update to the console.
    print("Update for {}. Event: {}.".format(data.event))

stream.subscribe_trade_updates(on_msg)
# Start listening for updates.
stream.run()
```
```javascript
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();

// Prepare the websocket connection and subscribe to trade_updates.
alpaca.websocket.onConnect(function () {
  console.log("Connected");
  client.subscribe(["trade_updates"]);
  setTimeout(() => {
    client.disconnect();
  }, 30 * 1000);
});
alpaca.websocket.onDisconnect(() => {
  console.log("Disconnected");
});
alpaca.websocket.onStateChange((newState) => {
  console.log(`State changed to ${newState}`);
});

// Handle updates on an order you've given a Client Order ID.
const client_order_id = "my_client_order_id";
alpaca.websocket.onOrderUpdate((orderData) => {
  const event = orderData["event"];
  if (orderData["order"]["client_order_id"] == client_order_id) {
    console.log(`Update for ${client_order_id}. Event: ${event}.`);
  }
});

// Start listening for updates.
alpaca.websocket.connect();
```
```csharp C#
using Alpaca.Markets;
using System;

const string clientOrderId = "my_client_order_id";
var streamingClient = Environments.Paper.GetAlpacaStreamingClient(
    new SecretKey("YOUR_API_KEY", "YOUR_API_SECRET"));

streamingClient.OnTradeUpdate += update =>
{
    if (update.Order.ClientOrderId == clientOrderId)
    {
        Console.WriteLine($"Update for {clientOrderId}: {update.Event}");
    }
};

var authStatus = await streamingClient.ConnectAndAuthenticateAsync();
Console.WriteLine($"{authStatus}. Press any key to stop listening.");
Console.ReadKey();
```
```go
package main

import (
	"fmt"

	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
    "github.com/alpacahq/alpaca-trade-api-go/stream"
)

func init() {
	alpaca.SetBaseUrl("https://paper-api.alpaca.markets")
}

func main() {
	if err := stream.Register(alpaca.TradeUpdates, tradeHandler); err != nil {
        panic(err)
    }
}

func tradeHandler(msg interface{}) {
	tradeupdate := msg.(alpaca.TradeUpdate)
	if tradeupdate.Order.ClientOrderID == "my_client_order_id" {
		fmt.Printf("Update for {}. Event: {}.\n", tradeupdate.Order.ClientOrderID, tradeupdate.Event)
	}
}
```

# FAQ

**What should I do if I receive a timeout message from Alpaca when submitting an order?**

The order may have been sent to the market for execution. You should not attempt to resend the order or mark the timed-out order as canceled until confirmed by Alpaca Support or the trading team. Before taking any action on the timed-out order you should check the broker dashboard and contact Alpaca support.\
Please contact our Support Team at <support@alpaca.markets> to verify if the order was successfully submitted and routed to the market.