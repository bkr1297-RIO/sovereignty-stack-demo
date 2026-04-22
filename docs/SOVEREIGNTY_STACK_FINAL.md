# ONE — Operator Notification Environment

## Definition

ONE is the human control surface for the RIO system. It is where the human operator observes system state, resolves contradictions, approves or blocks actions, and verifies receipts.

## Relationship to the Sovereignty Stack

The sovereignty stack produces decisions and receipts. ONE consumes them.

```
Sovereignty Stack → produces receipts → ONE displays them
ONE → human resolves contradiction → Sovereignty Stack continues
ONE → human approves action → RIO allows execution
```

## What ONE Does

- Displays the current preference state from the Continuity Engine
- Shows unresolved contradictions requiring human resolution
- Presents governance decisions from RIO for approval
- Displays the global receipt chain for verification
- Provides controls for resolving contradictions and approving actions

## What ONE Does Not Do

- ONE does not make governance decisions
- ONE does not modify receipts
- ONE does not execute actions
- ONE does not bypass RIO

## Scope

ONE is not part of this repository. This document defines its interface contract with the sovereignty stack. ONE is implemented separately.
