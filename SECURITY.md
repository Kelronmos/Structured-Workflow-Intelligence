# Security Policy

## Supported Versions

The following versions are currently maintained and eligible for security updates.

| Version | Supported         |
| ------- | ----------------- |
| 5.x     | ✅                 |
| 4.x     | ✅ Limited Support |
| < 4.0   | ❌ End of Life     |

### Support Definitions

* **Full Support** – Security fixes, bug fixes, and critical governance updates.
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

Examples:

* Governance bypass
* Policy engine compromise
* Receipt forgery
* Audit trail manipulation
* Remote code execution

Target remediation: 7–30 days

### High

Examples:

* Privilege escalation
* Authentication weaknesses
* Cryptographic implementation flaws
* Data integrity violations

Target remediation: 30–60 days

### Medium

Examples:

* Information disclosure
* Security misconfiguration
* Non-critical denial of service

Target remediation: 60–90 days

### Low

Examples:

* Documentation errors
* Non-exploitable weaknesses
* Minor hardening opportunities

Target remediation: Best effort

---

## Scope

The following SWI components are considered security-sensitive:

* Truth Kernel
* Policy Engine
* Receipt Chain
* Audit Ledger
* Identity and Authorization Components
* Cryptographic Modules
* Governance Enforcement Controls

---

## Safe Harbor

The project welcomes good-faith security research.

Researchers who:

* Avoid privacy violations
* Avoid service disruption
* Avoid data destruction
* Act responsibly

will not be considered to be acting maliciously.

---

## Security Roadmap

Current security priorities include:

* Formal verification of deterministic kernel behavior
* STRIDE threat modeling
* TPM/HSM trust anchor integration
* Cryptographic hardening
* Receipt-chain integrity verification
* Cross-runtime determinism testing

Security improvements are tracked publicly through the project's Security Roadmap and GitHub Issues.

---

## Disclaimer

SWI is currently an evolving platform and portions of the system may be classified as:

* VERIFIED
* PARTIAL
* SIMULATED

as documented within the repository.

Users should review component maturity levels before deploying SWI in production environments.
