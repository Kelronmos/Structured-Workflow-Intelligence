#!/usr/bin/env python3
"""Tranche 2A — per-candidate workflow security inspection.

A workflow file is merely an artifact. Existence, name, location, or history
grants no execution authority.

Produces machine-readable risk records. Does NOT activate anything.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT / ".github"
WORKFLOWS_DIR = GITHUB / "workflows"
OUT = ROOT / "evidence" / "generated"

# High-risk permission keys (GitHub Actions permissions block)
WRITE_PERMISSIONS = {
    "contents",
    "packages",
    "deployments",
    "actions",
    "security-events",
    "id-token",
    "attestations",
}

DEPLOY_HINTS = re.compile(
    r"(deploy|production|release|publish|gh-pages|heroku|aws|kubectl|terraform|ansible)",
    re.I,
)
SECRET_HINTS = re.compile(r"\$\{\{\s*secrets\.[A-Za-z0-9_]+\s*\}\}")
ENV_HINTS = re.compile(r"\$\{\{\s*env\.[A-Za-z0-9_]+\s*\}\}")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_yaml(path: Path) -> tuple[bool, Any, Optional[str]]:
    try:
        import yaml

        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        return True, data, text
    except Exception as e:
        return False, None, str(e)


def _status(ok: bool, detail: str = "") -> dict:
    return {
        "status": "VERIFIED" if ok else "UNVERIFIED",
        "detail": detail or ("ok" if ok else "requires review"),
    }


def inspect_candidate(path: Path) -> dict[str, Any]:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    under_workflows = WORKFLOWS_DIR in path.parents or path.parent == WORKFLOWS_DIR

    record: dict[str, Any] = {
        "workflow_id": f"WF-{path.stem.upper().replace('.', '_')}",
        "path": rel,
        "state": "REVIEW_REQUIRED",
        "location": "workflows" if under_workflows else "github_root",
        "authority": {"status": "UNVERIFIED", "detail": "no explicit activation record"},
        "permissions": {"status": "UNVERIFIED", "detail": ""},
        "secrets": {"status": "UNVERIFIED", "detail": ""},
        "execution": {"status": "UNVERIFIED", "detail": ""},
        "actions_refs": {"status": "UNVERIFIED", "refs": []},
        "deploy_write_risk": {"status": "UNVERIFIED", "flags": []},
        "route_provenance": {"status": "UNVERIFIED", "detail": "not covered by this artifact alone"},
        "governance": {"status": "BLOCKED", "detail": "activation denied unless verified"},
        "activation": {"status": "DENIED_UNLESS_VERIFIED"},
        "yaml": {"parses": False},
        "triggers": [],
        "risks": [],
        "file_sha256": _sha256_bytes(path.read_bytes()) if path.is_file() else None,
    }

    if path.suffix.lower() not in (".yml", ".yaml"):
        record["state"] = "NOT_APPLICABLE"
        record["governance"]["status"] = "NOT_APPLICABLE"
        record["activation"]["status"] = "NOT_APPLICABLE"
        return record

    ok, data, text_or_err = _load_yaml(path)
    if not ok or not isinstance(data, dict):
        record["yaml"] = {"parses": False, "error": str(text_or_err)}
        record["risks"].append("MALFORMED_YAML")
        record["state"] = "BLOCKED"
        record["governance"]["status"] = "BLOCKED"
        record["execution"] = _status(False, "malformed YAML — fail closed")
        return record

    record["yaml"] = {"parses": True, "name": data.get("name")}
    text = text_or_err if isinstance(text_or_err, str) else path.read_text(encoding="utf-8")

    # Triggers
    on = data.get("on")
    if on is None:
        record["triggers"] = []
        record["risks"].append("MISSING_TRIGGER")
    elif isinstance(on, str):
        record["triggers"] = [on]
    elif isinstance(on, list):
        record["triggers"] = on
    elif isinstance(on, dict):
        record["triggers"] = list(on.keys())
    else:
        record["triggers"] = ["UNKNOWN_TRIGGER_SHAPE"]
        record["risks"].append("UNKNOWN_TRIGGER_SHAPE")

    # Permissions
    perms = data.get("permissions")
    perm_flags = []
    if perms is None:
        record["permissions"] = {
            "status": "UNVERIFIED",
            "detail": "no explicit permissions block (defaults may be broad)",
        }
        record["risks"].append("PERMISSIONS_UNSPECIFIED")
    elif perms == "read-all" or perms == "write-all":
        record["permissions"] = {
            "status": "UNVERIFIED",
            "detail": f"broad permissions: {perms}",
        }
        record["risks"].append(f"BROAD_PERMISSIONS:{perms}")
        perm_flags.append(str(perms))
    elif isinstance(perms, dict):
        for k, v in perms.items():
            if str(v).lower() == "write" and k in WRITE_PERMISSIONS:
                perm_flags.append(f"{k}:write")
                record["risks"].append(f"WRITE_PERMISSION:{k}")
        record["permissions"] = {
            "status": "UNVERIFIED",
            "detail": "explicit block present; write keys flagged if any",
            "write_flags": perm_flags,
        }
    else:
        record["permissions"] = {"status": "UNVERIFIED", "detail": "unparsed permissions shape"}

    # Secrets / env
    secrets_found = SECRET_HINTS.findall(text)
    env_found = ENV_HINTS.findall(text)
    if secrets_found or env_found:
        record["secrets"] = {
            "status": "UNVERIFIED",
            "detail": "secret or env references present",
            "secret_refs_count": len(secrets_found),
            "env_refs_count": len(env_found),
        }
        record["risks"].append("SECRETS_OR_ENV_REFS")
    else:
        record["secrets"] = {
            "status": "UNVERIFIED",
            "detail": "no ${{ secrets.* }} or ${{ env.* }} patterns found (static scan only)",
        }

    # Actions / uses
    uses = re.findall(r"uses:\s*['\"]?([^'\"\s]+)", text)
    record["actions_refs"] = {
        "status": "UNVERIFIED",
        "refs": uses,
        "detail": "third-party or local actions require review",
    }
    if uses:
        record["risks"].append("EXTERNAL_OR_LOCAL_ACTIONS")

    # Deploy / write hints
    deploy_flags = []
    if DEPLOY_HINTS.search(path.name) or DEPLOY_HINTS.search(text):
        deploy_flags.append("NAME_OR_CONTENT_DEPLOY_HINT")
        record["risks"].append("DEPLOY_OR_WRITE_HINT")
    if perm_flags:
        deploy_flags.extend(perm_flags)
    record["deploy_write_risk"] = {
        "status": "UNVERIFIED",
        "flags": deploy_flags,
        "detail": "implicit activation forbidden for deploy/write capable workflows",
    }

    # Execution posture
    if under_workflows:
        record["execution"] = {
            "status": "UNVERIFIED",
            "detail": "ACTIVE location — GitHub may execute; authority still UNVERIFIED",
        }
        record["state"] = "ACTIVE_LOCATION_UNVERIFIED"
    else:
        record["execution"] = {
            "status": "UNVERIFIED",
            "detail": "not under workflows/ — not auto-executed by GitHub Actions",
        }
        record["state"] = "REVIEW_REQUIRED"

    # Governance remains blocked for activation of candidates
    if not under_workflows:
        record["governance"] = {
            "status": "BLOCKED",
            "detail": "candidate must not receive activation without explicit decision",
        }
        record["activation"] = {"status": "DENIED_UNLESS_VERIFIED"}
    else:
        record["governance"] = {
            "status": "BLOCKED",
            "detail": "active location does not imply completed authority/security review",
        }
        record["activation"] = {"status": "DENIED_UNLESS_VERIFIED"}

    return record


def run_inspection() -> dict:
    if not GITHUB.is_dir():
        return {"result": "FAIL", "reason": "NO_GITHUB_DIR", "workflows": []}

    records = []
    for path in sorted(GITHUB.rglob("*")):
        if path.is_file() and path.suffix.lower() in (".yml", ".yaml"):
            records.append(inspect_candidate(path))

    blocked = sum(1 for r in records if r["activation"]["status"] == "DENIED_UNLESS_VERIFIED")
    malformed = sum(1 for r in records if "MALFORMED_YAML" in r.get("risks", []))

    evidence = {
        "verification_id": "GOV-WORKFLOW-SECURITY-INSPECT",
        "repository": "Kelronmos/Structured-Workflow-Intelligence",
        "operation": "inspect_workflow_security",
        "result": "PASS",
        "doctrine": [
            "A workflow file is merely an artifact",
            "Existence, name, location, or historical presence grants no execution authority",
            "workflow_activation_authority: DENIED_UNLESS_VERIFIED",
        ],
        "summary": {
            "inspected": len(records),
            "activation_denied_count": blocked,
            "malformed_count": malformed,
        },
        "workflows": records,
        "limitations": [
            "Static scan only; does not execute workflows",
            "Does not resolve remote action SHAs or OIDC trust",
            "Does not replace human authority review",
            "Governance Backbone remains NOT SEALED",
        ],
    }

    payload = json.dumps(
        {k: v for k, v in evidence.items() if k != "verification_sha256"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    evidence["verification_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return evidence


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = run_inspection()
    out = OUT / "workflow_security_inspection.json"
    out.write_text(
        json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    s = evidence["summary"]
    print(
        f"workflow_security: {evidence['result']} "
        f"inspected={s['inspected']} denied={s['activation_denied_count']} "
        f"malformed={s['malformed_count']} sha256={evidence['verification_sha256']}"
    )
    for w in evidence["workflows"]:
        risks = ",".join(w.get("risks") or []) or "none"
        print(
            f"  {w['path']} state={w['state']} activation={w['activation']['status']} risks={risks}"
        )
    return 0 if evidence["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
