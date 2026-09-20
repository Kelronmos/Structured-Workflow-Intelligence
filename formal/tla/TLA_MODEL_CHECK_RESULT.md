# TLA+ model-check result (abstract route)

**model_status:** `MODEL_PASS`  
**runtime_implementation:** `NOT_IMPLEMENTED`  
**execution_authorized:** `false`

## Positive model

| Item | Value |
|------|--------|
| Spec | `formal/tla/route_model/SWIRouteModel.tla` |
| MaxStep | 26 |
| Result | No error found |
| States generated | 60 |
| Distinct states | 26 |
| Depth | 3 |

## Mutations (all COUNTEREXAMPLE)

MutA skip without rule · MutB empty halt · MutC empty pause · MutD empty quarantine · MutE execution_authorized true · MutF silent authority increase

```text
MODEL_PASS ≠ system proven ≠ legal ≠ FM runtime implemented
```
