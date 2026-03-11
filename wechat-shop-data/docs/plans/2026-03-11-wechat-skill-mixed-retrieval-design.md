# WeChat Shop Skill Mixed Retrieval Design

## Goal

Optimize the `wechat-shop-data` skill for mixed interactive and export workloads so it behaves consistently across models and avoids model-dependent performance swings.

## Problem

Several WeChat Shop APIs return only IDs in list responses:

- orders: `getorderlist`, `searchorder`
- products: `getproductlist`
- gift products: `getgiftproductlist`

The complete business fields live behind per-ID detail endpoints. If a model is allowed to improvise the retrieval strategy, one model may do summary-first retrieval while another may eagerly fan out into hundreds or thousands of detail calls. That creates large latency variance and poor operational predictability.

## Design Principles

1. Move retrieval policy out of model judgment and into fixed skill rules.
2. Separate intent classification from API execution strategy.
3. Use batch-friendly APIs whenever they exist.
4. Default to fast summary responses for interactive requests.
5. Reserve full detail expansion for explicit export or deep-detail tasks.
6. Make pagination, concurrency, retry, and continuation rules explicit.

## Retrieval Modes

### 1. `summary_only`

Use for overview questions, counts, status summaries, and recent-list requests.

Behavior:

- call list/search APIs only
- return IDs, counts, statuses, and pagination context
- do not auto-expand all details
- optionally expand a very small sample only when required to answer the question

### 2. `detail_on_demand`

Use when the request needs complete fields for a small matched set.

Behavior:

- collect IDs from list/search results
- expand details only for the bounded result set
- use explicit caps to prevent accidental large fan-out

### 3. `full_export`

Use for monthly exports, audits, warehousing, reconciliation, and reporting.

Behavior:

- collect all IDs page by page
- de-duplicate IDs
- fan out to detail endpoints using fixed chunking and concurrency limits
- support continuation and cache guidance

## Deterministic Expansion Rules

The skill should not let the model decide expansion style freely.

Suggested defaults:

- matched records `<= 20`: allow automatic detail expansion
- matched records `21-200`: summarize first, then offer or explicitly enter bounded detail expansion
- matched records `> 200`: treat as batch/export workflow, not conversational synchronous expansion

These thresholds make response behavior stable across models.

## Domain Strategy Matrix

### Orders

- list/search stage: `getorderlist`, `searchorder`
- detail stage: `getorder`
- monthly queries must use time slicing because list windows cannot exceed 7 days

### Products

- list stage: `getproductlist`
- detail stage: `getproduct`

### Gift Products

- list stage: `getgiftproductlist`
- detail stage: `getgiftproduct`

### Stock

- prefer `batchgetstock`
- do not recommend per-SKU `getstock` loops for bulk inventory views unless the user explicitly asks for a single SKU lookup

### Marketing Tasks

- consume list output directly unless a separate detail endpoint is later introduced

## Full Export Workflow

For order exports:

1. Split the requested date range into 7-day windows.
2. Page through each window using `next_key`.
3. Merge and de-duplicate all IDs.
4. Partition IDs into fixed chunks.
5. Process detail calls with bounded concurrency.
6. Retry recoverable failures with backoff.
7. Return progress and final structured export output.

Recommended execution guidance:

- chunk size: 20-50 IDs
- concurrency: 5-10 detail calls at a time
- backoff: exponential or stepped reduction after rate-limit errors

The exact numbers can remain guidance text in the skill, but the principle must be explicit.

## Response Contract

All query responses should prefer this structure:

- retrieval mode
- APIs used
- filters and time window
- IDs collected or record counts
- whether detail expansion was performed
- pagination state
- estimated next step

For large tasks, the skill should explicitly state whether the current answer is:

- summary-only
- partially expanded
- fully expanded

## Why This Reduces Model Variance

Model variance is reduced because:

- mode selection is rule-bound
- fan-out thresholds are fixed
- pagination behavior is fixed
- batch-first APIs are mandatory where available
- export tasks have a prescribed staged workflow

This turns the skill into a retrieval orchestrator rather than a loose set of API hints.
