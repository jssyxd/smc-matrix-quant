# Activities

Source: https://docs.alpaca.markets/us/docs/activity-sse.md

---
updatedAt: 2026-09-16T08:56:10.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Activities

Integration Guide & Migration Playbook

## Quick References

* [Introduction](#introduction)
* [Core Concept: State Machine Replication](#core-concept-state-machine-replication)
* [Endpoint References](#endpoint-references)
* [Event Schema](#event-schema)
* [Supported Activity Types](#supported-activity-types)
* [Integration Guide (New Partners)](#integration-guide-new-partners)
* [Migration Playbook (Existing Partners)](#migration-playbook-existing-partners)
  * [What Changes](#what-changes)
  * [Critical Migration Detail: Order Lifecycle Events](#critical-migration-detail-order-lifecycle-events)
  * [Field Mapping: Trade Events SSE → Activity SSE](#field-mapping-legacy-trade-events-sse--activity-sse)
  * [Field Mapping: Legacy NTA Events SSE → Activity SSE](#field-mapping-legacy-nta-events-sse--activity-sse)
  * [Field Mapping: Legacy Activities REST → Activity SSE](#field-mapping-legacy-activities-rest--activity-sse)
  * [Migration Checklist](#migration-checklist)
* [Event Samples](#event-samples)
* [Best Practices](#best-practices)

## Introduction

Alpaca's **Activity SSE** is a single Server-Sent Events endpoint that streams every activity — trade fills, corporate actions, fees, journals, transfers, and more — in real time with a unified schema.

It replaces or supersedes the following legacy endpoints:

| Legacy Endpoint               | Replacement Status                                                                                                                                                                                                                                                                                                                                                                                  | Type |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| `GET /v1/events/nta`          | **Fully replaced.** All NTA events are available on the Activity SSE with a richer schema.                                                                                                                                                                                                                                                                                                          | SSE  |
| `GET /v1/accounts/activities` | **Fully replaced.** Historical activity queries are supported via the `since` / `until` parameters. Activities booked after February 11, 2026 are available on the new endpoint.                                                                                                                                                                                                                    | REST |
| `GET /v2/events/trades`       | **Subset of events available.** Trade fills, corrections, and busts are available on the Activity SSE. Non-fill order lifecycle events (e.g., `accepted`, `canceled`, `expired`, `replaced`) are NOT activities and will NOT appear. If you depend on these events, continue using the Trade Events SSE alongside the Activity SSE. Latency on the Trade Events SSE stream is also generally lower. | SSE  |

**Why this matters for you:**

* **One connection for all activities** instead of separate NTA and REST endpoints. Partners who also need non-fill order lifecycle events (e.g., `accepted`, `canceled`) will still use the Trade Events SSE for those, but all financial state changes flow through a single Activity SSE connection.
* **Unified schema** with a common envelope and type-specific `details`, eliminating inconsistent field naming.
* **Stable identifier** (`ref_id`) for every activity, usable across SSE and future REST endpoints.
* **ULID-based&#x20;**`event_id` on every event, enabling lexicographic sorting and deterministic replay.

***

## Core Concept: State Machine Replication

Alpaca expects every partner to maintain a backend system that mirrors the financial state of customer accounts — positions, cash balances, and transaction history.

The Activity SSE is the mechanism for keeping that mirror in sync:

1. **Connect** to the Activity SSE.
2. **Receive** each activity event as it occurs.
3. **Apply** the event to your local state (update positions, adjust cash, record the transaction).
4. **Persist** the `event_id` (ULID) of the last successfully processed event.
5. **On reconnect**, resume from the persisted `event_id` using the `since_id` parameter. Process any re-delivered events idempotently using `ref_id` as your deduplication key.

Every activity event represents a state change that has already occurred on Alpaca's side. Your system should apply these events to converge toward the same state.

***

## Endpoint References

> **Note:** This endpoint is currently served under `/v2beta1/`. The path may change when it moves to general availability.

### Activities SSE

Streams events on account activities.

API Reference is available [here](https://docs.alpaca.markets/reference/subscribetoactivitiessse-1).

### Single Event Lookup

Returns a single activity event identified by its `event_id` ULID.

API Reference is available [here](https://docs.alpaca.markets/reference/get_v2alpha1-accounts-account-id-events-activities-event-id).

***

## Event Schema

Every event follows a **two-layer structure**: common fields at the top level, plus a `details` object with fields specific to the activity type.

### Common Fields (present on every event)

| Field              | Type                | Required | Description                                                                                                                                                                                                                                                                                                                  |
| ------------------ | ------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_id`       | UUID                | Yes      | The account this activity belongs to.                                                                                                                                                                                                                                                                                        |
| `at`               | datetime (RFC 3339) | Yes      | The business event timestamp — when the activity occurred in the source system (OMS or Ledgie) emitted.                                                                                                                                                                                                                      |
| `event_id`         | ULID                | Yes      | Lexicographically sortable, monotonically increasing event identifier. Consists of: the first 6 bytes encode the current time in UTC with miliseconds precision, the last 10 bytes are entropy. The time part encodes the timestamp when event-streaming emitted the event (publication time).  Use for cursor-based replay. |
| `activity_type`    | string              | Yes      | Primary activity classification (e.g., `TRD`, `DIV`, `SPLIT`, `FEE`).                                                                                                                                                                                                                                                        |
| `activity_subtype` | string              | No       | Further classification within the type (e.g., `CDIV`, `FSPLIT`, `REG`).                                                                                                                                                                                                                                                      |
| `ref_id`           | UUID                | Yes      | Stable unique identifier for this activity. For trades: the execution ID. For non-trade activities: the transaction ID. Use as your deduplication key.                                                                                                                                                                       |
| `status`           | string              | Yes      | Status of the activity (e.g., `executed`).                                                                                                                                                                                                                                                                                   |
| `executed_at`      | datetime (RFC 3339) | Yes      | When the activity was executed.                                                                                                                                                                                                                                                                                              |
| `settle_date`      | date                | Yes      | Settlement date for the activity.                                                                                                                                                                                                                                                                                            |
| `qty`              | decimal string      | No       | Quantity of the security involved.                                                                                                                                                                                                                                                                                           |
| `price`            | decimal string      | No       | Price of the security involved.                                                                                                                                                                                                                                                                                              |
| `net_amount`       | decimal string      | No       | Net cash impact (positive = credit, negative = debit).                                                                                                                                                                                                                                                                       |
| `currency`         | string              | Yes      | ISO currency code (e.g., `USD`).                                                                                                                                                                                                                                                                                             |
| `swap_rate`        | decimal string      | No       | FX conversion rate for local currency activities.                                                                                                                                                                                                                                                                            |
| `swap_fee_bps`     | decimal string      | No       | FX conversion fee in basis points.                                                                                                                                                                                                                                                                                           |
| `previous_id`      | UUID                | No       | Present when this activity corrects or cancels a prior activity. Contains the prior activity's `ref_id`.                                                                                                                                                                                                                     |
| `details`          | object              | Yes      | Activity-type-specific fields. Structure varies by `activity_type` and `activity_subtype`.                                                                                                                                                                                                                                   |

### The `details` Object

The `details` object contains fields specific to the activity type. This design avoids excessive nulls and provides rich, type-specific data.

For example, a `TRD` (trade fill) activity's `details` includes `order_id`, `side`, `symbol`, `cum_qty`, `leaves_qty`, `order_status`, and `execution_type`. A `DIV` / `CDIV` (cash dividend) activity's `details` includes `ca_id`, `symbol`, `rate`, `entitled_qty`, `cash_payout`, and corporate action dates.

The full details schema per activity type is defined in the API reference and samples are available in the last section below.

For fee activities (`FEE`), `details` may include a `parent_id` field linking the fee to the specific transaction that caused it. This applies to fees with a one-to-one relationship to a parent trade (e.g., `COM`, `OCOM`). Volume-based fees charged across multiple trades for a period (e.g., `REG`, `TAF`, `CAT`, `ORF`, `NRV`, `NRC`, `BSWP`) do not include `parent_id`.

***

## Supported Activity Types

### Trade Activities

| `activity_type` | `activity_subtype` | Description                                                                                                                                                                                                                 |
| --------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TRD`           | —                  | Trade fill (equity or options). `details.execution_type` is one of: `fill`, `trade_correct`, `trade_bust`. Multi-leg orders produce one `TRD` event per leg, each with a distinct `ref_id` but the same `details.order_id`. |

### Corporate Actions (Equity)

| `activity_type` | `activity_subtype` | Description                            |
| --------------- | ------------------ | -------------------------------------- |
| `CGD`           | `STCG`             | Short-Term Capital Gain                |
| `CGD`           | `LTCG`             | Long-Term Capital Gain                 |
| `DIV`           | `CDIV`             | Cash dividend                          |
| `DIV`           | `SDIV`             | Stock dividend                         |
| `DIV`           | `SPD`              | Substitute payment in lieu of dividend |
| `DIV`           | `ROC`              | Return of capital                      |
| `SPLIT`         | `FSPLIT`           | Forward stock split                    |
| `SPLIT`         | `RSPLIT`           | Reverse stock split                    |
| `SPLIT`         | `USPLIT`           | Unit split                             |
| `SPIN`          | —                  | Spinoff                                |
| `MA`            | `CMA`              | Cash merger                            |
| `MA`            | `SMA`              | Stock merger                           |
| `MA`            | `SCMA`             | Stock & cash merger                    |
| `NC`            | `SNC`              | Symbol name change                     |
| `NC`            | `CNC`              | CUSIP name change                      |
| `NC`            | `SCNC`             | Symbol & CUSIP name change             |
| `REO`           | `REOS`             | Stock-only reorganization              |
| `REO`           | `REOC`             | Cash-only reorganization               |
| `REO`           | `REOSC`            | Stock and cash reorganization          |
| `REORG`         | `WRM`              | Worthless removal                      |
| `VOF`           | `VDST`             | Rights distribution                    |
| `VOF`           | `VTND`             | Tender offer                           |
| `VOF`           | `VWRT`             | Warrant exercise                       |
| `VOF`           | `VRGT`             | Rights offer                           |
| `VOF`           | `VEXH`             | Exchange offer                         |
| `FIMAT`         | —                  | Fixed income maturity/redemption       |
| `DIVNRA`        | —                  | Dividend tax withholding               |

### Corporate Actions (Options)

| `activity_type` | `activity_subtype` | Description                            |
| --------------- | ------------------ | -------------------------------------- |
| `OPCA`          | `DIV.CDIV`         | Options CA: cash dividend              |
| `OPCA`          | `DIV.SDIV`         | Options CA: stock dividend             |
| `OPCA`          | `MA.CMA`           | Options CA: cash merger                |
| `OPCA`          | `MA.SMA`           | Options CA: stock merger               |
| `OPCA`          | `MA.SCMA`          | Options CA: stock & cash merger        |
| `OPCA`          | `NC.SNC`           | Options CA: symbol name change         |
| `OPCA`          | `NC.CNC`           | Options CA: CUSIP name change          |
| `OPCA`          | `NC.SCNC`          | Options CA: symbol & CUSIP name change |
| `OPCA`          | `SPIN`             | Options CA: spinoff                    |
| `OPCA`          | `SPLIT.FSPLIT`     | Options CA: forward split              |
| `OPCA`          | `SPLIT.RSPLIT`     | Options CA: reverse split              |
| `OPCA`          | `SPLIT.USPLIT`     | Options CA: unit split                 |

### Options (Non-CA)

| `activity_type` | `activity_subtype` | Description                                    |
| --------------- | ------------------ | ---------------------------------------------- |
| `OPASN`         | —                  | Option assignment                              |
| `OPEXC`         | —                  | Option exercise                                |
| `OPEXP`         | —                  | Option expiry                                  |
| `OPTRD`         | —                  | Option trade (paired with assignment/exercise) |
| `OPCSH`         | —                  | Options cash settlement                        |

### Transfers & Journals

| `activity_type` | `activity_subtype` | Description                                                                                                                                            |
| --------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ACATC`         | —                  | ACAT transfer (cash)                                                                                                                                   |
| `ACATS`         | —                  | ACAT transfer (securities)                                                                                                                             |
| `FOPT`          | —                  | Free-of-payment transfer (DTCC). Previously reported as `ACATC`/`ACATS`. If you filtered for ACAT types to capture all transfers, add `FOPT` handling. |
| `JNLC`          | —                  | Journal entry (cash)                                                                                                                                   |
| `JNLS`          | —                  | Journal entry (securities)                                                                                                                             |
| `CSW`           | —                  | Cash withdrawal                                                                                                                                        |
| `CSD`           | —                  | Cash disbursement (credit / cash inbound)                                                                                                              |
| `MEM`           | —                  | Instant funding memo-post                                                                                                                              |

### Fees & Interest

| `activity_type` | `activity_subtype` | Description                                                                                  |
| :-------------- | :----------------- | :------------------------------------------------------------------------------------------- |
| `FEE`           | `REG`              | Regulatory (SEC) fee                                                                         |
| `FEE`           | `TAF`              | Trading Activity Fee                                                                         |
| `FEE`           | `ORF`              | Options Regulatory Fee                                                                       |
| `FEE`           | `OCC`              | Options Clearing Corporation fee                                                             |
| `FEE`           | `NRV`              | Non-retail venue fee                                                                         |
| `FEE`           | `NRC`              | Non-retail commission fee                                                                    |
| `FEE`           | `LCT`              | Local currency trading fee                                                                   |
| `FEE`           | `COM`              | Commission                                                                                   |
| `FEE`           | `CAT`              | Consolidated Audit Trail fee                                                                 |
| `FEE`           | `ADR`              | ADR fee                                                                                      |
| `FEE`           | `OCOM`             | Options commission (exercise/liquidation)                                                    |
| `FEE`           | `BSWP`             | Banking sweep fee                                                                            |
| `INT`           | `MGN`              | Margin interest                                                                              |
| `INT`           | `CDT`              | Credit interest                                                                              |
| `INT`           | `SWP`              | Sweep interest                                                                               |
| `INT`           | `QII`              | Qualified interest income                                                                    |
| `INT`           | `FPSL`             | Fully Paid Securities Lending interest income                                                |
| `INT`           | `FI`               | Coupon payment on a fixed-income security or<br />Accrued interest on a full or partial call |

### Withholding

| `activity_type` | `activity_subtype` | Description         |
| --------------- | ------------------ | ------------------- |
| `WH`            | `SWH`              | State withholding   |
| `WH`            | `FWH`              | Federal withholding |
| `WH`            | `SLWH`             | Sales withholding   |

***

## Integration Guide (New Partners)

If you are a new Alpaca partner, integrate directly with the Activity SSE. Do not use the legacy endpoints.

### Step 1 — Establish the SSE Connection

Open a long-lived HTTP GET request to `/v2beta1/events/activities` with your Broker API credentials. The server will hold the connection open and push `data:` lines as events occur.

### Step 2 — Parse Each Event

Each SSE `data:` line contains a JSON object. Parse the common fields first (`activity_type`, `ref_id`, `event_id`, `account_id`), then route to type-specific handling logic based on `activity_type` and `activity_subtype`.

### Step 3 — Apply the Event to Your Local State

For each event, update your local database:

* **TRD (trade fill):** Record the fill. Update the account's position for the symbol. Adjust cash by `net_amount`.
* **DIV (dividend):** For `CDIV`, credit `net_amount` to cash. For `SDIV`, add `qty` shares to the position.
* **SPLIT:** Adjust the position quantity per the split ratio in `details`.
* **FEE / INT:** Adjust cash by `net_amount`.
* **JNLC / JNLS:** Adjust cash or positions accordingly.
* **MA, SPIN, NC, REORG:** Update positions per the corporate action details (remove old shares, add new shares, credit cash as applicable).

### Step 4 — Persist Your Cursor

After successfully processing each event, persist the `event_id` (ULID). This is your replay cursor.

### Step 5 — Handle Reconnections

When your connection drops (network issue, server restart, deployment):

1. Reconnect to the same endpoint.
2. Set `since_id` to the last successfully processed `event_id`.
3. Process all events received, deduplicating by `ref_id`.

### Step 6 — Handle Corrections and Busts

When `previous_id` is present on an event, it means this activity corrects or cancels a prior activity whose `ref_id` matches `previous_id`. Reverse the original activity in your system and apply the new one.

### Step 7 — Handle SSE Comments

Lines beginning with `:` are SSE comments, not data. Handle these two specifically:

* `:heartbeat` — The connection is alive. No action needed.
* `: you are reading too slowly, dropped N messages` — Your consumer is too slow. You have missed events. Reconnect with `since_id` set to your last processed `event_id` to replay missed events.
* `: internal server error` — The server is closing the connection. Reconnect.

### Step 8 — Historical Replay

To read historical data (e.g., during initial onboarding or reconciliation), connect with a `since` timestamp or `since_id`. If you use since\_id, and don’t specify until\_id, server streams all historical events from that point first, then transitions to real-time.

***

## Migration Playbook (Existing Partners)

This section is for partners currently using the legacy NTA Events SSE (`/v1/events/nta`) and/or the Activities REST endpoint (`/v1/accounts/activities`). We also document the differences with the current Trade Events SSE (`/v2/events/trades`), even though we don’t consider the new endpoint to be its full replacement..

### What Changes

| Aspect                      | Legacy                                                                   | Activity SSE                                                                                               |
| --------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Endpoints**               | Three separate endpoints (trade SSE, NTA SSE, activities REST)           | Single endpoint: `/v2beta1/events/activities`                                                              |
| **Event IDs**               | Integer (`event_id`) + ULID (`event_ulid`) depending on endpoint version | ULID only (`event_id`)                                                                                     |
| **Activity identification** | No common stable ID across SSE and REST                                  | `ref_id` (UUID) on every event                                                                             |
| **Schema**                  | Flat, inconsistent fields across trade and NTA events                    | Two-layer: common envelope + type-specific `details` object                                                |
| **Trade activity naming**   | `FILL` (REST) / `event: fill` (SSE)                                      | `activity_type: TRD`                                                                                       |
| **NTA type field**          | `entry_type` + `entry_sub_type`                                          | `activity_type` + `activity_subtype`                                                                       |
| **Free-text description**   | `description` field on NTA events                                        | Removed. Replaced by structured fields in `details`.                                                       |
| **Embedded order object**   | Full order object on trade events                                        | Only key order fields in `details` (`order_id`, `client_order_id`, `side`, `symbol`, `order_status`, etc.) |
| `per_share_amount`          | Present on legacy NTA events                                             | Replaced by `details.rate` (where applicable)                                                              |
| `position_qty`              | Present on trade events                                                  | Not present. Compute locally from fills.                                                                   |

### Order Lifecycle Events

The Trade Events SSE emits events for the **full order lifecycle**: `accepted`, `new`, `pending_new`, `fill`, `partial_fill`, `canceled`, `expired`, `replaced`, `rejected`, `done_for_day`, `held`, `stopped`, `suspended`, `pending_cancel`, `pending_replace`, `calculated`, `order_replace_rejected`, `order_cancel_rejected`, `trade_bust`, `trade_correct`.

The Activity SSE emits **only events that represent actual activities** — that is, events that change the financial state of the account:

* `fill` → `activity_type: TRD`, `details.execution_type: fill`
* `trade_correct` → `activity_type: TRD`, `details.execution_type: trade_correct`
* `trade_bust` → `activity_type: TRD`, `details.execution_type: trade_bust`

**Order lifecycle events that do not result in a fill** (`accepted`, `new`, `canceled`, `expired`, `replaced`, etc.) are **not activities** and will **not** appear on the Activity SSE. These events do not change positions or cash.

If your application depends on these non-fill order lifecycle events (e.g., to show "order accepted" or "order canceled" notifications), you should continue using the Trade Events SSE (`/v2/events/trades`) for order lifecycle tracking alongside the Activity SSE for activity tracking.

For state machine replication of positions, cash, and transaction history, the Activity SSE alone is sufficient.

### Field Mapping: Trade Events SSE → Activity SSE

| Trade Event Field                   | Activity SSE Field        | Notes                                                                                                                                                                                                                    |
| ----------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `account_id`                        | `account_id`              | Unchanged.                                                                                                                                                                                                               |
| `at`                                | `at`                      | Unchanged. This field, in both endpoints, encodes the  business event timestamp — when the activity occurred in the source system. If you previously used `at` as a proxy for execution time, use `executed_at` instead. |
| `event_id` (integer, v1)            | —                         | Removed. Use ULID-based `event_id` instead.                                                                                                                                                                              |
| `event_ulid` (v1) / `event_id` (v2) | `event_id`                | Now always a ULID.                                                                                                                                                                                                       |
| `event` (e.g., `fill`, `new`)       | `details.execution_type`  | Only `fill`, `trade_correct`, `trade_bust` are emitted. Non-fill lifecycle events are not activities.                                                                                                                    |
| `timestamp`                         | `executed_at`             | Renamed. The legacy `timestamp` field (which had varying semantics per event type) is replaced by `executed_at`.                                                                                                         |
| `order.id`                          | `details.order_id`        | Order object is no longer embedded; key fields promoted to `details`.                                                                                                                                                    |
| `order.client_order_id`             | `details.client_order_id` | —                                                                                                                                                                                                                        |
| `order.symbol`                      | `details.symbol`          | —                                                                                                                                                                                                                        |
| `order.asset_id`                    | `details.asset_id`        | —                                                                                                                                                                                                                        |
| `order.side`                        | `details.side`            | —                                                                                                                                                                                                                        |
| `order.status`                      | `details.order_status`    | —                                                                                                                                                                                                                        |
| `order.filled_qty`                  | `details.cum_qty`         | Renamed. Cumulative filled quantity on the order.                                                                                                                                                                        |
| `order.commission`                  | `details.commission`      | —                                                                                                                                                                                                                        |
| `order.*` (other fields)            | —                         | Remaining order fields (limit\_price, stop\_price, time\_in\_force, etc.) are not included.                                                                                                                              |
| `price`                             | `price`                   | Moved to common envelope.                                                                                                                                                                                                |
| `qty`                               | `qty`                     | Moved to common envelope.                                                                                                                                                                                                |
| `position_qty`                      | —                         | Removed. Compute from cumulative fills on your side.                                                                                                                                                                     |
| `execution_id`                      | `ref_id`                  | Renamed. Same value (execution UUID).                                                                                                                                                                                    |
| `previous_execution_id`             | `previous_id`             | Renamed. Present on `trade_correct` and `trade_bust` events.                                                                                                                                                             |

### Field Mapping: Legacy NTA Events SSE → Activity SSE

| Legacy NTA Event Field | Activity SSE Field    | Notes                                                                                                                                                                                                                                               |
| ---------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_id`           | `account_id`          | Unchanged.                                                                                                                                                                                                                                          |
| `at`                   | `at`                  | Unchanged. Both in the legacy SSE endpoints, `at` was the business event timestamp — when the activity occurred in the source system. In the Activity SSE, the `at` field maintains this semantics. See the Trade Events mapping above for details. |
| `event_id` (integer)   | —                     | Removed.                                                                                                                                                                                                                                            |
| `event_ulid`           | `event_id`            | Renamed. Now the primary event identifier.                                                                                                                                                                                                          |
| `id` (record UUID)     | `ref_id`              | Renamed. The stable unique identifier for the activity.                                                                                                                                                                                             |
| `entry_type`           | `activity_type`       | Renamed. Same values (e.g., `DIV`, `FEE`, `JNLC`).                                                                                                                                                                                                  |
| `entry_sub_type`       | `activity_subtype`    | Renamed. Same values (e.g., `CDIV`, `REG`, `TAF`).                                                                                                                                                                                                  |
| `status`               | `status`              | Unchanged.                                                                                                                                                                                                                                          |
| `qty`                  | `qty`                 | Unchanged. Now a string-formatted decimal.                                                                                                                                                                                                          |
| `price`                | `price`               | Unchanged. Now a string-formatted decimal.                                                                                                                                                                                                          |
| `net_amount`           | `net_amount`          | Unchanged. Now a string-formatted decimal.                                                                                                                                                                                                          |
| `settle_date`          | `settle_date`         | Unchanged.                                                                                                                                                                                                                                          |
| `system_date`          | `details.system_date` | Moved into `details`. Format changed from datetime to date (`YYYY-MM-DD`).                                                                                                                                                                          |
| `symbol`               | `details.symbol`      | Moved into `details` (present where applicable per type).                                                                                                                                                                                           |
| `cusip`                | `details.cusip`       | Moved into `details` (present where applicable per type).                                                                                                                                                                                           |
| `description`          | —                     | Removed. All information previously in the free-text description is now represented as structured fields in `details`.                                                                                                                              |
| `per_share_amount`     | `details.rate`        | Renamed and moved. Represents the per-share rate (e.g., dividend rate).                                                                                                                                                                             |
| `group_id`             | `details.group_id`    | Moved into `details`. Groups related activities (e.g., both legs of a split).                                                                                                                                                                       |
| `corporate_action_id`  | `details.ca_id`       | Renamed and moved into `details`.                                                                                                                                                                                                                   |
| `swap_rate`            | `swap_rate`           | Unchanged. Remains at the top level.                                                                                                                                                                                                                |
| `execution_id`         | —                     | Was present on some legacy NTA fee events. In the new schema, use `details.parent_id` for fee-to-parent-transaction linkage.                                                                                                                        |

### Field Mapping: Legacy Activities REST → Activity SSE

| Legacy REST Field           | Activity SSE Field      | Notes                                       |
| --------------------------- | ----------------------- | ------------------------------------------- |
| `id`                        | `ref_id`                | Renamed.                                    |
| `activity_type` (`FILL`)    | `activity_type` (`TRD`) | `FILL` is now `TRD`.                        |
| `activity_type` (non-trade) | `activity_type`         | Same values for non-trade types.            |
| `activity_sub_type`         | `activity_subtype`      | Renamed (underscore removed). Same values.  |
| `transaction_time`          | `executed_at`           | Renamed.                                    |
| `date`                      | `settle_date`           | Renamed.                                    |
| `net_amount`                | `net_amount`            | Unchanged.                                  |
| `qty`                       | `qty`                   | Unchanged.                                  |
| `price`                     | `price`                 | Unchanged.                                  |
| `side`                      | `details.side`          | Moved to `details` (trade activities only). |
| `symbol`                    | `details.symbol`        | Moved to `details`.                         |
| `order_id`                  | `details.order_id`      | Moved to `details` (trade activities only). |
| `cum_qty`                   | `details.cum_qty`       | Moved to `details` (trade activities only). |
| `leaves_qty`                | `details.leaves_qty`    | Moved to `details` (trade activities only). |
| `order_status`              | `details.order_status`  | Moved to `details` (trade activities only). |

### Migration Checklist

Use this checklist to track your migration from legacy endpoints to the Activity SSE.

**Preparation:**

* [ ] Read and understand this guide and the OpenAPI specification for `ActivityEventV2`.
* [ ] Inventory every place in your codebase that consumes from Trade SSE, legacy NTA SSE, or Activities REST.
* [ ] Identify if you depend on non-fill order lifecycle events (e.g., `accepted`, `canceled`, `expired`). If so, keep using the Trade Events SSE for those.

**Implementation:**

* [ ] Build a consumer for `GET /v2beta1/events/activities` that parses the common envelope fields.
* [ ] Implement routing logic that dispatches on `activity_type` (and `activity_subtype` where needed) to type-specific handlers.
* [ ] Update your data model to store `ref_id` as the primary activity identifier and `event_id` (ULID) as your replay cursor.
* [ ] Replace references to `entry_type` / `entry_sub_type` with `activity_type` / `activity_subtype`.
* [ ] Replace references to the `description` free-text field with structured field reads from `details`.
* [ ] If you previously stored `position_qty` from trade events, switch to computing position quantities from cumulative fills.
* [ ] If you referenced `per_share_amount`, switch to reading `details.rate`.
* [ ] Update deduplication logic to use `ref_id` instead of the legacy `id` field.
* [ ] Implement `previous_id` handling for trade corrections and busts.
* [ ] Verify that your reconnection logic uses `since_id` with the ULID `event_id`.

**Validation:**

* [ ] Run both legacy and new consumers in parallel. Compare the activities received: every trade fill and legacy NTA event should have a corresponding Activity SSE event with matching `ref_id`.
* [ ] Verify that `net_amount`, `qty`, `price`, and `settle_date` match between legacy and new events for the same activity.
* [ ] Confirm that corporate action details (split ratios, dividend rates, merger terms) are correctly extracted from the `details` object.
* [ ] Test reconnection: disconnect your consumer, wait, reconnect with `since_id`, and verify no events are lost and duplicates are handled.

**Cutover:**

* [ ] Once validation passes, decommission your legacy NTA SSE consumer.
* [ ] Decommission your legacy Activities REST polling (if used for real-time tracking).
* [ ] If you do not need non-fill order lifecycle events, decommission your Trade SSE consumer.
* [ ] Monitor for any dropped messages (watch for `: you are reading too slowly` comments).

***

## Event Samples

Representative samples for each activity type. All identifiers have been replaced with placeholders.

```json TRD (equities)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "TRD",
  "qty": "0.04",
  "price": "480.338",
  "currency": "USD",
  "net_amount": "-19.21",
  "status": "executed",
  "at": "2026-01-02T14:43:59.052726Z",
  "executed_at": "2026-01-02T14:43:59.05095724Z",
  "settle_date": "2026-01-05",
  "details": {
    "asset_id": "<ASID>",
    "order_id": "<ORID>",
    "client_order_id": "<CLID>",
    "side": "buy",
    "order_status": "filled",
    "execution_type": "fill",
    "symbol": "MSFT",
    "cum_qty": "0.04",
    "leaves_qty": "0"
  }
}
```
```json TRD (options)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "TRD",
  "qty": "1",
  "price": "9.3",
  "currency": "USD",
  "net_amount": "-930.02",
  "status": "executed",
  "at": "2026-01-10T14:30:02.89489Z",
  "executed_at": "2026-01-10T14:30:02.888518094Z",
  "settle_date": "2026-01-06",
  "details": {
    "asset_id": "<ASID>",
    "order_id": "<ORID>",
    "client_order_id": "<CLID>",
    "side": "buy",
    "order_status": "filled",
    "execution_type": "fill",
    "symbol": "F260109C00006000",
    "cum_qty": "1",
    "leaves_qty": "0",
    "commission": "0"
  }
}
```
```json CSD
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "CSD",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "1382000",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-13T09:37:31.970401Z",
  "settle_date": "2026-02-13",
  "details": {
    "system_date": "2026-02-13"
  }
}
```
```json CSW
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "CSW",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-7",
  "status": "executed",
  "at": "2026-01-17T02:00:08.514798Z",
  "executed_at": "2026-01-17T04:35:10.338561Z",
  "settle_date": "2026-01-16",
  "details": {
    "system_date": "2026-01-20"
  }
}
```
```json JNLC
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "JNLC",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-4.81",
  "status": "executed",
  "at": "2026-01-15T02:00:08.514798Z",
  "executed_at": "2026-01-15T08:00:00.925529Z",
  "settle_date": "2026-01-15",
  "details": {
    "journal_id": "<JRLID>",
    "system_date": "2026-01-15"
  }
}
```
```json JLNS
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "JNLS",
  "qty": "0.00911",
  "price": "638.2799",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T02:00:08.514798Z",
  "executed_at": "2026-01-15T23:54:13.330501Z",
  "settle_date": "2026-01-15",
  "details": {
    "journal_id": "<JRLID>",
    "symbol": "AAPL",
    "system_date": "2026-01-15"
  }
}
```
```json FEE
# there are some fees, that do not have one single transaction from which they are derived, but they are derived on a volume/bulk/duration of transactions. For them, there is no `parent_id` relationship. Such fees sub-types include: REG, TAF, CAT, ADR, ORF, BSWP, NRV, NRC, ADR, OCOM, LOC

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "FEE",
  "activity_subtype": "TAF",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-0.01",
  "status": "executed",
  "at": "2026-01-16T01:00:08.514798Z",
  "executed_at": "2026-01-16T01:00:00Z",
  "settle_date": "2026-01-16",
  "details": {
    "system_date": "2026-01-15"
  }
}


# All other fees, will have parent_id relationship setup, as they have one-to-one relationship with the transaction which they are derived from. 
# These fees may have sub-types
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "FEE",
  "activity_subtype": "OCC",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-0.02",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-01-15T14:44:09.189982Z",
  "settle_date": "2026-01-15",
  "details": {
    "parent_id": "<PTID>",
    "system_date": "2026-01-15"
  }
}

# or no sub-type at all
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "FEE",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-0.02",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-01-15T14:44:09.189982Z",
  "settle_date": "2026-01-15",
  "details": {
    "parent_id": "<PTID>",
    "system_date": "2026-01-15"
  }
}
```
```json ACATC
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "ACATC",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "118.79",
  "status": "executed",
  "at": "2025-12-06T02:00:08.514798Z",
  "executed_at": "2025-12-06T00:00:42.17753Z",
  "settle_date": "2025-12-08",
  "details": {
    "request_id": "<RQTID>",
    "external_id": "20251110012345@000031",
    "system_date": "2025-12-05",
    "hold_date": "2025-12-08"
  }
}
```
```json ACATS
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "ACATS",
  "qty": "4",
  "price": "157.44",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2025-12-06T02:00:08.514798Z",
  "executed_at": "2025-12-06T00:00:42.17753Z",
  "settle_date": "2025-12-08",
  "details": {
    "request_id": "<RQTID>",
    "external_id": "20252220054321@000007",
    "symbol": "AAPL",
    "system_date": "2025-12-05",
    "hold_date": "2025-12-08"
  }
}
```
```json INT (MGN)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "INT",
  "activity_subtype": "MGN",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-3.01",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-28T05:56:15.207304Z",
  "settle_date": "2026-02-27",
  "details": {
    "system_date": "2026-03-02"
  }
}
```
```json INT (FPSL)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "INT",
  "activity_subtype": "FPSL",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "0.01",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T05:00:30.215648Z",
  "settle_date": "2026-02-27",
  "details": {
    "system_date": "2026-02-27"
  }
}
```
```json INT (FI)
// Regular coupon 
// - has rate
// - does not have accrued_interest_rate or price
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "INT",
  "activity_subtype": "FI",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "3203.13",
  "status": "executed",
  "at": "2026-07-27T16:00:08.514798Z",
  "executed_at": "2026-07-27T16:00:00Z",
  "settle_date": "2026-07-27",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "entitled_qty": "205000",
    "cash_payout": "3203.125",
    "cusip": "61761J3R8",
    "isin": "US61761J3R84",
    "rate": "15.625",
    "record_date": "2026-07-24",
    "payment_date": "2026-07-27",
    "position_date": "2026-07-24",
    "system_date": "2026-07-27"
  }
}

// Accrued intereston for a full or partial call  
// - no rate 
// - instead has price + accrued_interest_rate
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "INT",
  "activity_subtype": "FI",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "42.50",
  "status": "executed",
  "at": "2026-07-08T16:00:08.514798Z",
  "executed_at": "2026-07-08T16:00:00Z",
  "settle_date": "2026-07-09",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "entitled_qty": "10000",
    "cash_payout": "42.50",
    "cusip": "037833EK4",
    "isin": "US037833EK41",
    "price": "101.25",
    "accrued_interest_rate": "4.25",
    "record_date": "2026-07-08",
    "payment_date": "2026-07-09",
    "position_date": "2026-07-08",
    "system_date": "2026-07-09"
  }
}
```
```json DIV (cash)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "DIV",
  "activity_subtype": "CDIV",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "28.25",
  "status": "executed",
  "at": "2026-05-19T07:44:25.462922Z",
  "executed_at": "2026-05-19T16:00:00Z",
  "settle_date": "2026-05-19",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "VG",
    "cusip": "92333F101",
    "entitled_qty": "113",
    "rate": "0.25",
    "cash_payout": "28.25",
    "foreign": "false",
    "special": "false",
    "ex_date": "2026-05-19",
    "record_date": "2026-05-19",
    "system_date": "2026-05-19",
    "payable_date": "2026-05-19",
    "position_date": "2026-05-19"
  }
}
```
```json DIV (ROC)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "DIV",
  "activity_subtype": "ROC",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "28.25",
  "status": "executed",
  "at": "2026-05-19T07:44:25.462922Z",
  "executed_at": "2026-05-19T16:00:00Z",
  "settle_date": "2026-05-19",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "VG",
    "cusip": "92333F101",
    "entitled_qty": "113",
    "rate": "0.25",
    "cash_payout": "28.25",
    "foreign": "false",
    "special": "false",
    "ex_date": "2026-05-19",
    "record_date": "2026-05-19",
    "system_date": "2026-05-19",
    "payable_date": "2026-05-19",
    "position_date": "2026-05-19"
  }
}
```
```json DIV (stock)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "DIV",
  "activity_subtype": "SDIV",
  "qty": "0.002709921",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-02T17:00:08.514798Z",
  "executed_at": "2026-01-02T17:00:00Z",
  "settle_date": "2025-12-29",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "SBS",
    "new_qty": "0.094116171",
    "entitled_qty": "0.09140625",
    "paid_qty": "0.002709921",
    "rate": "1.029647",
    "ex_date": "2025-12-29",
    "record_date": "2025-12-29",
    "system_date": "2026-01-02",
    "payable_date": "2026-01-02",
    "position_date": "2025-12-26"
  }
}
```
```json DIV (SPD)
# Substitute payment in lieu of dividend
# Often paired with a DIV/CDIV for the same corporate action. The SPD covers shares loaned out (e.g., via Fully Paid Securities Lending); the CDIV covers shares held on record date.
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "DIV",
  "activity_subtype": "SPD",
  "qty": "0",
  "price": "0",
  "currency": "",
  "net_amount": "-0.03",
  "status": "executed",
  "at": "2025-10-17T16:00:08.514798Z",
  "executed_at": "2025-10-17T16:00:00Z",
  "settle_date": "2025-10-17T00:00:00Z",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "ULTY",
    "entitled_qty": "77",
    "rate": "0.000338",
    "cash_payout": "0.026026",
    "foreign": "false",
    "special": "true",
    "ex_date": "2025-10-16",
    "record_date": "2025-10-16",
    "system_date": "2025-10-17",
    "payable_date": "2025-10-17",
    "position_date": "2025-10-16",
    "due_bill_on_date": "2025-09-03",
    "due_bill_off_date": "2025-09-02"
  }
}
```
```json DIVNRA
# DIVNRA is linked to its parent DIV activity via details.parent_id, which matches the parent DIV's ref_id. Parent can be a DIV/CDIV or a DIV/SPD.

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "DIVNRA",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "-8.47",
  "status": "executed",
  "at": "2026-05-19T07:44:25.462922Z",
  "executed_at": "2026-05-19T07:44:21.799701Z",
  "settle_date": "2026-05-19",
  "details": {
    "symbol": "VG",
    "cusip": "92886T201",
    "parent_id": "<REFID-1>",
    "system_date": "2026-05-19",
    "tax_rate": "<withholding-rate, e.g: 0.15 for AUS>",
    "tax_country": "<3-digit-country-code>"
  }
}
```
```json MA (CMA)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "MA",
  "activity_subtype": "CMA",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "0.03",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T17:00:00Z",
  "settle_date": "2026-02-27",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "0.045366059",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "cash_rate": "0.583043",
    "cash_payout": "0.03",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-27",
    "position_date": "2026-02-26",
    "effective_date": "2026-02-02"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "MA",
  "activity_subtype": "CMA",
  "qty": "-0.045366059",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T17:00:00Z",
  "settle_date": "2026-02-27",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "0.045366059",
    "cash_rate": "0.583043",
    "cash_payout": "0.03",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-27",
    "position_date": "2026-02-26",
    "effective_date": "2026-02-02",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>"
    
  }
}
```
```json MA (SMA)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "MA",
  "activity_subtype": "SMA",
  "qty": "-2000",
  "price": "0.8",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-25T05:00:00Z",
  "settle_date": "2026-02-25",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "2000",
    "acquirer_qty": "200",
    "acquiree_rate": "1",
    "acquirer_rate": "0.1",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquirer_symbol": "<ACQUIRER_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquirer_cusip": "<ACQUIRER_CUSIP>",
    "system_date": "2026-02-25",
    "payable_date": "2026-02-25",
    "position_date": "2026-02-24",
    "effective_date": "2026-02-24"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "MA",
  "activity_subtype": "SMA",
  "qty": "200",
  "price": "8",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-25T05:00:00Z",
  "settle_date": "2026-02-25",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "2000",
    "acquirer_qty": "200",
    "acquiree_rate": "1",
    "acquirer_rate": "0.1",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquirer_symbol": "<ACQUIRER_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquirer_cusip": "<ACQUIRER_CUSIP>",
    "system_date": "2026-02-25",
    "payable_date": "2026-02-25",
    "position_date": "2026-02-24",
    "effective_date": "2026-02-24"
  }
}
```
```json MA (SCMA)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "previous_id": "<PRID-1>",
  "activity_type": "MA",
  "activity_subtype": "SCMA",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "8.29",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-13T17:00:00Z",
  "settle_date": "2026-02-13",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "0.394803871",
    "acquirer_qty": "0.394803871",
    "cash_rate": "21",
    "acquiree_rate": "1",
    "acquirer_rate": "1",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquirer_symbol": "<ACQUIRER_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquirer_cusip": "<ACQUIRER_CUSIP>",
    "cash_payout": "8.29",
    "system_date": "2026-02-13",
    "payable_date": "2026-02-13",
    "position_date": "2026-02-12",
    "effective_date": "2026-02-12"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "previous_id": "<PRID-2>",
  "activity_type": "MA",
  "activity_subtype": "SCMA",
  "qty": "-0.394803871",
  "price": "15.704",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-13T17:00:00Z",
  "settle_date": "2026-02-13",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "0.394803871",
    "acquirer_qty": "0.394803871",
    "cash_rate": "21",
    "acquiree_rate": "1",
    "acquirer_rate": "1",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquirer_symbol": "<ACQUIRER_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquirer_cusip": "<ACQUIRER_CUSIP>",
    "cash_payout": "8.29",
    "system_date": "2026-02-13",
    "payable_date": "2026-02-13",
    "position_date": "2026-02-12",
    "effective_date": "2026-02-12"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-3>",
  "ref_id": "<REFID-3>",
  "previous_id": "<PRID-3>",
  "activity_type": "MA",
  "activity_subtype": "SCMA",
  "qty": "0.394803871",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-13T17:00:00Z",
  "settle_date": "2026-02-13",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "acquiree_qty": "0.394803871",
    "acquirer_qty": "0.394803871",
    "cash_rate": "21",
    "acquiree_rate": "1",
    "acquirer_rate": "1",
    "acquiree_symbol": "<ACQUIREE_SYMBOL>",
    "acquirer_symbol": "<ACQUIRER_SYMBOL>",
    "acquiree_cusip": "<ACQUIREE_CUSIP>",
    "acquirer_cusip": "<ACQUIRER_CUSIP>",
    "cash_payout": "8.29",
    "system_date": "2026-02-13",
    "payable_date": "2026-02-13",
    "position_date": "2026-02-12",
    "effective_date": "2026-02-12"
  }
}
```
```json NC (SNC)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "NC",
  "activity_subtype": "SNC",
  "qty": "-7.30762391",
  "price": "328.77",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-26T17:00:00Z",
  "settle_date": "2026-02-26",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "RNA",
    "new_symbol": "RNAM",
    "position_qty": "7.30762391",
    "system_date": "2026-02-26",
    "position_date": "2026-02-25"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "NC",
  "activity_subtype": "SNC",
  "qty": "7.30762391",
  "price": "328.77",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-26T17:00:00Z",
  "settle_date": "2026-02-26",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "RNA",
    "new_symbol": "RNAM",
    "position_qty": "7.30762391",
    "system_date": "2026-02-26",
    "position_date": "2026-02-25"
  }
}
```
```json NC (CNC)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "NC",
  "activity_subtype": "CNC",
  "qty": "-4.68546239",
  "price": "26.89",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-23T17:00:00Z",
  "settle_date": "2026-02-23",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "BRIF",
    "new_symbol": "BRIF",
    "position_qty": "4.68546239",
    "system_date": "2026-02-23",
    "position_date": "2026-02-20"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "NC",
  "activity_subtype": "CNC",
  "qty": "4.68546239",
  "price": "26.89",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-23T17:00:00Z",
  "settle_date": "2026-02-23",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "BRIF",
    "new_symbol": "BRIF",
    "position_qty": "4.68546239",
    "system_date": "2026-02-23",
    "position_date": "2026-02-20"
  }
}
```
```json NC (SCNC)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "NC",
  "activity_subtype": "SCNC",
  "qty": "1",
  "price": "0.1001",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-25T17:00:00Z",
  "settle_date": "2026-02-25",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "SVIWF",
    "new_symbol": "NUCLW",
    "position_qty": "1",
    "system_date": "2026-02-25",
    "position_date": "2026-02-24"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "NC",
  "activity_subtype": "SCNC",
  "qty": "-1",
  "price": "0.1001",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-25T17:00:00Z",
  "settle_date": "2026-02-25",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "SVIWF",
    "new_symbol": "NUCLW",
    "position_qty": "1",
    "system_date": "2026-02-25",
    "position_date": "2026-02-24"
  }
}
```
```json SPLIT (FSPLIT)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "SPLIT",
  "activity_subtype": "FSPLIT",
  "qty": "-0.54796447",
  "price": "62.32",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T17:00:00Z",
  "settle_date": "2026-02-26",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3038297",
    "symbol": "SF",
    "old_qty": "0.54796447",
    "new_qty": "0.821946705",
    "old_rate": "1",
    "new_rate": "1.5",
    "ex_date": "2026-02-27",
    "record_date": "2026-02-12",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-26",
    "position_date": "2026-02-26",
    "due_bill_redemption_date": "2026-02-27"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "SPLIT",
  "activity_subtype": "FSPLIT",
  "qty": "0.821946705",
  "price": "41.5467",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T17:00:00Z",
  "settle_date": "2026-02-26",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3038297",
    "symbol": "SF",
    "old_qty": "0.54796447",
    "new_qty": "0.821946705",
    "old_rate": "1",
    "new_rate": "1.5",
    "ex_date": "2026-02-27",
    "record_date": "2026-02-12",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-26",
    "position_date": "2026-02-26",
    "due_bill_redemption_date": "2026-02-27"
  }
}
```
```json SPLIT (RSPLIT)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "SPLIT",
  "activity_subtype": "RSPLIT",
  "qty": "-33",
  "price": "7",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T05:00:00Z",
  "settle_date": "2026-02-27",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3049682",
    "symbol": "XRPT",
    "old_qty": "33",
    "new_qty": "1.65",
    "old_rate": "20",
    "new_rate": "1",
    "ex_date": "2026-02-27",
    "record_date": "2026-02-27",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-27",
    "position_date": "2026-02-26"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "SPLIT",
  "activity_subtype": "RSPLIT",
  "qty": "1.65",
  "price": "140",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T05:00:00Z",
  "settle_date": "2026-02-27",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3049682",
    "symbol": "XRPT",
    "old_qty": "33",
    "new_qty": "1.65",
    "old_rate": "20",
    "new_rate": "1",
    "ex_date": "2026-02-27",
    "record_date": "2026-02-27",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-27",
    "position_date": "2026-02-26"
  }
}
```
```json SPLIT (USPLIT)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "SPLIT",
  "activity_subtype": "USPLIT",
  "qty": "-8",
  "price": "26.31",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-17T17:00:00Z",
  "settle_date": "2026-02-17",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "CCCXU",
    "new_symbol": "INFQ",
    "alternate_symbol": "INFQ.WS",
    "old_qty": "8",
    "new_qty": "8",
    "alternate_qty": "2",
    "old_rate": "1",
    "new_rate": "1",
    "alternate_rate": "0.25",
    "system_date": "2026-02-17",
    "payable_date": "2026-02-17",
    "position_date": "2026-02-13",
    "effective_date": "2026-02-17"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "SPLIT",
  "activity_subtype": "USPLIT",
  "qty": "8",
  "price": "26.31",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-17T17:00:00Z",
  "settle_date": "2026-02-17",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "CCCXU",
    "new_symbol": "INFQ",
    "alternate_symbol": "INFQ.WS",
    "old_qty": "8",
    "new_qty": "8",
    "alternate_qty": "2",
    "old_rate": "1",
    "new_rate": "1",
    "alternate_rate": "0.25",
    "system_date": "2026-02-17",
    "payable_date": "2026-02-17",
    "position_date": "2026-02-13",
    "effective_date": "2026-02-17"
  }
}

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-3>",
  "ref_id": "<REFID-3>",
  "activity_type": "SPLIT",
  "activity_subtype": "USPLIT",
  "qty": "2",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-17T17:00:00Z",
  "settle_date": "2026-02-17",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "CCCXU",
    "new_symbol": "INFQ",
    "alternate_symbol": "INFQ.WS",
    "old_qty": "8",
    "new_qty": "8",
    "alternate_qty": "2",
    "old_rate": "1",
    "new_rate": "1",
    "alternate_rate": "0.25",
    "system_date": "2026-02-17",
    "payable_date": "2026-02-17",
    "position_date": "2026-02-13",
    "effective_date": "2026-02-17"
  }
}
```
```json SPIN
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "SPIN",
  "qty": "0.2",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T14:00:08.514798Z",
  "executed_at": "2026-02-27T17:00:00Z",
  "settle_date": "2026-02-26",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3044458",
    "new_symbol": "RNA",
    "source_symbol": "RNAM",
    "new_qty": "0.2",
    "source_qty": "2",
    "new_rate": "0.1",
    "source_rate": "1",
    "new_price": "0",
    "source_price": "72.82",
    "ex_date": "2026-02-27",
    "record_date": "2026-02-12",
    "system_date": "2026-02-27",
    "payable_date": "2026-02-26",
    "position_date": "2026-02-26",
    "due_bill_redemption_date": "2026-02-27"
  }
}
```
```json FIMAT
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "FIMAT",
  "qty": "-1000",
  "price": "100",
  "currency": "USD",
  "net_amount": "1000",
  "status": "executed",
  "at": "2026-01-15T17:00:08.514798Z",
  "executed_at": "2026-01-15T17:00:00Z",
  "settle_date": "2026-01-15",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "qty": "1000",
    "cash_payout": "1000",
    "system_date": "2026-01-15",
    "payment_date": "2026-01-15"
  }
}
```
```json VOF (VDST)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "VOF",
  "activity_subtype": "VDST",
  "qty": "9.975695601",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-12T17:00:08.514798Z",
  "executed_at": "2026-01-12T17:00:00Z",
  "settle_date": "2026-01-05",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3018482",
    "new_symbol": "HYT.RT",
    "source_symbol": "HYT",
    "new_qty": "9.975695601",
    "source_qty": "9.975695601",
    "rate": "1",
    "ex_date": "2026-01-02",
    "record_date": "2026-01-02",
    "system_date": "2026-01-12",
    "payable_date": "2026-01-05",
    "position_date": "2025-12-31",
    "expiration_date": "2026-01-26"
  }
}
```
```json REORG (WRM)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "REORG",
  "activity_subtype": "WRM",
  "qty": "-200",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-15T17:00:08.514798Z",
  "executed_at": "2026-01-15T17:00:00Z",
  "settle_date": "2026-01-15",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "CLNNW",
    "removed_qty": "200",
    "system_date": "2026-01-15",
    "position_date": "2026-01-14"
  }
}
```
```json OP(ASN, EXC, EXP, TRD)
# options - non corporate action related types: OPASN, OPEXC, OPEXP, OPTRD
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "OPASN",
  "qty": "14",
  "price": "0",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-14T21:00:08.514798Z",
  "executed_at": "2026-01-14T21:00:00Z",
  "settle_date": "2026-01-14",
  "details": {
    "group_id": "<GRPID>",
    "system_date": "2026-01-14"
  }
}
```
```json OPCA (DIV.CDIV)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.CDIV",
  "qty": "-7",
  "price": "0.19",
  "currency": "USD",
  "net_amount": "133",
  "status": "executed",
  "at": "2026-07-13T08:25:15.080016Z",
  "executed_at": "2026-07-13T16:00:00Z",
  "settle_date": "2026-07-13",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "FIZZ",
    "cusip": "635017106",
    "old_contract_symbol": "FIZZ260717P00030000",
    "new_contract_symbol": "FIZZ260717P00026750",
    "qty": "7",
    "rate": "3.25",
    "foreign": "false",
    "special": "true",
    "ex_date": "2026-07-13",
    "record_date": "2026-07-13",
    "system_date": "2026-07-13",
    "payable_date": "2026-07-30",
    "position_date": "2026-07-10"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.CDIV",
  "qty": "7",
  "price": "0.19",
  "currency": "USD",
  "net_amount": "-133",
  "status": "executed",
  "at": "2026-07-13T08:25:19.214049Z",
  "executed_at": "2026-07-13T16:00:00Z",
  "settle_date": "2026-07-13",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "FIZZ",
    "cusip": "635017106",
    "old_contract_symbol": "FIZZ260717P00030000",
    "new_contract_symbol": "FIZZ260717P00026750",
    "qty": "7",
    "rate": "3.25",
    "foreign": "false",
    "special": "true",
    "ex_date": "2026-07-13",
    "record_date": "2026-07-13",
    "system_date": "2026-07-13",
    "payable_date": "2026-07-30",
    "position_date": "2026-07-10"
  }
}
```
```json OPCA (DIV.SDIV)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.SDIV",
  "qty": "-2",
  "price": "0.2",
  "currency": "USD",
  "net_amount": "40",
  "status": "executed",
  "at": "2025-12-29T10:00:11.144201Z",
  "executed_at": "2025-12-29T17:00:00Z",
  "settle_date": "2025-12-29",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3019202",
    "symbol": "ITUB",
    "cusip": "465562106",
    "old_contract_symbol": "ITUB260116C00008000",
    "new_contract_symbol": "ITUB2260116C00007770",
    "qty": "2",
    "rate": "1.03",
    "ex_date": "2025-12-29",
    "record_date": "2025-12-29",
    "system_date": "2025-12-29",
    "payable_date": "2025-12-31",
    "position_date": "2025-12-26"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.SDIV",
  "qty": "2",
  "price": "0.1942",
  "currency": "USD",
  "net_amount": "-40.01",
  "status": "executed",
  "at": "2025-12-29T10:00:16.145582Z",
  "executed_at": "2025-12-29T17:00:00Z",
  "settle_date": "2025-12-29",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3019202",
    "symbol": "ITUB",
    "cusip": "465562106",
    "old_contract_symbol": "ITUB260116C00008000",
    "new_contract_symbol": "ITUB2260116C00007770",
    "qty": "2",
    "rate": "1.03",
    "ex_date": "2025-12-29",
    "record_date": "2025-12-29",
    "system_date": "2025-12-29",
    "payable_date": "2025-12-31",
    "position_date": "2025-12-26"
  }
}
```
```json OPCA (DIV.ROC)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.ROC",
  "qty": "-5",
  "price": "0.15",
  "currency": "USD",
  "net_amount": "75",
  "status": "executed",
  "at": "2026-04-28T08:11:14.996362Z",
  "executed_at": "2026-04-28T16:00:00Z",
  "settle_date": "2026-04-28",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "VISN260515P00016000",
    "new_contract_symbol": "VISN1260515P00016000",
    "qty": "5",
    "system_date": "2026-04-28",
    "position_date": "2026-04-27"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "DIV.ROC",
  "qty": "5",
  "price": "0.15",
  "currency": "USD",
  "net_amount": "-75",
  "status": "executed",
  "at": "2026-04-28T08:11:14.996362Z",
  "executed_at": "2026-04-28T16:00:00Z",
  "settle_date": "2026-04-28",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "VISN260515P00016000",
    "new_contract_symbol": "VISN1260515P00016000",
    "qty": "5",
    "system_date": "2026-04-28",
    "position_date": "2026-04-27"
  }
}
```
```json OPCA (MA.SMA)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "MA.SMA",
  "qty": "-3",
  "price": "0.65",
  "currency": "USD",
  "net_amount": "195",
  "status": "executed",
  "at": "2026-05-12T10:51:14.881163Z",
  "executed_at": "2026-05-12T16:00:00Z",
  "settle_date": "2026-05-12",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3017560",
    "acquiree_symbol": "UDMY",
    "acquirer_symbol": "COUR",
    "acquiree_cusip": "902685106",
    "acquirer_cusip": "22266M104",
    "old_contract_symbol": "UDMY260821C00005000",
    "new_contract_symbol": "COUR1260821C00005000",
    "qty": "3",
    "acquiree_rate": "1",
    "acquirer_rate": "0.8",
    "system_date": "2026-05-12",
    "payable_date": "2026-05-12",
    "position_date": "2026-05-11",
    "effective_date": "2026-05-11"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "MA.SMA",
  "qty": "3",
  "price": "0.65",
  "currency": "USD",
  "net_amount": "-195",
  "status": "executed",
  "at": "2026-05-12T10:51:21.103005Z",
  "executed_at": "2026-05-12T16:00:00Z",
  "settle_date": "2026-05-12",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3017560",
    "acquiree_symbol": "UDMY",
    "acquirer_symbol": "COUR",
    "acquiree_cusip": "902685106",
    "acquirer_cusip": "22266M104",
    "old_contract_symbol": "UDMY260821C00005000",
    "new_contract_symbol": "COUR1260821C00005000",
    "qty": "3",
    "acquiree_rate": "1",
    "acquirer_rate": "0.8",
    "system_date": "2026-05-12",
    "payable_date": "2026-05-12",
    "position_date": "2026-05-11",
    "effective_date": "2026-05-11"
  }
}
```
```json OPCA (MA.SCMA)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "MA.SCMA",
  "qty": "-20",
  "price": "2.01",
  "currency": "USD",
  "net_amount": "4020",
  "status": "executed",
  "at": "2026-06-02T10:04:35.420592Z",
  "executed_at": "2026-06-02T16:00:00Z",
  "settle_date": "2026-06-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "THR261120C00090000",
    "new_contract_symbol": "CECO1261120C00090000",
    "qty": "20",
    "system_date": "2026-06-02",
    "position_date": "2026-06-01"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "MA.SCMA",
  "qty": "20",
  "price": "2.01",
  "currency": "USD",
  "net_amount": "-4020",
  "status": "executed",
  "at": "2026-06-02T10:04:35.420592Z",
  "executed_at": "2026-06-02T16:00:00Z",
  "settle_date": "2026-06-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "THR261120C00090000",
    "new_contract_symbol": "CECO1261120C00090000",
    "qty": "20",
    "system_date": "2026-06-02",
    "position_date": "2026-06-01"
  }
}
```
```json OPCA (NC.SNC)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.SNC",
  "qty": "-1",
  "price": "29.1",
  "currency": "USD",
  "net_amount": "2910",
  "status": "executed",
  "at": "2026-06-24T08:40:37.427535Z",
  "executed_at": "2026-06-24T16:00:00Z",
  "settle_date": "2026-06-24",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "SATS",
    "new_symbol": "ECHO",
    "old_cusip": "278768106",
    "new_cusip": "278768106",
    "old_contract_symbol": "SATS271217C00120000",
    "new_contract_symbol": "ECHO271217C00120000",
    "qty": "1",
    "system_date": "2026-06-24",
    "position_date": "2026-06-23"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.SNC",
  "qty": "1",
  "price": "29.1",
  "currency": "USD",
  "net_amount": "-2910",
  "status": "executed",
  "at": "2026-06-24T08:40:46.012399Z",
  "executed_at": "2026-06-24T16:00:00Z",
  "settle_date": "2026-06-24",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "SATS",
    "new_symbol": "ECHO",
    "old_cusip": "278768106",
    "new_cusip": "278768106",
    "old_contract_symbol": "SATS271217C00120000",
    "new_contract_symbol": "ECHO271217C00120000",
    "qty": "1",
    "system_date": "2026-06-24",
    "position_date": "2026-06-23"
  }
}
```
```json OPCA (NC.CNC)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.CNC",
  "qty": "-4",
  "price": "0.22",
  "currency": "USD",
  "net_amount": "88",
  "status": "executed",
  "at": "2025-09-29T07:21:46.420695Z",
  "executed_at": "2025-09-29T16:00:00Z",
  "settle_date": "2025-09-29",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "WOLF",
    "new_symbol": "WOLF",
    "old_cusip": "977852102",
    "new_cusip": "97785W106",
    "old_contract_symbol": "WOLF260116C00002000",
    "new_contract_symbol": "WOLF1260116C00002000",
    "qty": "4",
    "system_date": "2025-09-29",
    "position_date": "2025-09-26"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.CNC",
  "qty": "4",
  "price": "0.22",
  "currency": "USD",
  "net_amount": "-88",
  "status": "executed",
  "at": "2025-09-29T07:22:37.461371Z",
  "executed_at": "2025-09-29T16:00:00Z",
  "settle_date": "2025-09-29",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "WOLF",
    "new_symbol": "WOLF",
    "old_cusip": "977852102",
    "new_cusip": "97785W106",
    "old_contract_symbol": "WOLF260116C00002000",
    "new_contract_symbol": "WOLF1260116C00002000",
    "qty": "4",
    "system_date": "2025-09-29",
    "position_date": "2025-09-26"
  }
}
```
```json OPCA (NC.SCNC)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.SCNC",
  "qty": "-1",
  "price": "3.7",
  "currency": "USD",
  "net_amount": "370",
  "status": "executed",
  "at": "2026-04-06T08:23:56.397116Z",
  "executed_at": "2026-04-06T16:00:00Z",
  "settle_date": "2026-04-06",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "BITF",
    "new_symbol": "KEEL",
    "old_cusip": "09173B107",
    "new_cusip": "486917107",
    "old_contract_symbol": "BITF270115C00000500",
    "new_contract_symbol": "KEEL270115C00000500",
    "qty": "1",
    "system_date": "2026-04-06",
    "position_date": "2026-04-02"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "NC.SCNC",
  "qty": "1",
  "price": "3.7",
  "currency": "USD",
  "net_amount": "-370",
  "status": "executed",
  "at": "2026-04-06T08:23:56.397116Z",
  "executed_at": "2026-04-06T16:00:00Z",
  "settle_date": "2026-04-06",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "BITF",
    "new_symbol": "KEEL",
    "old_cusip": "09173B107",
    "new_cusip": "486917107",
    "old_contract_symbol": "BITF270115C00000500",
    "new_contract_symbol": "KEEL270115C00000500",
    "qty": "1",
    "system_date": "2026-04-06",
    "position_date": "2026-04-02"
  }
}
```
```json OPCA (SPIN)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "SPIN",
  "qty": "-1",
  "price": "8.36",
  "currency": "USD",
  "net_amount": "836",
  "status": "executed",
  "at": "2026-07-01T09:42:22.981030Z",
  "executed_at": "2026-07-01T04:00:00Z",
  "settle_date": "2026-07-01",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "new_symbol": "MBGL",
    "source_symbol": "SPGI",
    "new_cusip": "60744M106",
    "source_cusip": "78409V104",
    "old_contract_symbol": "SPGI260821C00470000",
    "new_contract_symbol": "SPGI1260821C00470000",
    "qty": "-1",
    "new_rate": "1",
    "source_rate": "1",
    "new_price": "22.05",
    "source_price": "407.26",
    "ex_date": "2026-07-01",
    "record_date": "2026-06-15",
    "system_date": "2026-07-01",
    "payable_date": "2026-07-01",
    "position_date": "2026-06-30"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "SPIN",
  "qty": "1",
  "price": "8.36",
  "currency": "USD",
  "net_amount": "-836",
  "status": "executed",
  "at": "2026-07-01T09:42:22.981030Z",
  "executed_at": "2026-07-01T04:00:00Z",
  "settle_date": "2026-07-01",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "new_symbol": "MBGL",
    "source_symbol": "SPGI",
    "new_cusip": "60744M106",
    "source_cusip": "78409V104",
    "old_contract_symbol": "SPGI260821C00470000",
    "new_contract_symbol": "SPGI1260821C00470000",
    "qty": "-1",
    "new_rate": "1",
    "source_rate": "1",
    "new_price": "22.05",
    "source_price": "407.26",
    "ex_date": "2026-07-01",
    "record_date": "2026-06-15",
    "system_date": "2026-07-01",
    "payable_date": "2026-07-01",
    "position_date": "2026-06-30"
  }
}
```
```json OPCA (SPLIT.FSPLIT)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.FSPLIT",
  "qty": "-1",
  "price": "1.07",
  "currency": "USD",
  "net_amount": "107",
  "status": "executed",
  "at": "2026-07-15T08:23:48.523132Z",
  "executed_at": "2026-07-15T16:00:00Z",
  "settle_date": "2026-07-14",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3102892",
    "symbol": "KORU",
    "old_cusip": "25461A387",
    "new_cusip": "25461A387",
    "old_contract_symbol": "KORU260717C01700000",
    "new_contract_symbol": "KORU260717C00085000",
    "old_qty": "1",
    "new_qty": "20",
    "old_rate": "1",
    "new_rate": "20",
    "ex_date": "2026-07-15",
    "record_date": "2026-07-13",
    "system_date": "2026-07-15",
    "payable_date": "2026-07-14",
    "position_date": "2026-07-15",
    "due_bill_redemption_date": "2026-07-15"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.FSPLIT",
  "qty": "20",
  "price": "0.05",
  "currency": "USD",
  "net_amount": "-100",
  "status": "executed",
  "at": "2026-07-15T08:23:53.983324Z",
  "executed_at": "2026-07-15T16:00:00Z",
  "settle_date": "2026-07-14",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3102892",
    "symbol": "KORU",
    "old_cusip": "25461A387",
    "new_cusip": "25461A387",
    "old_contract_symbol": "KORU260717C01700000",
    "new_contract_symbol": "KORU260717C00085000",
    "old_qty": "1",
    "new_qty": "20",
    "old_rate": "1",
    "new_rate": "20",
    "ex_date": "2026-07-15",
    "record_date": "2026-07-13",
    "system_date": "2026-07-15",
    "payable_date": "2026-07-14",
    "position_date": "2026-07-15",
    "due_bill_redemption_date": "2026-07-15"
  }
}
```
```json OPCA (SPLIT.RSPLIT)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.RSPLIT",
  "qty": "-454",
  "price": "0.83",
  "currency": "USD",
  "net_amount": "37682",
  "status": "executed",
  "at": "2026-07-15T13:52:50.100451Z",
  "executed_at": "2026-07-15T16:00:00Z",
  "settle_date": "2026-07-15",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3102961",
    "symbol": "SOXS",
    "old_cusip": "25461H572",
    "new_cusip": "25461H291",
    "old_contract_symbol": "SOXS260821C00005000",
    "new_contract_symbol": "SOXS2260821C00005000",
    "qty": "454",
    "old_rate": "10",
    "new_rate": "1",
    "ex_date": "2026-07-15",
    "record_date": "2026-07-15",
    "system_date": "2026-07-15",
    "payable_date": "2026-07-15",
    "position_date": "2026-07-15"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.RSPLIT",
  "qty": "454",
  "price": "0.83",
  "currency": "USD",
  "net_amount": "-37682",
  "status": "executed",
  "at": "2026-07-15T13:53:25.520705Z",
  "executed_at": "2026-07-15T16:00:00Z",
  "settle_date": "2026-07-15",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "3102961",
    "symbol": "SOXS",
    "old_cusip": "25461H572",
    "new_cusip": "25461H291",
    "old_contract_symbol": "SOXS260821C00005000",
    "new_contract_symbol": "SOXS2260821C00005000",
    "qty": "454",
    "old_rate": "10",
    "new_rate": "1",
    "ex_date": "2026-07-15",
    "record_date": "2026-07-15",
    "system_date": "2026-07-15",
    "payable_date": "2026-07-15",
    "position_date": "2026-07-15"
  }
}
```
```json OPCA (SPLIT.USPLIT)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.USPLIT",
  "qty": "-3",
  "price": "10",
  "currency": "USD",
  "net_amount": "3000",
  "status": "executed",
  "at": "2026-05-07T07:00:00.000000Z",
  "executed_at": "2026-05-07T16:00:00Z",
  "settle_date": "2026-05-07",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "PLTR",
    "new_symbol": "PLTT",
    "alternate_symbol": "PLTRX",
    "old_cusip": "69608A108",
    "new_cusip": "69608A109",
    "alternate_cusip": "74255L555",
    "old_contract_symbol": "PLTR260515C00165000",
    "new_contract_symbol": "PLTT1260515C00165000",
    "qty": "3",
    "old_rate": "1",
    "new_rate": "1",
    "alternate_rate": "1",
    "system_date": "2026-05-07",
    "position_date": "2026-05-06",
    "effective_date": "2026-05-07"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "SPLIT.USPLIT",
  "qty": "3",
  "price": "10",
  "currency": "USD",
  "net_amount": "-3000",
  "status": "executed",
  "at": "2026-05-07T07:00:00.000000Z",
  "executed_at": "2026-05-07T16:00:00Z",
  "settle_date": "2026-05-07",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_symbol": "PLTR",
    "new_symbol": "PLTT",
    "alternate_symbol": "PLTRX",
    "old_cusip": "69608A108",
    "new_cusip": "69608A109",
    "alternate_cusip": "74255L555",
    "old_contract_symbol": "PLTR260515C00165000",
    "new_contract_symbol": "PLTT1260515C00165000",
    "qty": "3",
    "old_rate": "1",
    "new_rate": "1",
    "alternate_rate": "1",
    "system_date": "2026-05-07",
    "position_date": "2026-05-06",
    "effective_date": "2026-05-07"
  }
}
```
```json OPCA (VOF.VDST)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "VOF.VDST",
  "qty": "-1",
  "price": "0.23",
  "currency": "USD",
  "net_amount": "23",
  "status": "executed",
  "at": "2026-07-06T11:40:36.859065Z",
  "executed_at": "2026-07-06T16:00:00Z",
  "settle_date": "2026-07-06",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "EOSE260717P00005000",
    "new_contract_symbol": "EOSE1260717P00005000",
    "qty": "1",
    "system_date": "2026-07-06",
    "position_date": "2026-07-02"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "VOF.VDST",
  "qty": "1",
  "price": "0.23",
  "currency": "USD",
  "net_amount": "-23",
  "status": "executed",
  "at": "2026-07-06T11:40:36.859065Z",
  "executed_at": "2026-07-06T16:00:00Z",
  "settle_date": "2026-07-06",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "EOSE260717P00005000",
    "new_contract_symbol": "EOSE1260717P00005000",
    "qty": "1",
    "system_date": "2026-07-06",
    "position_date": "2026-07-02"
  }
}
```
```json OPCA (CADJ)
# old contract removal leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "OPCA",
  "activity_subtype": "CADJ",
  "qty": "-1",
  "price": "0.69",
  "currency": "USD",
  "net_amount": "69",
  "status": "executed",
  "at": "2026-07-23T08:46:42.453905Z",
  "executed_at": "2026-07-23T16:00:00Z",
  "settle_date": "2026-07-23",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "EOSE1260731C00005500",
    "new_contract_symbol": "EOSE260731C00005500",
    "qty": "1",
    "system_date": "2026-07-23",
    "position_date": "2026-07-22"
  }
}

# new contract creation leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "OPCA",
  "activity_subtype": "CADJ",
  "qty": "1",
  "price": "0.69",
  "currency": "USD",
  "net_amount": "-69",
  "status": "executed",
  "at": "2026-07-23T08:49:32.667749Z",
  "executed_at": "2026-07-23T16:00:00Z",
  "settle_date": "2026-07-23",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "old_contract_symbol": "EOSE1260731C00005500",
    "new_contract_symbol": "EOSE260731C00005500",
    "qty": "1",
    "system_date": "2026-07-23",
    "position_date": "2026-07-22"
  }
}
```
```json FOPT
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "FOPT",
  "qty": "10",
  "price": "100",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-01-14T02:00:08.514798Z",
  "executed_at": "2026-01-14T17:33:52.409539Z",
  "settle_date": "2026-01-14",
  "details": {
    "external_id": "DEF5GRE2E5CW1F09",
    "contra": "00000632",
    "symbol": "IBM",
    "system_date": "2026-01-14"
  }
}
```
```json MEM
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "MEM",
  "qty": "42",
  "price": "42",
  "currency": "USD",
  "net_amount": "1764",
  "status": "executed",
  "at": "2026-01-14T02:00:08.514798Z",
  "executed_at": "2025-09-03T16:04:00.512126999Z",
  "settle_date": "2025-09-03",
    "details": {
    "transfer_id": "63febd60-51ad-4b90-b9a5-f4553972154d",
    "system_date": "2025-09-03",
    "group_id": "cebd684a-0f6a-4437-8435-0c99af5f86a9"
  },
}
```
```json CGD
// A CGD event could have 1 leg or 2 legs, because it can have either the LTCG/STCG subtype or both subtypes. 
// LTCG leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "CGD",
  "activity_subtype": "LTCG",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "45.86",
  "status": "executed",
  "at": "2026-01-09T14:00:00.123456Z",
  "executed_at": "2026-01-09T16:00:00Z",
  "settle_date": "2026-01-09",
  "details": {
    "ca_id":  "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "GCAD",
    "cusip": "36261K509",
    "entitled_qty": "100",
    "cash_payout": "45.855",
    "rate": "0.45855",
    "long_term_rate": "0.45855",
    "short_term_rate": "0.11019",
    "ex_date": "2025-12-26",
    "record_date": "2025-12-29",
    "payable_date": "2026-01-09",
    "position_date": "2025-12-26",
    "system_date": "2026-01-09"
  }
}

// STCG leg
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "CGD",
  "activity_subtype": "STCG",
  "qty": "0",
  "price": "0",
  "currency": "USD",
  "net_amount": "11.02",
  "status": "executed",
  "at": "2026-01-09T14:00:00.456789Z",
  "executed_at": "2026-01-09T16:00:00Z",
  "settle_date": "2026-01-09",
  "details": {
    "ca_id":  "<CAID>",
    "group_id": "<GRPID>",
    "symbol": "GCAD",
    "cusip": "36261K509",
    "isin": "US36261K5090",
    "entitled_qty": "100",
    "cash_payout": "1.1019",
    "rate": "0.11019",
    "short_term_rate": "0.11019",
    "ex_date": "2025-12-26",
    "record_date": "2025-12-29",
    "payable_date": "2026-01-09",
    "position_date": "2025-12-26",
    "system_date": "2026-01-09"
  }
}
```
```json REO (REOS)
// A stock-only reorganization emits one SSE event per leg.
// Example: stock only, 1-for-1 exchange (CEPT → SECZ). Example: 50 CEPT shares convert 1:1 into 50 SECZ shares.
// Leg 1 — remove source shares (details.removed_qty = 50) 
{
  ...
  "activity_type": "REO",
  "activity_subtype": "REOS",
  "qty": "-50",
  "net_amount": "0",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_isin": "US1234567890",
    "removed_qty": "50",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}

// Leg 2 — add destination shares
{
  ...
  "activity_type": "REO",
  "activity_subtype": "REOS",
  "qty": "50",
  "net_amount": "0",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_isin": "US1234567890",
    "source_qty": "50",
    "symbol": "SECZ",
    "cusip": "98765Z432",
    "isin": "US9876543210", 
    "source_rate": "1",
    "new_rate": "1",
    "qty": "50",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}

// It's possible to have multi-leg variant that add shares for more than one symbol. For example, three legs: 
// - removal (−50 CEPT) - example above
// - add SECZ (+50) - example above 
// - add SPNA (+10) - described below 

// Leg 3 — adds second target shares (SPNA)
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-3>",
  "ref_id": "<REFID-3>",
  "activity_type": "REO",
  "activity_subtype": "REOS",
  "qty": "10",
  "price": "63.45",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id":  "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_isin": "US1234567890",
    "source_qty": "50",
    "symbol": "SPNA",
    "cusip": "55555Q111",
    "isin": "US55555Q111",
    "source_rate": "1",
    "new_rate": "0.2",
    "qty": "10",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}
```
```json REO (REOC)
// Example: cash only ($10.00/share cash-out)
// Cash-only reorganization. No new stock-leg fields.
// 50 shares at $10.00/share → $500 cash payout.

{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "REO",
  "activity_subtype": "REOC",
  "qty": "-50",
  "price": "10.00",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "removed_qty": "50",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}

// Leg 2 - add cash
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID>",
  "ref_id": "<REFID>",
  "activity_type": "REO",
  "activity_subtype": "REOC",
  "qty": "0",
  "currency": "USD",
  "net_amount": "500",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_qty": "50",
    "cash_rate": "10",
    "cash_payout": "500",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}
```
```json REO (REOSC)
// Example: stock and cash. Mixed consideration: 50 CEPT → 25 SECZ + $150 cash.
// 3 events

// leg 1 - remove shares 
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-1>",
  "ref_id": "<REFID-1>",
  "activity_type": "REO",
  "activity_subtype": "REOSC",
  "qty": "-50",
  "price": "12.69",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_isin": "US1234567890",
    "removed_qty": "50",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}

// leg 2 - add cash
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-2>",
  "ref_id": "<REFID-2>",
  "activity_type": "REO",
  "activity_subtype": "REOSC",
  "qty": "0",
  "currency": "USD",
  "net_amount": "150",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_qty": "50",
    "cash_rate": "3",
    "cash_payout": "150",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}

// leg 3 - add shares
{
  "account_id": "<ACCID>",
  "event_id": "<EVTID-3>",
  "ref_id": "<REFID-3>",
  "activity_type": "REO",
  "activity_subtype": "REOSC",
  "qty": "25",
  "price": "12.69",
  "currency": "USD",
  "net_amount": "0",
  "status": "executed",
  "at": "2026-07-02T04:00:08.514798Z",
  "executed_at": "2026-07-02T04:00:00Z",
  "settle_date": "2026-07-02",
  "details": {
    "ca_id": "<CAID>",
    "group_id": "<GRPID>",
    "reorg_id": "12345",
    "source_symbol": "CEPT",
    "source_cusip": "12345A678",
    "source_isin": "US1234567890",
    "source_qty": "50",
    "symbol": "SECZ",
    "cusip": "98765Z432",
    "isin": "US9876543210",
    "source_rate": "1",
    "new_rate": "0.5",
    "qty": "25",
    "effective_date": "2026-07-02",
    "payable_date": "2026-07-02",
    "position_date": "2026-07-02",
    "system_date": "2026-07-02"
  }
}
```

**Important Note**

Some activity types (listed below) are missing from the samples. We are working on adding these samples as soon as these activities are processed in our production environment.

* VOF/VTND
* VOF/VWRT
* VOF/VRGT
* VOF/VEXH

***

## Best Practices

### Idempotent Processing

You may receive duplicate events during reconnection. Use `ref_id` as your deduplication key. Before applying an event, check if you have already processed an activity with that `ref_id`.

### Reconnection Strategy

* Implement automatic reconnection with exponential backoff.
* Always reconnect using `since_id` set to the last successfully processed `event_id`.
* When reconnecting for reconciliation purposes, set `since` to a few minutes before your last processed event's timestamp to account for potential ordering edge cases.

### Account Scope

The Activity SSE streams events for all accounts under your correspondent, including firm accounts — not only customer accounts.

### Message Ordering

* **Per-account ordering is guaranteed.** If event E1 arrives before E2 for the same account, E1 happened first.
* **Cross-account ordering is NOT guaranteed.** Use the `at` or `event_id` fields to determine ordering across accounts.

### Event Ordering vs. Business Time

The `event_id` (ULID) and the `at` field encode different timestamps:

* `at` is the business event timestamp — when the activity actually occurred in the source system.
* `event_id` (ULID) encodes the publish sequence timestamp — when the event was appended to the internal activities stream. This governs the order in which events are delivered and replayed.

In normal operation these are nearly identical. However, they can diverge during infrastructure delays or backfills. If Alpaca backfills a historical activity, it will appear at the end of the `event_id` sequence (reflecting when it was published), even though its `at` value reflects the original business time.

The since and until query parameters filter by the business timestamp (`at`). A query with `since=2026-01-15T00:00:00Z&until=2026-01-16T00:00:00Z` returns events that may include activities whose `event_id` value is outside this range, and was only delivered later due to backfills..

For cursor-based replay, always use `since_id` with the last processed `event_id`. The `since`/`until` timestamp parameters are best suited for reconcilliation and broad historical queries, not for gap-free resumption. If you specify `since`, you also need to specify `until` - while `since_id` lets you leave the end date open, and transition to live consumption.

### Timestamp Encoding

`since` and `until` parameters accept RFC 3339 timestamps with timezone. The `+` character in timezone offsets (e.g., `+07:00`) must be URL-encoded as `%2B`:

```
/v2beta1/events/activities?since=2026-01-02T15:04:05%2B07:00
```

### Consumer Performance

If your consumer cannot keep up with the event rate, the server will drop messages and send a comment: `: you are reading too slowly, dropped N messages`. To avoid this:

* Process events asynchronously — read from the stream into a buffer, and process from the buffer.
* Avoid blocking I/O (e.g., synchronous database writes) in your stream reader loop.
* For customers with large event volumes, we also offer sharded streaming. Please contact us.

### SSE Delivery vs. Balance and Position Queries

The Activity SSE delivers events as soon as they are booked in the ledger. Balance and position queries (e.g., the Trading Account or Account Portfolio endpoints) may not reflect the activity immediately because they depend on separate intraday adjustment processes.

Do not assume that receiving an activity event means the account's balance or position has already been updated in query endpoints. If your workflow reacts to an SSE event by checking a balance, build in a polling or retry mechanism to account for the propagation delay.

***