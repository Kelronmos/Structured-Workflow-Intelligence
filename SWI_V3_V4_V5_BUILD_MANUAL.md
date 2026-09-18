# SWI v3–v5 Controlled Completion Manual

**Project:** Structured Workflow Intelligence  
**Repository:** Kelronmos/Structured-Workflow-Intelligence  
**Related foundations:**  
- [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10) (Python modules 00–10, evidence export)  
- [SWI-V2-Modules-11-22](https://github.com/Kelronmos/SWI-V2-Modules-11-22) (M11 admission, travel CI, authority)  

**Status of this document:** GOVERNING PROCESS (not a claim that v3–v5 are complete)  
**Current system state:** See `SWI_SYSTEM_STATE.json` (research prototype; simulated crypto where stated; do not deploy as production).

---

## 0. Executive rule

SWI v3–v5 is **not** a conventional rewrite.

```text
DISCOVER → CLASSIFY → ADOPT → HARDEN → BUILD MISSING
  → TEST → VERIFY → SEAL → INTEGRATE → SYSTEM VERIFY → RELEASE
```

**Never rebuild an existing verified capability merely because a newer module requires it.**  
Reuse, wrap, harden, or extend. Build only what is demonstrably missing.

A module may exist in the tree without being operational.  
Operational trust requires a **passed verification path**.  
Implemented-but-unproven modules remain **SEALED** (visible, testable, non-trusted).

---

## 1. Purpose

This manual governs completion of remaining capabilities across v3, v4, and v5 while preventing:

1. duplicate implementations  
2. incompatible parallel architectures  
3. premature integration  
4. false completion claims  
5. unverified security assumptions  
6. hidden dependency coupling  
7. irreversible architectural decisions without evidence  
8. production exposure of unfinished capabilities  

---

## 2. Treat current architecture as an asset

Before creating a subsystem:

```text
Future requirement
  → search existing SWI (this repo + V1 + V2)
  → Fully satisfies → ADOPT
  → Partial → EXTEND / HARDEN
  → Related primitive → ADAPTER
  → Nothing → BUILD
```

Record the decision. No new subsystem without that record.

---

## 3. Capability classification (exactly one)

| Class | Meaning |
|-------|--------|
| **ADOPT** | Existing implementation; config/docs/tests only |
| **HARDEN** | Concept correct; verification/security insufficient |
| **EXTEND** | Right foundation; missing features |
| **ADAPTER** | External mature tech; SWI owns policy/identity/audit |
| **BUILD** | Nothing acceptable exists |
| **DEFER** | Postponed with owner, dependency, reason, acceptance criteria |

---

## 4. Module state machine

```text
PLANNED → DISCOVERED → DESIGNED → BUILDING → IMPLEMENTED
  → TESTED → VERIFIED → SEALED → INTEGRATION-READY
  → INTEGRATED → SYSTEM-VERIFIED → RELEASE-CANDIDATE → RELEASED
```

Failure paths: TESTED→FAILED · VERIFIED→INVALIDATED · SEALED→REOPENED · INTEGRATED→ROLLBACK · RELEASED→INCIDENT/RECALL

---

## 5. Meaning of SEALED

**SEALED ≠ complete.**  
**SEALED =** implementation may exist, but it is **prohibited** as a trusted production dependency until its declared verification path passes.

Allowed while sealed: source control, unit tests, fixtures, docs, isolated verification.  
Not allowed: silent promotion to trusted production dependency.

### Seal levels

| Level | Meaning | Usage |
|-------|---------|--------|
| SEAL-0 | Scaffold / contract only | No runtime dependency |
| SEAL-1 | Implemented + unit tests | Isolated dev/test |
| SEAL-2 | Verified (negatives, security, fixtures) | Controlled integration tests |
| SEAL-3 | System verified | INTEGRATION-READY |

---

## 6. Evidence vocabulary (mandatory)

Prefer: Scaffolded · Implemented · Tested · Verified · Sealed · Integration-ready · System-verified · Release candidate · Released.

Do **not** use DONE / COMPLETE / SECURE / PRODUCTION READY / ENTERPRISE READY / PROVEN unless defined evidence thresholds are met.

See also: `CAPABILITY_MATRIX.md`, `TRACEABILITY_MATRIX.md`, `SECURITY_ROADMAP.md`, `SWI_SYSTEM_STATE.json`.

---

## 7. Build focus by family

### v3 — Foundations

Identity · secrets · API boundaries · audit · observability · security automation · synchronization · operational controls.  
**Goal:** trustworthy foundations, not maximum feature count.

### v4 — Infrastructure & resilience

PKI / certificate lifecycle · hardware-backed security · HA · DR · cross-runtime determinism · zero-trust service identity · external adapters.  
**Adopt** mature tech (e.g. WireGuard, Vault/KMS, OpenTelemetry, OIDC) via **ADAPTER**; SWI owns policy, identity semantics, governance, verification, audit, receipts, trust decisions.

### v5 — Convergence

Verified module registry · cross-module contracts · trust boundaries · integration proofs · E2E determinism · recovery · security validation · operational maturity · release evidence.  
**Goal:** prove capabilities work **together** without violating individual guarantees.

---

## 8. Module development pattern

1. Define contract  
2. Discover existing implementation (this repo + V1 + V2)  
3. Select ADOPT / HARDEN / EXTEND / ADAPTER / BUILD / DEFER  
4. Threat model + invariants  
5. Implement in isolation  
6. Positive + negative + determinism + recovery tests as applicable  
7. Static analysis / build / verify  
8. Record evidence (hashed where possible)  
9. Seal  
10. Review  
11. Only then permit integration  

Mental command:

```text
FIND → ADOPT → GAP → BUILD → TEST → VERIFY → SEAL → CONNECT
```

Never: `REBUILD → CONNECT → HOPE → VERIFY`.

---

## 9. Non-negotiable rules

1. Existing verified code is an asset, not debt.  
2. Do not rebuild merely for cosmetic architecture.  
3. Do not connect unfinished modules because interfaces exist.  
4. Every new security-sensitive capability starts sealed.  
5. Verification is evidence, not a declaration.  
6. Trust-critical change invalidates prior verification.  
7. A mock is never production trust (mark MOCK / TEST ONLY).  
8. Prefer external mature infrastructure via controlled adapters.  
9. Future modules get contracts before integration dependencies.  
10. No trust from filenames, docs, version numbers, or status reports—only reproducible evidence.  

---

## 10. External adoption examples (orientation)

| Need | Prefer |
|------|--------|
| VPN | WireGuard + SWI authz/audit adapter |
| Secrets | Vault/KMS adapter; reject dev providers in production |
| Observability | OpenTelemetry + correlation fields |
| PKI | Separate primitive / CA / lifecycle / HSM adapter |
| HA / DR | Prove via failure drills, not manifests alone |

---

## 11. Canonicalization & determinism

Trust-sensitive data must use the **repository’s established** canonicalization where one exists.  
Do not invent competing algorithms.  
Python foundation: V1 `swi_core.canonical` / V2 `swi_v2.kernel.canonical` (`canonicalization_v0`).  
Identical canonical inputs → identical digests/outputs on the trust path.

---

## 12. Negative testing minimum (security-sensitive modules)

Invalid/expired identity · missing authz · malformed input · tampered payload · bad signature · wrong key · replay · stale policy · corrupted state · timeout · dependency failure · partial failure.

Success-only demos are not verification.

---

## 13. Integration & release gates

**Integrate only after** individual module verification + contract compatibility + security + determinism + audit continuity + recovery as applicable + CI pass.

**Release only after** source/deps/modules/integration/security verified, artifacts hashed, config reviewed, rollback/recovery tested, release manifest generated.

Canary progression: DISABLED → SHADOW → TEST → CANARY → CONTROLLED → GENERAL.  
Shadow must not silently alter trusted state.  
Rollback defined **before** activation and tested.

---

## 14. Registry

Machine-readable readiness lives in `MODULE_REGISTRY.json`.  
It is a **control plane**, not a marketing status page.  
Updating a registry row to INTEGRATION_READY without evidence is a process defect.

---

## 15. Immediate next steps (practical)

1. Inventory remaining capabilities against `CAPABILITY_MATRIX.md` / `TRACEABILITY_MATRIX.md` using ADOPT/HARDEN/EXTEND/ADAPTER/BUILD/DEFER.  
2. Do **not** connect sealed modules as trusted dependencies.  
3. Prefer hardening V1/V2 evidence and this repo’s documented prototype boundaries over parallel rewrites.  
4. Add verification tooling only when it runs against real tests and records real SHAs.  

---

## 16. Target end-state picture (aspirational layout)

Governance / policy / decisions → verification core → identity, audit, crypto, secrets, ledger, receipts, API, observability, recovery, PKI, HA, DR, external adapters → verification gate → release evidence → production.

The architecture **may** contain planned modules before all are trusted. Unfinished components remain **visible, documented, testable, sealed, non-trusted** until verification passes.

---

*This manual is the operating principle for v3–v5 completion. It does not seal modules by itself.*
