"""SWI Admission Control Package.

Core rule: Source code is not authority.
A module becomes executable only after structure, contract,
implementation, tests, dependencies, integrity and seal
have been independently verified.

Default state: DENY
"""

from .validator import validate, admit
from .halt import halt
from .seal_verifier import verify_seal
from .dependency_gate import check_dependencies

__all__ = [
    "validate",
    "admit",
    "halt",
    "verify_seal",
    "check_dependencies",
]
