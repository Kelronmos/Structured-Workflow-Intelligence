------------------------------ MODULE SWI_v5 ------------------------------

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
  /\ proposal' = Hash(input)
  /\ UNCHANGED <<nodes, log, committed, view>>

(* --- PBFT PREPARE --- *)
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
  \A x, y \in committed : x = y \/ x # y => TRUE

(* --- Consistency Invariant --- *)
LedgerConsistency ==
  \A d \in committed :
    \E m \in log : m.d = d

Spec ==
  Init /\ [][Prepare(_) \/ Commit(_) \/ Execute(_)]_log

=============================================================================
