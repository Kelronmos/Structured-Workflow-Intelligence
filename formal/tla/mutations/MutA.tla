-------------------------------- MODULE MutA --------------------------------
EXTENDS Integers
CONSTANTS MaxStep
VARIABLES step, route_rule, evidence_bound, execution_authorized
None == 0
Init ==
  /\ step = 23 /\ route_rule = None
  /\ evidence_bound = TRUE /\ execution_authorized = FALSE
BadSkip ==
  /\ step = 23 /\ step' = MaxStep /\ route_rule' = None
  /\ UNCHANGED <<evidence_bound, execution_authorized>>
Next == BadSkip
Spec == Init /\ [][Next]_<<step, route_rule, evidence_bound, execution_authorized>>
Inv_I_SIM_008 == (step > 24) => (route_rule # None)
=============================================================================
