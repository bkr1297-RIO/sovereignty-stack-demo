"""
Receipt Service
Maintains ONE append-only, hash-linked receipt chain across all services.

Endpoints:
  POST /receipts  — accept a receipt event, append to chain
  GET  /receipts  — return all receipts
  POST /verify    — verify chain integrity
"""
import json
import hashlib
import uuid
from datetime import datetime


def _now():
    return datetime.utcnow().isoformat()


def _make_id(prefix):
    return f"{prefix}_{uuid.uuid4()}"


def _hash_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


# Single global chain
receipts = []


def post_receipt(layer, event_type, payload):
    """
    POST /receipts
    Accept a receipt event from any service, append to the global chain.
    Returns the receipt.
    """
    prior_receipt_hash = receipts[-1]["objectHash"] if receipts else None
    parent_receipt_id = receipts[-1]["receiptId"] if receipts else None
    r = {
        "receiptId": _make_id("rcpt"),
        "timestamp": _now(),
        "layer": layer,
        "eventType": event_type,
        "objectHash": _hash_obj(payload),
        "priorReceiptHash": prior_receipt_hash,
        "parentReceiptId": parent_receipt_id
    }
    receipts.append(r)
    return r


def get_receipts():
    """
    GET /receipts
    Return all receipts in the chain.
    """
    return list(receipts)


def verify():
    """
    POST /verify
    Verify the chain is valid:
    - First receipt has priorReceiptHash = None
    - Each subsequent receipt's priorReceiptHash == previous receipt's objectHash
    - Chain is continuous
    """
    if not receipts:
        return {"valid": True, "length": 0}

    # First receipt must have no prior
    if receipts[0]["priorReceiptHash"] is not None:
        return {
            "valid": False,
            "error": "First receipt has non-null priorReceiptHash",
            "index": 0
        }

    # Each subsequent receipt must chain to the previous
    for i in range(1, len(receipts)):
        expected = receipts[i - 1]["objectHash"]
        actual = receipts[i]["priorReceiptHash"]
        if actual != expected:
            return {
                "valid": False,
                "error": f"Chain break at index {i}: expected {expected}, got {actual}",
                "index": i
            }

    return {"valid": True, "length": len(receipts)}


def reset():
    """Reset the chain (for testing only)."""
    receipts.clear()
