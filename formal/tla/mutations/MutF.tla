-------------------------------- MODULE MutF --------------------------------
EXTENDS Integers
VARIABLES step, authority, execution_authorized
Init == step = 23 /\ authority = 1 /\ execution_authorized = FALSE
BadEscalation ==
  /\ step = 23 /\ authority' = authority + 1
  /\ UNCHANGED <<step, execution_authorized>>
Next == BadEscalation
Spec == Init /\ [][Next]_<<step, authority, execution_authorized>>
Inv_NoSilentAuthIncrease == authority <= 1
=============================================================================
