# SWI v3–v5 Execution, Testing, Review & Diagnostic Technical Manual

**Repository:** Kelronmos/Structured-Workflow-Intelligence  
**Status:** Draft  
**Purpose:** Teaching, implementation, testing, review, diagnosis, and evidence discipline

---

## 1. Purpose

This manual defines how SWI maintainers should discover missing work, reuse existing capabilities, reproduce defects, implement controlled fixes, test them, review the changes, diagnose failures, retest, verify evidence, and maintain sealed boundaries.

The governing lifecycle is:

```text
FIND
  ↓
ADOPT EXISTING
  ↓
IDENTIFY GAP
  ↓
REPRODUCE
  ↓
FIX / HARDEN
  ↓
TEST
  ↓
REVIEW
  ↓
DIAGNOSE
  ↓
RETEST
  ↓
VERIFY
  ↓
SEAL / RE-SEAL
  ↓
PROVE INTEGRATION
  ↓
CONNECT
  ↓
SYSTEM VERIFY
  ↓
RELEASE EVIDENCE
```

Never reverse this into:

```text
REBUILD → CONNECT → HOPE → VERIFY
```

This manual is a process and teaching document. Its existence does not constitute verification, production authorization, security certification, or release approval.

---

## 2. Core SWI Doctrine

SWI v3–v5 is controlled completion, not a rewrite.

The first question is not:

> "How do we build this?"

The first question is:

> "What already exists, what can be adopted, what is actually missing, and what evidence proves it?"

The governing principle is:

```text
DISCOVER
→ ADOPT EXISTING
→ IDENTIFY GAPS
→ BUILD ONLY MISSING
→ TEST
→ VERIFY
→ SEAL
→ INTEGRATION-READY
→ CONNECT
→ SYSTEM VERIFY
→ RELEASE
```

No module should be promoted merely because:

- documentation exists;
- source files exist;
- tests exist;
- a test command exits successfully;
- a developer reports completion;
- a registry flag was manually changed;
- CI appears green without proving the relevant property.

---

## 3. Evidence Vocabulary

These states must remain distinct:

| State | Meaning |
|-------|---------|
| EXISTS | Code, configuration, documentation, or infrastructure is present |
| TESTED | One or more tests were executed |
| VERIFIED | Declared verification criteria passed with evidence |
| INTEGRATED | Verified components are connected under defined controls |
| SYSTEM-VERIFIED | The integrated system passed system-level verification |
| RELEASED | Release controls accepted the release |

Therefore:

```text
EXISTS ≠ TESTED
TESTED ≠ VERIFIED
VERIFIED ≠ INTEGRATED
INTEGRATED ≠ SYSTEM-VERIFIED
SYSTEM-VERIFIED ≠ RELEASED
```

Avoid unsupported claims such as:

- DONE
- COMPLETE
- SECURE
- PRODUCTION READY
- FULLY HARDENED
- 100% VERIFIED

unless the exact claim is supported by explicit, reproducible evidence.

---

## 4. Discover Before Building

Before writing new code, inspect:

1. Current repository implementation.
2. SWI V1/V2 implementation.
3. Existing APIs.
4. Existing tests.
5. Existing fixtures.
6. Existing contracts.
7. Existing CI.
8. Existing security controls.
9. Existing cryptographic infrastructure.
10. Existing persistence/ledger infrastructure.
11. Existing identity/governance infrastructure.
12. Mature external infrastructure that should be consumed through adapters.

Every proposed capability should receive a disposition.

| Disposition | Meaning |
|-------------|---------|
| ADOPT | Existing implementation satisfies the required contract |
| HARDEN | Existing implementation is fundamentally correct but requires stronger controls/evidence |
| EXTEND | Existing foundation is correct but bounded functionality is missing |
| ADAPTER | A mature external primitive should be integrated rather than reimplemented |
| BUILD | Capability is genuinely absent |
| DEFER | Safe completion criteria are not yet established |

### Discovery worksheet

```text
Requirement:

Existing implementation:

V1/V2 equivalent:

Existing API:

Existing tests:

Existing security controls:

Known limitations:

Disposition:

Actual gap:

Evidence required:
```

Do not invent missing capabilities simply because a new module name appears in a roadmap.

---

## 5. Baseline the Repository

Before modifying anything, capture the exact repository state.

```bash
git rev-parse HEAD
git status --short
git branch --show-current
```

Inspect:

```bash
cat package.json
cat SWI_SYSTEM_STATE.json
cat config/swi-module-registry.json
```

Then inspect the relevant:

- source
- tests
- scripts
- workflows
- configuration
- documentation
- fixtures

Record the baseline commit.

