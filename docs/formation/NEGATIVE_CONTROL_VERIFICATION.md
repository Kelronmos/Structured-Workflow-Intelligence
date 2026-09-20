# Formation package — negative-control verification

**Result package status (unchanged):** `PROPOSED` / `NOT_IMPLEMENTED`

## Bound commits

| SHA | Role |
|-----|------|
| `ed7fb40` / full `ed7fb40a2b317096f0cdb79defe7234751972c0d` | Machine inventory + schemas |
| `1cf2eec` / full `1cf2eec1939aa878ee2c96ab3a154d73d8d3fb09` | Human map + five-axis example |

This report challenges the documentation package; it does **not** implement FM-023–040, seal any module, authorize execution, or move paths into V1/V2.

## Checks

- [x] exactly 18 paths
- [x] every node PROPOSED / NOT_IMPLEMENTED / proof_status NONE
- [x] inventory package_status=PROPOSED
- [x] inventory implementation_status=NOT_IMPLEMENTED
- [x] inventory proof_status=NONE
- [x] inventory seal_status non-promoting (NOT_APPLICABLE)
- [x] inventory authorization_status non-promoting (NOT_AUTHORIZED)
- [x] inventory execution_status non-promoting (NOT_EXECUTABLE)
- [x] path-node schema locks status to PROPOSED
- [x] path-node schema locks implementation_status to NOT_IMPLEMENTED
- [x] five axes A1–A5 present
- [x] 20 MUST_NOT_INFER pairs (no cross-axis inference)
- [x] example posture all NOT_ASSESSED
- [x] valid five-axis document validates
- [x] ESTABLISHED posture rejected by schema
- [x] SEALED posture rejected by schema
- [x] package_status IMPLEMENTED rejected
- [x] valid path node validates
- [x] path node status SEALED rejected
- [x] path node IMPLEMENTED rejected
- [x] formation artifact with full axis_posture validates
- [x] artifact missing A5 rejected
- [x] package does not self-promote to proof/implementation

## Decision

**NEGATIVE CONTROL: PASSED** — package remains non-promoting.

```text
PROPOSED / NOT_IMPLEMENTED
proof_status: NONE
No ESTABLISHED/SEALED posture enums accepted
Cross-axis inference forbidden (MUST_NOT_INFER)
FM-023–040 stay out of V1/V2 implementation surface
```

Re-run: `python3 scripts/verify_formation_package.py`
