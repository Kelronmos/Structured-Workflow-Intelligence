"""Determinism Test Fixtures for SWI Truth Kernel.

These fixtures validate bit-identical behavior across:
- Multiple runs (same runtime)
- Cross-runtime (Python ↔ TypeScript)
- Time-independent execution (no clock-dependent operations)
- Serialization stability (canonical JSON ordering)

Usage:
    pytest tests/determinism_fixtures.py -v
    python scripts/cross_runtime_test.py
"""

import json
import hashlib
from typing import Any, Dict, List
from dataclasses import dataclass, asdict
from enum import Enum


class Decision(Enum):
    """Decision outcomes from policy evaluation."""
    EXECUTE = "EXECUTE"
    REJECT = "REJECT"
    REQUIRE_HUMAN = "REQUIRE_HUMAN"
    AUDIT_ONLY = "AUDIT_ONLY"


@dataclass
class Request:
    """Canonical request structure for determinism testing."""
    action: str
    corridor: str
    actor: str
    context: Dict[str, Any]
    timestamp: int  # FIXED: Do not use system time; use provided value
    
    def to_canonical_json(self) -> str:
        """Serialize to canonical JSON (sorted keys, no whitespace)."""
        return json.dumps(
            asdict(self),
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=True
        )
    
    def hash(self) -> str:
        """Compute deterministic SHA256 hash."""
        return hashlib.sha256(
            self.to_canonical_json().encode('utf-8')
        ).hexdigest()


@dataclass
class Receipt:
    """Audit receipt with hash chain."""
    receipt_id: int
    request_hash: str
    decision_hash: str
    policy_version: str
    timestamp: int
    previous_hash: str
    
    def to_canonical_json(self) -> str:
        return json.dumps(
            asdict(self),
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=True
        )
    
    def hash(self) -> str:
        return hashlib.sha256(
            self.to_canonical_json().encode('utf-8')
        ).hexdigest()


class DeterminismTestFixtures:
    """Test fixture collection for determinism validation."""
    
    # Fixture 1: Simple request with AHMR pass
    AHMR_PASS_REQUEST = Request(
        action="financial_transfer",
        corridor="FINANCIAL",
        actor="SYSTEM_SEEDER",
        context={
            "amount": 1000,
            "recipient": "user_123",
            "human_signoff": True,
            "attestation_token": "valid_token_xyz"
        },
        timestamp=1000000  # Fixed epoch
    )
    
    # Fixture 2: Request with AHMR fail
    AHMR_FAIL_REQUEST = Request(
        action="financial_transfer",
        corridor="FINANCIAL",
        actor="SYSTEM_SEEDER",
        context={
            "amount": 5000,
            "recipient": "user_456",
            "human_signoff": False,  # Missing approval
            "attestation_token": "valid_token_xyz"
        },
        timestamp=1000001
    )
    
    # Fixture 3: Complex request with nested context
    COMPLEX_NESTED_REQUEST = Request(
        action="policy_deployment",
        corridor="GOVERNANCE",
        actor="ADMIN",
        context={
            "policy_id": "pol_456",
            "rules": [
                {"condition": "actor == SEEDER", "action": "BLOCK"},
                {"condition": "corridor == FINANCIAL", "action": "REQUIRE_HUMAN"}
            ],
            "metadata": {
                "created_by": "security_team",
                "reviewed": True,
                "review_date": "2026-06-21"
            }
        },
        timestamp=1000002
    )
    
    # Fixture 4: Edge case - empty context
    EMPTY_CONTEXT_REQUEST = Request(
        action="query",
        corridor="PUBLIC",
        actor="ANONYMOUS",
        context={},
        timestamp=1000003
    )
    
    # Fixture 5: Edge case - special characters and unicode
    UNICODE_REQUEST = Request(
        action="audit_log_review",
        corridor="AUDIT",
        actor="COMPLIANCE_OFFICER",
        context={
            "query": "Governance policy: 治理 (zhìlǐ) ✓",
            "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?"
        },
        timestamp=1000004
    )
    
    # Fixture 6: Large request with many fields
    LARGE_REQUEST = Request(
        action="batch_audit_export",
        corridor="AUDIT",
        actor="AUDITOR",
        context={
            "date_range": {"start": "2026-01-01", "end": "2026-06-21"},
            "filters": {
                "action_types": ["EXECUTE", "REJECT", "REQUIRE_HUMAN"],
                "corridors": ["FINANCIAL", "GOVERNANCE", "AUDIT"],
                "actors": [f"actor_{i}" for i in range(10)]
            },
            "export_format": "json"
        },
        timestamp=1000005
    )
    
    @classmethod
    def all_fixtures(cls) -> List[Request]:
        """Return all test fixtures."""
        return [
            cls.AHMR_PASS_REQUEST,
            cls.AHMR_FAIL_REQUEST,
            cls.COMPLEX_NESTED_REQUEST,
            cls.EMPTY_CONTEXT_REQUEST,
            cls.UNICODE_REQUEST,
            cls.LARGE_REQUEST
        ]


class DeterminismValidator:
    """Utility for validating deterministic behavior."""
    
    def __init__(self, runs: int = 5):
        self.runs = runs
        self.hashes = {}  # track hashes across runs
    
    def validate_single_runtime(
        self,
        evaluate_fn,
        fixture: Request,
        runs: int = None
    ) -> bool:
        """Validate determinism within a single runtime.
        
        Args:
            evaluate_fn: Function(request) -> decision
            fixture: Test request
            runs: Number of evaluation runs (uses self.runs if None)
        
        Returns:
            True if all runs produce identical hash
        """
        runs = runs or self.runs
        hashes = []
        
        for i in range(runs):
            decision = evaluate_fn(fixture)
            decision_json = json.dumps(
                {"decision": decision.value},
                sort_keys=True,
                separators=(',', ':')
            )
            decision_hash = hashlib.sha256(
                decision_json.encode('utf-8')
            ).hexdigest()
            hashes.append(decision_hash)
        
        return all(h == hashes[0] for h in hashes)
