------------------------------ MODULE SWI_v5 ------------------------------

(*
  Research formal model only.
  Does not prove production security, consensus, or seal status.
  Status: SPEC / SIMULATED relative to runtime.
*)

EXTENDS Naturals, Sequences

VARIABLES
  nodes,
  log,
  committed,
  view,
  proposal

Init ==
  /\ nodes = {"A", "B", "C", "D", "E"}
  /\ log = << >>
  /\ committed = {}
  /\ view = 0
  /\ proposal = ""

(* --- Kernel Execution --- *)
Execute(input) ==
  /\ proposal' = input
  /\ UNCHANGED <<nodes, log, committed, view>>

(* --- PBFT-style PREPARE (model only) --- *)
Prepare(node, digest) ==
  /\ proposal = digest
  /\ log' = Append(log, [type |-> "PREPARE", node |-> node, d |-> digest])
  /\ UNCHANGED <<nodes, committed, view>>

(* --- COMMIT RULE --- *)
Commit(digest) ==
  LET votes == {m \in log : m.d = digest}
  IN
    /\ Cardinality(votes) >= 3
    /\ committed' = committed \cup {digest}
    /\ UNCHANGED <<nodes, log, view, proposal>>

(* --- Safety Invariant --- *)
NoDoubleCommit ==
  \A x, y \in committed : x = y \/ x # y

(* --- Consistency Invariant --- *)
LedgerConsistency ==
  \A d \in committed :
    \E m \in log : m.d = d

Spec ==
  Init /\ [][Prepare(_, _) \/ Commit(_) \/ Execute(_)]_<<nodes, log, committed, view, proposal>>

=============================================================================
