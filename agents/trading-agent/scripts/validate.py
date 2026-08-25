"""
Trading Agent — Data Verifier
Cross-verifies two data sources for a given metric.
Usage: python validate.py <value_a> <value_b> [tolerance_pct]
Example: python validate.py 90.20 90.35 2.0
"""

import sys
import json


def verify(value_a, value_b, tolerance_pct=2.0):
    try:
        a = float(value_a)
        b = float(value_b)
    except (ValueError, TypeError):
        return {
            "passed": False,
            "error": f"Cannot parse values: {value_a}, {value_b}",
            "diff_pct": None,
            "consensus": None
        }

    if b == 0 and a == 0:
        diff_pct = 0.0
    elif b == 0:
        diff_pct = float('inf')
    else:
        diff_pct = abs(a - b) / abs(b) * 100

    passed = diff_pct <= tolerance_pct if diff_pct != float('inf') else False
    consensus = round((a + b) / 2, 2) if passed else round(min(a, b), 2)

    return {
        "passed": passed,
        "source_a_value": round(a, 2),
        "source_b_value": round(b, 2),
        "diff": round(a - b, 2),
        "diff_pct": round(diff_pct, 2) if diff_pct != float('inf') else "infinite",
        "tolerance_pct": tolerance_pct,
        "consensus": consensus,
        "verdict": "VERIFIED" if passed else "UNVERIFIED — discrepancy exceeds tolerance"
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate.py <value_a> <value_b> [tolerance_pct]")
        print("Example: python validate.py 90.20 90.35 2.0")
        sys.exit(1)

    tolerance = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    result = verify(sys.argv[1], sys.argv[2], tolerance)
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["passed"] else 1)
