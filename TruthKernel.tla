----------------------------- MODULE TruthKernel -----------------------------

EXTENDS Naturals, Sequences

VARIABLES log, hashChain

Init ==
  /\ log = << >>
  /\ hashChain = << >>

Append(event) ==
  /\ log' = Append(log, event)
  /\ hashChain' = Append(hashChain, Hash(event, Last(hashChain)))

IntegrityInvariant ==
  \A i \in 1..Len(hashChain):
    hashChain[i] = Hash(log[i], hashChain[i-1])

Spec ==
  Init /\ [][Append(_)]_log

=============================================================================
