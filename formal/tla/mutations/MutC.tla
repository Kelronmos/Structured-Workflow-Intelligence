-------------------------------- MODULE MutC --------------------------------
EXTENDS Integers
VARIABLES step, pause_reason, execution_authorized
None == 0
Paused == -1
Init == step = 23 /\ pause_reason = None /\ execution_authorized = FALSE
BadPause ==
  /\ step = 23 /\ step' = Paused /\ pause_reason' = None
  /\ UNCHANGED execution_authorized
Next == BadPause
Spec == Init /\ [][Next]_<<step, pause_reason, execution_authorized>>
Inv_I_SIM_007 == (step = Paused) => (pause_reason # None)
=============================================================================
