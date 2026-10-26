# Rate Limits

Source: https://docs.alpaca.markets/us/docs/broker-api-rate-limits.md

---
updatedAt: 2026-07-11T15:53:23.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Rate Limits

Alpaca applies rate limits to the Broker API to protect the stability and fairness of the platform for every partner. This page explains how to detect where you stand, what happens if you exceed your limit, and how to build an integration that handles limits gracefully.

## How limits are applied

Broker API rate limits are applied at the **correspondent level** - that is, across your whole integration, not per end-user account. Every partner starts with a default limit, and limits can be tailored based on demonstrated, sustained usage. Because limits are set per partner and reviewed case by case, Alpaca does not publish fixed Broker API rate-limit numbers.

## Rate-limit headers (returned on every response)

Every Broker API response - **not only&#x20;**`429`**&#x20;responses** - includes headers that tell you exactly where you stand in the current window:

| Header                  | Meaning                                                    |
| ----------------------- | ---------------------------------------------------------- |
| `X-RateLimit-Limit`     | Total requests allowed in the current window               |
| `X-RateLimit-Remaining` | Requests still available in the current window             |
| `X-RateLimit-Reset`     | Unix timestamp (in seconds) when the current window resets |

**Best practice:** monitor `X-RateLimit-Remaining` proactively and slow down *before* it reaches zero, rather than waiting to be throttled.

## What happens when you exceed the limit

When you exceed your limit, the request returns `HTTP 429 Too Many Requests`. When you receive a `429`, **stop, wait, and retry using exponential backoff.** Ideally, do not retry before the time indicated by `X-RateLimit-Reset`.

## Exponential backoff

Instead of retrying a throttled request immediately (which only adds load and produces more `429`s), wait a short interval and double it after each subsequent failure - e.g. 1s, then 2s, 4s, 8s - up to a maximum, until the request succeeds. Add a small amount of randomness ("jitter") to each wait so that many clients don't retry in lockstep.

Example (pseudocode):

```python
delay = 1.0          # seconds
max_delay = 60.0
for attempt in range(max_retries):
    response = send_request()
    if response.status_code != 429:
        break
    sleep(delay + random.uniform(0, 0.5))   # add jitter
    delay = min(delay * 2, max_delay)       # exponential backoff
```

## Sandbox vs. production limits

Sandbox and production do not share the same rate limits. Sandbox is provisioned for **functional testing** - verifying that your integration creates accounts, places orders, journals funds, and handles responses correctly - and its rate limits are **significantly lower** than production.

Because of this, a request rate that works comfortably in production may be throttled in sandbox. Rate limiting you observe in sandbox is therefore **not a reliable signal** of the limits or headroom you'll have in production.

Sandbox responses include the same `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers as production, so you can still validate that your client reads them and backs off correctly - just don't treat the sandbox numbers themselves as representative of production.

## Load testing

**Do not use the sandbox for load testing.** Sandbox is intended for functional testing, and its rate limits are far lower than production. A load test against sandbox will hit limits it would never hit in production, so the results are misleading and the exercise mostly measures the sandbox throttle rather than your integration.

Sandbox also isn't a faithful stand-in for production latency. Many operations that reach real downstream systems in production (for example, order routing) are simulated in sandbox, so timing and behavior differ.

**Recommended approach:** build your integration so that calls to Alpaca can be **stubbed or mocked**, and enable that mode for load tests. To keep results realistic, have the stub simulate latency based on durations you've sampled from real production API calls. This lets you exercise your own system's throughput, queuing, and backoff logic without being gated by sandbox limits.

## If you need a higher limit

Increases are reviewed based on demonstrated need. If you have a genuine, sustained requirement for a higher limit, reach out to Alpaca and be specific about the driver: your use case, expected peak requests per minute, and the time pattern of the traffic. Limits exist to keep the platform stable for everyone, so increases are granted against real, evidenced usage.