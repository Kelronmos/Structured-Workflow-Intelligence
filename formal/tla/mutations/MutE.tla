-------------------------------- MODULE MutE --------------------------------
EXTENDS Integers
VARIABLES step, execution_authorized
Init == step = 23 /\ execution_authorized = FALSE
BadAuth ==
  /\ step = 23 /\ execution_authorized' = TRUE /\ UNCHANGED step
Next == BadAuth
Spec == Init /\ [][Next]_<<step, execution_authorized>>
Inv_I_SIM_003 == execution_authorized = FALSE
=============================================================================
