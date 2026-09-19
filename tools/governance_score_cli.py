#!/usr/bin/env python3
"""
SWI governance red-team score CLI (research tool).

Status: RESEARCH / NOT production verification.
Does not establish SEALED, production_ready, or EU AI Act compliance.
Use only against local fixtures; treat output as diagnostic, not certification.
"""

import json
import sys
import copy

REQUIRED_FIELDS = [
    "execution_trace",
]

CRITICAL_FAILURE_FLAGS = [
    "unlogged_action",
    "missing_evidence",
    "invalid_auth_token",
    "rollback_possible_false_commit",
    "identity_drift",
    "signature_missing",
]


def flatten(trace):
    return json.dumps(trace).lower()


def detect_failures(trace):
    flat = flatten(trace)
    failures = []

    if "execution_trace" not in trace:
        failures.append("execution_trace_missing")

    for flag in CRITICAL_FAILURE_FLAGS:
        if flag in flat:
            failures.append(flag)

    steps = trace.get("execution_trace", [])

    if not isinstance(steps, list) or len(steps) == 0:
        failures.append("empty_or_invalid_trace")

    step_ids = [s.get("step") for s in steps if isinstance(s, dict)]
    if len(step_ids) != len(set(step_ids)):
        failures.append("duplicate_step_ids_detected")

    for s in steps:
        if s.get("action") == "commit":
            evidence = s.get("evidence", {})
            if evidence.get("rollback_possible") is False:
                failures.append("rollback_invalidation_detected")

    return list(set(failures))


def inject_attack(trace):
    attacked = copy.deepcopy(trace)
    steps = attacked.get("execution_trace", [])

    if steps:
        if "evidence" in steps[0]:
            steps[0]["evidence"].pop("signature", None)

        steps.append({
            "step": 999,
            "action": "unlogged_action",
            "input_state": "unknown",
            "output_state": "unknown",
            "evidence": {},
        })

    return attacked


def compute_score(failures):
    base = 100
    penalty_map = {
        "execution_trace_missing": 40,
        "empty_or_invalid_trace": 30,
        "unlogged_action": 25,
        "missing_evidence": 15,
        "invalid_auth_token": 15,
        "rollback_invalidation_detected": 20,
        "duplicate_step_ids_detected": 10,
        "identity_drift": 20,
        "signature_missing": 10,
    }

    for f in failures:
        base -= penalty_map.get(f, 5)

    return max(0, base)


def rank(score):
    if score <= 20:
        return "R0 - FAIL (non-auditable)"
    if score <= 40:
        return "R1 - HIGH RISK"
    if score <= 60:
        return "R2 - PARTIAL GOVERNANCE"
    if score <= 80:
        return "R3 - STRUCTURED BUT WEAK"
    if score <= 95:
        return "R4 - STRONG"
    return "R5 - DETECTABLE HIGH INTEGRITY"


def run(trace):
    original_failures = detect_failures(trace)
    attacked_trace = inject_attack(trace)
    attacked_failures = detect_failures(attacked_trace)

    original_score = compute_score(original_failures)
    attacked_score = compute_score(attacked_failures)

    return {
        "original": {
            "failures": original_failures,
            "score": original_score,
            "rank": rank(original_score),
        },
        "red_team_attack": {
            "failures": attacked_failures,
            "score": attacked_score,
            "rank": rank(attacked_score),
        },
        "governance_verdict": "FAIL" if attacked_score < 80 else "PASS",
        "delta_resilience_drop": original_score - attacked_score,
        "disclaimer": "RESEARCH diagnostic only; not seal evidence or production certification",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/governance_score_cli.py input.json", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    trace = {"execution_trace": data.get("execution_trace", [])}
    result = run(trace)
    print(json.dumps(result, indent=2))
