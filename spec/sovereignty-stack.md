# Sovereignty Stack

## 4-Layer Model

The sovereignty stack consists of four layers. Each layer has a single responsibility. All layers share one global receipt chain.

| Layer | Name | Responsibility |
|-------|------|---------------|
| 1 | Digital Chip | Classifies input. Admits preferences. Flags actions that require approval. |
| 2 | Continuity Engine | Stores preferences. Detects contradictions. Resolves contradictions. |
| 3 | RIO | Governs actions against active preferences and unresolved contradictions. |
| 4 | Execution | Executes only if RIO decision is `allow`. Otherwise blocks. |

## System Flow

```
Input → Chip → Continuity → RIO → Execution → Receipts
```

### Step-by-step

1. **Input arrives.** An object with `type` (preference or action) enters the system.

2. **Chip evaluates.** The Digital Chip classifies the input:
   - Preferences are admitted directly.
   - Actions are admitted or flagged for approval (e.g., `external_send` requires approval).
   - Emits a `chip/evaluate` receipt.

3. **Continuity stores.** The Continuity Engine processes preferences:
   - Stores the preference.
   - If a preference contradicts an existing one (same domain + key, different value), a contradiction is recorded.
   - Emits `continuity/store` and optionally `continuity/contradiction` receipts.

4. **Contradictions are resolved.** A human resolves contradictions by choosing a winner:
   - The losing preference is deactivated.
   - Emits a `continuity/resolve` receipt.

5. **RIO governs.** RIO evaluates the current state:
   - If unresolved contradictions exist: **block**.
   - If active preference allows it (e.g., `draft_only`): **allow** with mode.
   - Otherwise: **require approval**.
   - Emits a `rio/govern` receipt.

6. **Execution runs.** The execution layer acts on the RIO decision:
   - If `allow`: executes the action.
   - If anything else: blocks.
   - Emits a `rio/execute` receipt.

7. **Receipts verify.** The global receipt chain can be verified at any time to confirm integrity.

## Invariant

No action executes without a governance decision. No governance decision is made with unresolved contradictions. Every step produces a receipt. The receipt chain is append-only and hash-linked.
