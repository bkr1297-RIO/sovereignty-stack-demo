"""
Receipt Verifier
Independent verification of a receipt chain.

Takes a list of receipts and verifies:
  - First receipt has priorReceiptHash = None
  - Each subsequent receipt chains to the previous via priorReceiptHash == prior objectHash
  - Chain is continuous and append-only
"""


def verify_chain(receipts):
    """
    Verify a receipt chain is valid.

    Args:
        receipts: list of receipt dicts, each with at least:
            - receiptId
            - objectHash
            - priorReceiptHash

    Returns:
        dict with:
            - valid: bool
            - length: int (if valid)
            - error: str (if invalid)
            - index: int (if invalid, position of break)
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
