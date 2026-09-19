# Route Provenance Invariant (Policy 003)

**Invariant R-001**

> Every governed route shall be reconstructible from preserved provenance records sufficient to identify its origin, traversed nodes, interfaces, operations, destination, integrity state, and resulting evidence.

**Invariant R-002**

> Route records are append-only. Historical route records must never be silently overwritten or edited in place.

**Invariant R-003**

> Loss of mandatory route provenance constitutes a verification failure and shall cause HALT. The operation must not continue.

**Invariant R-004**

> No repository may be admitted into governed cross-repository development until it implements a compliant route-provenance interface.

**Invariant R-005**

> Naming, affiliation, repository location, or self-declared SWI status does not create a route record and does not satisfy this policy.
