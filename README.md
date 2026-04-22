# RIO Sovereignty Stack

A reference implementation of the sovereignty stack: a layered architecture where human preferences govern AI action, and every decision produces a verifiable receipt.

## Core Invariant

No action executes without a governance decision. No governance decision is made with unresolved contradictions. Every step produces a receipt. The receipt chain is append-only and hash-linked.

## Architecture

```
Input → Digital Chip → Continuity Engine → RIO → Execution → Receipts
```

| Layer | Name | Responsibility |
|-------|------|---------------|
| 1 | Digital Chip | Classifies input. Admits preferences. Flags actions requiring approval. |
| 2 | Continuity Engine | Stores preferences. Detects and resolves contradictions. |
| 3 | RIO | Governs actions against preferences and contradictions. |
| 4 | Execution | Executes only if RIO allows. Otherwise blocks. |

All layers write to a single global receipt chain. The chain is append-only, hash-linked, and independently verifiable.

## Run the Demo

```
python demo/demo_sovereignty_stack.py
```

The demo will:

1. Store a preference (`draft_only`)
2. Store a contradicting preference (`auto_send`)
3. Resolve the contradiction (keep `draft_only`)
4. Process an action through Chip → RIO → Execution
5. Print the global receipt chain
6. Verify chain integrity

Expected output includes:
- Contradiction blocks execution until resolved
- After resolution, execution succeeds in draft mode
- Chain verification returns `{"valid": true, "length": 7}`

## Repository Structure

```
rio-sovereignty-stack/
  README.md
  docs/
    PUBLIC_RELEASE.md
    NAMING.md
    one-spec.md
  spec/
    receipts.md
    sovereignty-stack.md
  demo/
    demo_sovereignty_stack.py
  shared/
    receipt_service.py
    receipt_verifier.py
```

## License

MIT
