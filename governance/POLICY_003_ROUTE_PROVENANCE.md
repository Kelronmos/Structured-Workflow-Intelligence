# SWI POLICY 003

## Route Provenance and Retraceability

**Policy ID:** SWI-POLICY-003  
**Status:** CORE / MANDATORY  
**Authority:** SWI Governance Authority  
**Depends on:** SWI-POLICY-001, SWI-POLICY-002  
**Default:** DENY / HALT on missing mandatory route record  
**Applies to:** All governed development, discovery, pull, ingest, transform, bridge and execution operations across V1–V5 and future versions.

---

### 1. Purpose

No governed development process may traverse, discover, pull, ingest, transform, or connect to a node without creating a retraceable route record.

This control is broader than ordinary logging. The system must preserve the complete path by which an artifact, node, dependency, policy, repository, or evidence item was reached so that the route can be reconstructed later.

---

### 2. Formal Requirement

Every governed operation shall record, where applicable:

```
origin
  → source
  → route
  → intermediate nodes
  → bridge / interface
  → operation
  → destination
  → result
  → evidence
  → integrity reference
```

Example path:

```
Repository A
   ↓
Repository discovery
   ↓
SWI Bridge Security
   ↓
Node B
   ↓
Dependency C
   ↓
Module D
   ↓
Evidence E
```

The complete route must remain recoverable.

---

### 3. Canonical Route Record

A route record shall contain at minimum:

```yaml
route_id:
operation_id:

actor:
authority:

origin:
  repository:
  commit:

route:
  - node:
    type:
    repository:
    module:
    interface:
    operation:
    timestamp:          # or governed event reference
    integrity_reference:

destination:
  repository:
  module:

purpose:

contract:
  id:
  version:
  sha256:

result:                 # ADMITTED | REJECTED | HALTED

evidence:
  evidence_id:
  sha256:

parent_route:
previous_route_hash:

route_hash:             # SHA-256 of the canonical form of this record
```

---

### 4. Critical Rule — Append-Only

The route record itself must be **append-only**.

Forbidden:

```
old route
   ↓
edited
   ↓
new route
```

Required:

```
Route 001
   ↓ hash
Route 002
   ↓ hash
Route 003
   ↓ hash
Route 004
```

This produces a retraceable chain. Historical route records must never be silently overwritten.

---

### 5. Covered Operations

When any of the following occurs under governance, a route record is mandatory where technically applicable:

- PULL
- DISCOVER
- CLONE
- FETCH
- INGEST
- IMPORT
- DEPENDENCY RESOLVE
- BRIDGE
- EXECUTE
- POLICY / LAW / GOVERNANCE transfer across repositories

Example:

```
Developer
   ↓
Repository discovery
   ↓
Repository X
   ↓
commit abc123
   ↓
file / module
   ↓
dependency Y
   ↓
SWI Bridge
   ↓
analysis
```

---

### 6. Failure Condition

If a mandatory route record cannot be created or preserved:

> The operation shall HALT rather than silently continue.

Loss of mandatory route provenance constitutes a verification failure and shall cause HALT.

---

### 7. Safety / Recovery Requirement

The system must be able to answer, at any later time:

- Where did this come from?
- Who / what initiated it?
- Which repository supplied it?
- Which commit?
- Which node was traversed?
- Which bridge was used?
- Which module processed it?
- What was pulled?
- What was changed?
- What evidence existed at the time?
- What downstream components received it?
- Can we reproduce the route?

---

### 8. Formal Invariant

> Every governed route shall be reconstructible from preserved provenance records sufficient to identify its origin, traversed nodes, interfaces, operations, destination, integrity state, and resulting evidence. Loss of mandatory route provenance shall constitute a verification failure and shall cause HALT.

This requirement applies during development, not only after release.

---

### 9. Required Architecture Pattern

```
DISCOVER
   ↓
RECORD ROUTE
   ↓
VERIFY
   ↓
PULL / TRAVERSE
   ↓
RECORD NODE
   ↓
PROCESS
   ↓
RECORD RESULT
   ↓
HASH
   ↓
CONTINUE
```

Never:

```
Discover everything first
   ↓
Try to reconstruct history afterward
```

---

### 10. Relationship to Existing Controls

- **Policy 001** governs who may change policy and how.
- **Policy 002** governs the SWI Bridge Security Boundary and open pipes.
- **Policy 003** governs the retraceable path taken through those boundaries and modules.

Together they form:

```
POLICY 001 (Authority & Ingestion)
        ↓
POLICY 002 (Bridge Security)
        ↓
POLICY 003 (Route Provenance)
        ↓
ADMISSION VALVE
        ↓
EXECUTE or HALT + EVIDENCE
```

---

### 11. Admission Prerequisite

Every applicable repository must implement a compliant route-provenance interface before that repository can be admitted into governed cross-repository development.

A repository that cannot produce the required route records remains non-admitted for cross-repository operations.

---

### 12. Core Principle Statement

«No governed development process may traverse, discover, pull, ingest, transform, or connect to a node without creating a retraceable route record. Route records are append-only. Loss of mandatory route provenance causes HALT.»
