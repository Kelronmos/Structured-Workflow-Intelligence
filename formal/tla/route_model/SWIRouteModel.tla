---------------------------- MODULE SWIRouteModel ----------------------------
(***************************************************************************)
(* Abstract route machine: I-SIM-007 / I-SIM-008 / I-SIM-003                *)
(* FORMAL MODEL ONLY — not SWI runtime. PROPOSED / NOT_IMPLEMENTED.        *)
(***************************************************************************)
EXTENDS Integers, FiniteSets, TLC

CONSTANTS MaxStep

VARIABLES
  step,
  pause_reason,
  halt_reason,
  quarantine_reason,
  route_rule,
  evidence_bound,
  execution_authorized

None == 0
R1 == 1
R2 == 2
Reasons == {None, R1, R2}

TerminalPaused == -1
TerminalHalted == -2
TerminalQuarantined == -3

TypeOK ==
  /\ step \in (23..MaxStep) \cup {TerminalPaused, TerminalHalted, TerminalQuarantined}
  /\ pause_reason \in Reasons
  /\ halt_reason \in Reasons
  /\ quarantine_reason \in Reasons
  /\ route_rule \in Reasons
  /\ evidence_bound \in BOOLEAN
  /\ execution_authorized \in BOOLEAN

Init ==
  /\ step = 23
  /\ pause_reason = None
  /\ halt_reason = None
  /\ quarantine_reason = None
  /\ route_rule = None
  /\ evidence_bound = TRUE
  /\ execution_authorized = FALSE

Advance ==
  /\ step \in 23..(MaxStep - 1)
  /\ step' = step + 1
  /\ route_rule' = None
  /\ UNCHANGED <<pause_reason, halt_reason, quarantine_reason,
                 evidence_bound, execution_authorized>>

SkipWithRule ==
  /\ step \in 23..(MaxStep - 2)
  /\ \E dest \in (step + 2)..MaxStep :
       /\ step' = dest
  /\ route_rule' \in {R1, R2}
  /\ evidence_bound = TRUE
  /\ UNCHANGED <<pause_reason, halt_reason, quarantine_reason,
                 evidence_bound, execution_authorized>>

Pause ==
  /\ step \in 23..MaxStep
  /\ step' = TerminalPaused
  /\ pause_reason' \in {R1, R2}
  /\ UNCHANGED <<halt_reason, quarantine_reason, route_rule,
                 evidence_bound, execution_authorized>>

Halt ==
  /\ step \in 23..MaxStep
  /\ step' = TerminalHalted
  /\ halt_reason' \in {R1, R2}
  /\ UNCHANGED <<pause_reason, quarantine_reason, route_rule,
                 evidence_bound, execution_authorized>>

Quarantine ==
  /\ step \in 23..MaxStep
  /\ step' = TerminalQuarantined
  /\ quarantine_reason' \in {R1, R2}
  /\ UNCHANGED <<pause_reason, halt_reason, route_rule,
                 evidence_bound, execution_authorized>>

Next ==
  \/ Advance
  \/ SkipWithRule
  \/ Pause
  \/ Halt
  \/ Quarantine

vars == <<step, pause_reason, halt_reason, quarantine_reason,
          route_rule, evidence_bound, execution_authorized>>

Spec == Init /\ [][Next]_vars

Inv_TerminalJustified ==
  /\ (step = TerminalHalted => halt_reason # None)
  /\ (step = TerminalPaused => pause_reason # None)
  /\ (step = TerminalQuarantined => quarantine_reason # None)

Inv_NoExecutionAuth ==
  execution_authorized = FALSE

Inv_TypeOK == TypeOK

Safety ==
  /\ Inv_TypeOK
  /\ Inv_TerminalJustified
  /\ Inv_NoExecutionAuth

=============================================================================
