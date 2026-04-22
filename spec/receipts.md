# Receipt Protocol

## Receipt Structure

Every action in the sovereignty stack produces a receipt. Each receipt contains exactly these fields:

| Field | Type | Description |
|-------|------|-------------|
| `receiptId` | string | Unique identifier. Format: `rcpt_{uuid}` |
| `timestamp` | string | UTC ISO 8601 timestamp of receipt creation |
| `layer` | string | Originating layer: `chip`, `continuity`, or `rio` |
| `eventType` | string | Event that produced this receipt |
| `objectHash` | string | SHA-256 hash of the receipt payload (sorted keys, UTF-8 encoded JSON) |
| `priorReceiptHash` | string or null | `objectHash` of the previous receipt in the chain. `null` for the first receipt. |
| `parentReceiptId` | string or null | `receiptId` of the previous receipt. `null` for the first receipt. |

## Hash Computation

The `objectHash` is computed as:

```
SHA-256( JSON.stringify(payload, sortKeys=true).encode("utf-8") )
```

The payload is the result object produced by the service at the time the receipt is created. The hash is represented as a lowercase hexadecimal string.

## Hash Chaining Rule

Each receipt links to the previous receipt via `priorReceiptHash`:

```
receipt[0].priorReceiptHash = null
receipt[n].priorReceiptHash = receipt[n-1].objectHash
```

This forms a single, ordered, hash-linked chain across all layers.

## Append-Only Constraint

The receipt chain is append-only:

- Receipts are never modified after creation.
- Receipts are never deleted.
- Receipts are never reordered.
- New receipts are always appended to the end of the chain.

## Verification Rule

A receipt chain is valid if and only if:

1. The first receipt has `priorReceiptHash` equal to `null`.
2. For every subsequent receipt at index `n`, `receipt[n].priorReceiptHash` equals `receipt[n-1].objectHash`.
3. No gaps exist in the chain.

If any of these conditions fail, the chain is invalid.

## Event Types

| Layer | Event Type | Trigger |
|-------|-----------|---------|
| `chip` | `evaluate` | Input classified |
| `continuity` | `store` | Preference stored |
| `continuity` | `contradiction` | Contradiction detected |
| `continuity` | `resolve` | Contradiction resolved |
| `rio` | `govern` | Governance decision made |
| `rio` | `execute` | Execution attempted |
