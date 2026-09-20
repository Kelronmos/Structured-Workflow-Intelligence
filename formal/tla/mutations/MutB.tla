-------------------------------- MODULE MutB --------------------------------
EXTENDS Integers
VARIABLES step, halt_reason, execution_authorized
None == 0
Halted == -2
Init == step = 23 /\ halt_reason = None /\ execution_authorized = FALSE
BadHalt ==
  /\ step = 23 /\ step' = Halted /\ halt_reason' = None
  /\ UNCHANGED execution_authorized
Next == BadHalt
Spec == Init /\ [][Next]_<<step, halt_reason, execution_authorized>>
Inv_I_SIM_007 == (step = Halted) => (halt_reason # None)
=============================================================================
