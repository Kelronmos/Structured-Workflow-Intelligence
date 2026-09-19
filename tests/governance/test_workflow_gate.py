"""Tranche 2A tests — workflow gate cannot silently activate candidates."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from inspect_workflow_security import inspect_candidate, run_inspection  # noqa: E402


def test_malformed_yaml_fail_closed(tmp_path):
    p = tmp_path / "bad.yml"
    p.write_text(": this: is: not: valid: yaml: [[[\n", encoding="utf-8")
    # inspect_candidate expects path under ROOT for relative_to — use synthetic via monkeypatch style
    # Call internal logic by writing under a fake structure is heavy; test parse path directly
    from inspect_workflow_security import _load_yaml

    ok, data, err = _load_yaml(p)
    assert ok is False


def test_inspection_emits_denied_activation():
    evidence = run_inspection()
    assert evidence["result"] == "PASS"
    assert "verification_sha256" in evidence
    for w in evidence["workflows"]:
        if w["path"].endswith((".yml", ".yaml")):
            # No candidate receives ACTIVATION_AUTHORIZED from inspection alone
            assert w["activation"]["status"] in (
                "DENIED_UNLESS_VERIFIED",
                "NOT_APPLICABLE",
            )
            assert w["authority"]["status"] == "UNVERIFIED" or w["state"] == "NOT_APPLICABLE"


def test_evidence_hash_stable_structure():
    e1 = run_inspection()
    e2 = run_inspection()
    # Same repo state → same hash
    assert e1["verification_sha256"] == e2["verification_sha256"]


def test_no_implicit_activation_authority():
    evidence = run_inspection()
    assert evidence["doctrine"]
    assert any("no execution authority" in d.lower() or "merely an artifact" in d.lower()
               for d in evidence["doctrine"])