This allows later reviewers to determine whether a failure was pre-existing or introduced by the patch.

---

## 6. Audit Executable References

A command appearing in a package script or workflow is not evidence that the command actually works.

Trace every important command:

```text
WORKFLOW / PACKAGE COMMAND
          ↓
TARGET SCRIPT EXISTS?
          ↓
IMPORTS EXIST?
          ↓
DEPENDENCIES EXIST?
          ↓
COMMAND EXECUTES?
          ↓
MEANINGFUL ASSERTIONS?
          ↓
FAILS ON VIOLATION?
```

Useful checks:

```bash
node -e "console.log(require('./package.json').scripts)"
find scripts -maxdepth 1 -type f -print
grep -R "generate_report\|hashseal\|verify.mjs\|swi-ci-check" \
  .github package.json scripts tests 2>/dev/null
```

If CI references a missing script, that is a real execution defect.

Do not create a fake script that only prints `PASS` and exits with code `0`. That is verification theatre.

---

## 7. Reproduce Before Fixing

Every fix should begin with a reproducible problem whenever practical.

The defect loop is:

```text
EXPECTED
   ↓
ACTUAL
   ↓
REPRODUCER
   ↓
FAILING TEST
   ↓
MINIMAL FIX
```

Example:

```text
Given:
  a module is SEALED

When:
  integration_enabled is set to true

Then:
  registry verification must reject the configuration
```

The test should fail before the fix if the defect exists.

A successful demonstration is not equivalent to a regression test.

---

## 8. Define Invariants

Trust-critical behavior must be expressed as explicit invariants.

Examples:

- Duplicate module IDs must be rejected.
- Missing dependencies must be rejected.
- SEALED modules must not be integration-enabled.
- Production readiness must require appropriate verification evidence.
- Integrated modules must not depend on untrusted modules.
- M11 must be verified before M12 can advance.
- M12 must remain disconnected until its own evidence exists.
- Research-prototype system state must not be silently converted into production state.

For every invariant document:

```text
Invariant:
Why it matters:
Valid input:
Invalid input:
Expected result:
Executable assertion:
Evidence artifact:
```

---

## 9. Implement the Smallest Safe Fix

Prefer:

```text
ONE DEFECT
   ↓
ONE FOCUSED CHANGE
   ↓
FOCUSED TEST
   ↓
REGRESSION TEST
```

Before changing code ask:

1. Does existing code already solve this?
2. Can the existing implementation be adopted?
3. Is the proposed change actually necessary?
4. Does the change modify an API?
5. Does it modify a trust boundary?
6. Does it change module state?
7. Does it invalidate previous evidence?
8. What negative test is required?
9. What regression could this introduce?

Avoid unrelated refactoring in trust-critical patches.

---

## 10. Testing Model

SWI verification should use multiple testing layers.

### 10.1 Unit Testing

Test local behavior: parsing, validation, canonicalization, state transitions, dependency resolution, data transformations.

### 10.2 Negative Testing

Test forbidden behavior: duplicate IDs, missing dependencies, malformed input, invalid state transitions, unauthorized operations, untrusted dependencies, invalid configuration.

The system should reject invalid states rather than merely accepting valid states.

### 10.3 Security Testing

Where applicable, test: invalid signatures, wrong keys, replay attempts, stale authorization, boundary bypass, invalid credentials, unsafe configuration, tampered records.

Security tests must exercise actual controls rather than documentation claims.

### 10.4 Determinism Testing

Where deterministic output is required, execute the same operation repeatedly. Compare exit status, raw bytes, canonical serialization, digest/hash, ordering, timestamps, generated identifiers, metadata.

A command returning `0` twice does not prove deterministic output.

### 10.5 Integration Testing

Integration tests must prove the contract between components that have already passed their individual verification gates.

Do not treat successful module tests as proof of system integration.

### 10.6 Recovery Testing

If resilience or disaster recovery is claimed, exercise the recovery mechanism. A document saying "Backups exist" does not prove "Restore succeeded."

---

## 11. Tamper Testing

For trust-critical registries, intentionally construct invalid fixtures.

Test cases should include:

```text
VALID REGISTRY
      ↓
duplicate module ID
      ↓
missing dependency
      ↓
SEALED + integration_enabled
      ↓
production_ready without verification
      ↓
integrated module + untrusted dependency
```

Each mutation should produce the expected rejection. After testing, restore the original fixture.

The objective is to demonstrate that the control plane mechanically prevents unsafe states.

---

## 12. Review the Patch

After implementation:

```bash
git diff --check
git diff --stat
git diff
git status --short
```

Review every changed line. Ask:

