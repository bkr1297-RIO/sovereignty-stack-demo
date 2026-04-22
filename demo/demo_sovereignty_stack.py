"""
RIO Sovereignty Stack — Reference Demo

Demonstrates the full sovereignty stack flow:
  Input → Digital Chip → Continuity Engine → RIO → Execution → Receipts

All receipts go to a single global chain.
Chain is verified at the end.

Run:
  python demo/demo_sovereignty_stack.py
"""
import sys
import os
import json

# Add parent directory so shared/ is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.receipt_service import post_receipt, get_receipts, verify, _make_id


# ── Digital Chip ──────────────────────────────────────────────

def chip(obj):
    """Classify input. Preferences are admitted. Actions may require approval."""
    if obj["type"] == "preference":
        result = {"status": "admit", "class": "preference"}
    elif obj.get("action") == "external_send":
        result = {"status": "require_approval", "class": "action"}
    else:
        result = {"status": "admit", "class": "action"}
    result["receipt"] = post_receipt("chip", "evaluate", result)
    return result


# ── Continuity Engine ─────────────────────────────────────────

preferences = []
contradictions = []


def continuity(obj):
    """Store a preference. Detect contradictions."""
    if obj["type"] != "preference":
        return {"status": "no_change"}
    new_pref = {
        "id": _make_id("pref"),
        "domain": obj["domain"],
        "key": obj["key"],
        "value": obj["value"],
        "active": True
    }
    for p in preferences:
        if p["domain"] == new_pref["domain"] and p["key"] == new_pref["key"] and p["value"] != new_pref["value"]:
            c = {
                "id": _make_id("contradiction"),
                "prefs": [p["id"], new_pref["id"]],
                "status": "unresolved"
            }
            contradictions.append(c)
            post_receipt("continuity", "contradiction", c)
    preferences.append(new_pref)
    result = {"status": "stored", "pref": new_pref}
    result["receipt"] = post_receipt("continuity", "store", result)
    return result


def resolve(contradiction_id, keep_id):
    """Resolve a contradiction by picking a winner."""
    for c in contradictions:
        if c["id"] == contradiction_id:
            c["status"] = "resolved"
            c["winner"] = keep_id
            for p in preferences:
                if p["id"] in c["prefs"] and p["id"] != keep_id:
                    p["active"] = False
            post_receipt("continuity", "resolve", c)
            return c


# ── RIO ───────────────────────────────────────────────────────

def rio(prefs, contras):
    """Govern action against preferences and contradictions."""
    active = None
    for p in prefs:
        if p["domain"] == "vendor" and p["key"] == "send_mode" and p["active"]:
            active = p["value"]
    unresolved = [c for c in contras if c["status"] == "unresolved"]
    if unresolved:
        result = {"status": "block", "reason": "contradiction"}
    elif active == "draft_only":
        result = {"status": "allow", "mode": "draft"}
    else:
        result = {"status": "require_approval"}
    result["receipt"] = post_receipt("rio", "govern", result)
    return result


def execute(decision):
    """Execute only if decision status is 'allow'."""
    if decision["status"] != "allow":
        result = {"status": "blocked"}
    else:
        result = {"status": "executed", "action": "draft_created"}
    result["receipt"] = post_receipt("rio", "execute", result)
    return result


# ── Demo Flow ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n--- STEP 1: Preference A ---")
    a = {"type": "preference", "domain": "vendor", "key": "send_mode", "value": "draft_only"}
    print(continuity(a))

    print("\n--- STEP 2: Preference B (contradiction) ---")
    b = {"type": "preference", "domain": "vendor", "key": "send_mode", "value": "auto_send"}
    print(continuity(b))

    print("\n--- STEP 3: Resolve contradiction ---")
    cid = contradictions[0]["id"]
    resolve(cid, preferences[0]["id"])
    print("Resolved")

    print("\n--- STEP 4: Action request ---")
    action = {"type": "action", "action": "reply_to_vendor"}
    chip_result = chip(action)
    print("Chip:", chip_result)

    decision = rio(preferences, contradictions)
    print("RIO:", decision)

    exec_result = execute(decision)
    print("Execution:", exec_result)

    print("\n--- GLOBAL RECEIPT CHAIN ---")
    print(json.dumps(get_receipts(), indent=2))

    print("\n--- CHAIN VERIFICATION ---")
    print(json.dumps(verify(), indent=2))
