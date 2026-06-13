import hashlib
import json

def generate_proof(event, state_before, state_after, audit_log):
    """
    Post-execution artifact builder.
    Consumes verified state transitions from the SWI kernel.
    Produces a causally bound cryptographic proof artifact.
    """
    event_str = json.dumps(event, sort_keys=True).encode("utf-8")
    event_hash = hashlib.sha256(event_str).hexdigest()

    state_transition_str = json.dumps({
        "before": state_before,
        "after": state_after
    }, sort_keys=True).encode("utf-8")
    
    state_transition_hash = hashlib.sha256(state_transition_str).hexdigest()

    return {
        "event_hash": event_hash,
        "state_transition": state_transition_hash,
        "audit_link": audit_log.get("id", "unknown_audit_link")
    }