- Is this line necessary?
- Does it implement the stated fix?
- Does it introduce unrelated behavior?
- Did a security gate become weaker?
- Did a default change?
- Did a trust boundary change?
- Did module state change?
- Did production flags change?
- Was a bypass introduced?
- Do the tests exercise the real implementation?
- Could an attacker or malformed input bypass the control?

A technically valid review may conclude: **FIX CORRECT BUT VERIFICATION EVIDENCE INSUFFICIENT**. That is a valid and useful outcome.

---

## 13. Stale Evidence

Trust-critical changes can invalidate earlier verification (authentication, authorization, cryptography, canonicalization, registry validation, dependency trust, verification logic, audit integrity, release gates, security controls).

When such a change occurs:

```text
previous evidence
      ↓
potentially stale
      ↓
identify affected gates
      ↓
rerun required verification
```

Never rely on "It passed last week." Evidence must correspond to the relevant revision and implementation.

---

## 14. Failure Diagnosis

When something fails:

1. **Capture the command** — exact command executed.
2. **Capture the first meaningful error** — not only the final cascade.
3. **Identify the failing layer** — source / configuration / dependency / test / build / package script / workflow / environment / security gate / integration.
4. **Reproduce narrowly** — smallest command that reproduces the failure.
5. **Classify the failure** — syntax/parse, missing file/stale reference, assertion, nondeterministic, CI-only, security-gate.

### Security-Gate Failure

Never solve a security failure by disabling the gate.

```text
FAIL → REPRODUCE → IDENTIFY INVARIANT → ADD/RETAIN REGRESSION TEST
  → FIX → SECURITY TEST → MODULE TEST → REGRESSION TEST
```

---

## 15. Retest Ladder

After a fix, testing should expand gradually:

1. REPRODUCER
2. TARGETED TEST
3. MODULE TEST SUITE
4. REGRESSION SUITE
5. TYPECHECK / BUILD
6. CI-EQUIVALENT TESTS
7. INTEGRATION

Examples where configured:

```bash
npm ci
node scripts/swi-verify-module.mjs
node --test tests/swi-module-registry.test.mjs
npx tsc --noEmit
```

Only execute commands that actually exist and have meaningful behavior.

---

## 16. Stop Conditions

Do not promote a module or enable integration when:

- required tests fail
- security invariants fail
- deterministic output differs unexpectedly
- dependency trust is insufficient
- required evidence cannot be reproduced
- CI references missing commands
- evidence cannot be tied to a revision
- a bypass is required

A failed gate is information about the current state. It is not permission to weaken the gate.

---

## 17. Evidence Recording

For every important verification run record:

```text
Repository:
Commit:
Date/time:
Environment:
Command:
Scope:
Expected result:
Actual result:
Tests executed:
Artifacts:
Checksums:
CI run:
Known limitations:
Next required gate:
```

A narrow result must remain a narrow result.

---

## 18. Evidence Hierarchy

Prefer evidence in approximately this order:

1. Reproducible executable test
2. Security/negative test
3. Deterministic fixture/result
4. Integration test
5. CI result tied to exact commit
6. Build artifact and checksum
7. Static analysis
8. Code review
9. Documentation

Documentation is necessary for maintainability. Documentation alone is not executable verification.

---

## 19. Module Sealing

Every module starts untrusted. The module registry is the machine-readable control plane. Evidence flags describe evidence; they must not manufacture evidence.

Important control-plane properties:

- duplicate module IDs rejected
- dependencies must exist
- production readiness requires appropriate evidence
- integration requires an allowed trusted state
- SEALED cannot be integration-enabled
- integrated modules cannot depend on untrusted dependencies

Never manually set `production_ready=true` or `integration_enabled=true` just because implementation appears complete.

---

## 20. M11 → M12 Order

```text
M11 → DISCOVER → ADOPT / FIX → TEST → VERIFY → INTEGRATION-READY
  ↓
M12 → DISCOVER → ADOPT / FIX → TEST → VERIFY → INTEGRATION-READY
  ↓
JOINT INTEGRATION → SYSTEM VERIFICATION
```

M12 must not become trusted simply because M11 exists.

---

## 21. CI Repair Method

For every workflow command, trace:

```text
WORKFLOW COMMAND → PACKAGE SCRIPT? → TARGET FILE? → IMPORTS?
  → DEPENDENCIES? → MEANINGFUL ASSERTIONS? → LOCAL EXECUTION? → CI EXECUTION?
```

If a workflow calls a missing script: identify the real intended behavior, repair the reference or implement the genuinely required command, test locally, test CI-equivalent path.

Never implement `console.log("PASS"); process.exit(0)` as a substitute for verification.

---

## 22–25. Teaching Exercises

