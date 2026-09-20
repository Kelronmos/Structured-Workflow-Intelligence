-------------------------------- MODULE MutD --------------------------------
EXTENDS Integers
VARIABLES step, quarantine_reason, execution_authorized
None == 0
Quarantined == -3
Init == step = 23 /\ quarantine_reason = None /\ execution_authorized = FALSE
BadQ ==
  /\ step = 23 /\ step' = Quarantined /\ quarantine_reason' = None
  /\ UNCHANGED execution_authorized
Next == BadQ
Spec == Init /\ [][Next]_<<step, quarantine_reason, execution_authorized>>
Inv_I_SIM_007 == (step = Quarantined) => (quarantine_reason # None)
=============================================================================
