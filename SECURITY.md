# Security Policy

## Supported Versions

The following versions are currently maintained and eligible for security updates.

| Version | Supported         |
| ------- | ----------------- |
| 5.x     | ✅ Research support |
| 4.x     | ✅ Limited Support |
| < 4.0   | ❌ End of Life     |

### Support Definitions

* **Full Support** – Security fixes, bug fixes, and critical governance updates (research track).
* **Limited Support** – Critical security fixes only.
* **End of Life (EOL)** – No security or maintenance updates.

---

# Reporting a Vulnerability

The SWI Project takes security, governance integrity, auditability, and responsible disclosure seriously.

## Responsible Disclosure Process

If you discover a security vulnerability, please do **not** create a public GitHub issue.

Instead, report the vulnerability through one of the following channels:

* GitHub Security Advisories (preferred)
* Private email to the project maintainers
* Responsible disclosure channel designated by the project

### Required Information

Please include:

* Description of the vulnerability
* Impact assessment
* Steps to reproduce
* Affected component(s)
* Proof of concept (if available)
* Suggested mitigation (optional)

---

## Response Targets

| Activity                | Target Time       |
| ----------------------- | ----------------- |
| Initial acknowledgement | Within 72 hours   |
| Triage assessment       | Within 7 days     |
| Status update           | Every 14 days     |
| Fix development         | Based on severity |
| Public disclosure       | After remediation |

---

## Severity Classification

### Critical

Examples: governance bypass, policy engine compromise, receipt forgery, audit trail manipulation, remote code execution.  
Target remediation: 7–30 days

### High

Examples: privilege escalation, authentication weaknesses, cryptographic implementation flaws, data integrity violations.  
Target remediation: 30–60 days

### Medium

Examples: information disclosure, security misconfiguration, non-critical denial of service.  
Target remediation: 60–90 days

### Low

Examples: documentation errors, non-exploitable weaknesses, minor hardening.  
Target remediation: Best effort

---

## Scope

Security-sensitive areas (when implemented):

* Truth Kernel / decision kernel
* Policy Engine
* Receipt / audit chain
* Identity and authorization
* Cryptographic modules
* Governance enforcement controls
* Module registry and seal gate

---

## Safe Harbor

Good-faith research that avoids privacy violations, service disruption, and data destruction is welcome and will not be treated as malicious.

---

## Security Roadmap (research priorities)

* Formal verification of deterministic kernel behavior
* STRIDE threat modeling
* TPM/HSM trust anchor integration (future)
* Cryptographic hardening with evidence
* Receipt-chain integrity verification tests
* Cross-runtime determinism testing
* Evidence-backed module sealing (`scripts/swi-seal.mjs`)

---

## Disclaimer (authoritative)

SWI is a **research prototype**. See `SWI_SYSTEM_STATE.json`:

* `status`: RESEARCH_PROTOTYPE
* `risk`: DO_NOT_DEPLOY

Portions may be REAL, HYBRID, or SIMULATED.  
**Do not deploy as production security infrastructure** without independent verification that exceeds this repository’s claims.

Maturity labels (VERIFIED / PARTIAL / SIMULATED) must match executable evidence. Documentation alone is not verification.