**A — Stale CI Script:** Find workflow → package script → target file → existence → execute → capture failure → root cause → disposition → smallest fix → regression test → retest → review.

**B — Registry Tampering:** Create temporary invalid fixtures (duplicate ID, missing dep, SEALED+integration, production_ready without evidence, integrated+untrusted dep). Run real verifier. Expect mechanical rejection. Restore original.

**C — Determinism:** Run same trust-sensitive operation repeatedly. Compare bytes, hash, serialization, ordering, timestamps, identifiers, exit status.

**D — Patch Review:** Document changed / necessary / risk / security impact / regression risk / tests / missing tests / evidence / remaining sealed / trust-boundary changes.

---

## 26. Command Cookbook

```bash
# Baseline
git rev-parse HEAD
git status --short
git branch --show-current

# Package scripts
node -e "console.log(require('./package.json').scripts)"

# Script inventory
find scripts -maxdepth 1 -type f -print

# Reference audit
grep -R "generate_report\|hashseal\|verify.mjs\|swi-ci-check" \
  .github package.json scripts tests 2>/dev/null

# Patch validation
git diff --check && git diff --stat && git diff && git status --short

# Registry verification
node scripts/swi-verify-module.mjs
node --test tests/swi-module-registry.test.mjs

# Typecheck (when configured)
npx tsc --noEmit
```

---

## 27. Maintainer Checklist

Before advancing work:

- [ ] Existing implementation searched
- [ ] V1/V2 equivalent checked
- [ ] Existing tests inspected
- [ ] Capability classified
- [ ] Baseline commit recorded
- [ ] Defect reproduced where applicable
- [ ] Regression test added where practical
- [ ] Smallest safe fix implemented
- [ ] Positive / negative / security / determinism tests as applicable
- [ ] CI commands point to real files
- [ ] Diff reviewed line-by-line
- [ ] No bypass or fake verification introduced
- [ ] Evidence tied to exact commit
- [ ] Registry state matches evidence
- [ ] Unproven modules remain SEALED
- [ ] M11/M12 ordering respected
- [ ] Integration not prematurely enabled
- [ ] Production state consistent with `SWI_SYSTEM_STATE.json`

---

## 28. Verification Report Template

```markdown
# SWI Fix Verification Report

## Baseline
Repository: / Commit: / Branch: / Scope:

## Defect
Observed failure / Reproducer / Expected / Actual:

## Diagnosis
Root cause / Affected files / Security-trust impact:

## Fix
Disposition / Changed files / Why smallest safe change:

## Tests
Reproducer / Targeted / Module / Regression / Security / Negative /
Determinism / Recovery / Build-typecheck / CI-equivalent:

## Review
Diff reviewed / Unrelated changes / Bypass / Trust-boundary / Evidence invalidated:

## Evidence
Commit / Commands / Results / Artifacts / Checksums / CI run:

## Remaining Limitations
Unverified / SEALED / Integration blocked / Known defects / Production status:

## Decision
State supported by evidence / Next required gate:
```

---

## 29–30. Release-Evidence Discipline & Prohibited Shortcuts

Before any release claim: exact source revision → known dependency state → reproducible tests → security evidence → build evidence → artifact identity → checksums/signatures → CI evidence → review record → release decision.

Do not use `--force`, `--skip-verification`, `--allow-unverified`.  
Do not manually promote `production_ready=true` or `integration_enabled=true`.  
Do not use fake PASS scripts, success-only tests, documentation-only verification, or unreviewed trust-boundary changes.

---

## 31. Core Teaching Model

```text
CODE → CONTRACT → TEST → FAILURE → FIX → RETEST → REVIEW
  → VERIFICATION → SEALED STATE → INTEGRATION EVIDENCE
  → SYSTEM EVIDENCE → RELEASE EVIDENCE
```

The strongest engineering report answers:

- What was checked?
- What passed?
- What failed?
- What changed?
- Why was the change necessary?
- What evidence proves the change?
- What evidence is still missing?
- What remains SEALED?
- What is mechanically blocked?
- What must happen next?

---

## 32. Final Maintainer Principle

When evidence is incomplete:

**DO NOT GUESS. DO NOT PROMOTE. DO NOT HIDE THE FAILURE. DO NOT WEAKEN THE GATE. DO NOT CALL DOCUMENTATION VERIFICATION.**

Instead:

```text
REPRODUCE → DIAGNOSE → FIX → TEST → REVIEW → RETEST
  → VERIFY → RECORD EVIDENCE → KEEP UNPROVEN WORK SEALED
```

Evidence before status. Tests before claims. Existing infrastructure before rewrites. Verification before integration. Integration evidence before system claims. System evidence before release.

---

*End of Draft Technical Manual*
