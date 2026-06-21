----------------------- MODULE TruthKernel -------------------------
(*
  TLA+ Specification for SWI Truth Kernel
  
  This module formalizes the core governance kernel behavior:
  - Request evaluation against policy
  - Deterministic decision production
  - Receipt generation and chaining
  - Replay validation for audit integrity
*)

EXTENDS Naturals, Sequences, FiniteSets

CONSTANT MaxRequests
CONSTANT MaxReceipts
CONSTANT Policies

(*
  State Machine Definition
*)

VARIABLE
  requests,        \* Sequence of incoming requests
  decisions,       \* Map: RequestHash -> Decision
  receipts,        \* Sequence of chained receipts
  policyVersion,   \* Current active policy version
  ledgerHash,      \* Hash chain anchor
  requestCounter

(*
  Receipt Structure
  
  Receipt ::= [
    receiptId       |-> string,
    requestHash     |-> hash,
    decisionHash    |-> hash,
    policyVersion   |-> version,
    timestamp       |-> timestamp,
    previousHash    |-> hash,
    signature       |-> signature (optional)
  ]
*)

Receipts == UNION {[
    receiptId: 1..MaxReceipts,
    requestHash: STRING,
    decisionHash: STRING,
    policyVersion: STRING,
    timestamp: Nat,
    previousHash: STRING
  ]}

(*
  Decision Outcomes
*)

Decisions == {"EXECUTE", "REJECT", "REQUIRE_HUMAN", "AUDIT_ONLY"}

(*
  Initialization
*)

Init ==
  /\ requests = <<>>
  /\ decisions = {}
  /\ receipts = <<>>
  /\ policyVersion = "1.0"
  /\ ledgerHash = "genesis"
  /\ requestCounter = 0

(*
  Request Arrival
  
  A new request enters the kernel for evaluation.
  Precondition: Request is well-formed
  Postcondition: Request is queued for evaluation
*)

RequestArrive(req) ==
  /\ Len(requests) < MaxRequests
  /\ requests' = Append(requests, req)
  /\ requestCounter' = requestCounter + 1
  /\ UNCHANGED <<decisions, receipts, policyVersion, ledgerHash>>

(*
  Evaluate
  
  The kernel evaluates a request against current policy.
  Determinism Requirement: Same request + policy must always produce identical decision.
  
  Precondition: Request in queue, policy loaded
  Postcondition: Decision recorded, hash computed
*)

Evaluate(idx) ==
  /\ idx <= Len(requests)
  /\ LET req == requests[idx]
         policy == policyVersion
     IN
       /\ ~(req.hash \in DOMAIN decisions)  \* Not yet decided
       /\ LET decision == PolicyEngine(req, policy)
          IN
            /\ decisions' = decisions @@ (req.hash :> decision)
            /\ UNCHANGED <<requests, receipts, policyVersion, ledgerHash, requestCounter>>

(*
  Record
  
  A decision is committed to the append-only ledger as a Receipt.
  Hash chaining ensures immutability and tamper detection.
  
  Precondition: Decision exists, not yet receipted
  Postcondition: Receipt appended, hash chain updated
*)

Record(requestHash) ==
  /\ requestHash \in DOMAIN decisions
  /\ Len(receipts) < MaxReceipts
  /\ LET decision == decisions[requestHash]
         previousReceipt == IF Len(receipts) = 0 
                           THEN [hash |-> ledgerHash]
                           ELSE receipts[Len(receipts)]
         newReceipt == [
           receiptId |-> Len(receipts) + 1,
           requestHash |-> requestHash,
           decisionHash |-> Hash(decision),
           policyVersion |-> policyVersion,
           timestamp |-> requestCounter,
           previousHash |-> previousReceipt.hash
         ]
     IN
       /\ receipts' = Append(receipts, newReceipt)
       /\ ledgerHash' = Hash(newReceipt)
       /\ UNCHANGED <<requests, decisions, policyVersion, requestCounter>>

(*
  Replay
  
  Reconstructs decision history from ledger for audit/forensics.
  Determinism guarantee: Given same ledger + policies, replay must be bit-identical.
  
  Precondition: Receipts exist, original events available
  Postcondition: Replayed decisions match original
*)

Replay(startIdx, endIdx) ==
  /\ startIdx >= 1
  /\ endIdx <= Len(receipts)
  /\ startIdx <= endIdx
  /\ LET replayResults == [i \in startIdx..endIdx |->
       LET receipt == receipts[i]
           policy == receipt.policyVersion
           \* Note: Original request must be available in audit log
       IN
         Hash(PolicyEngine(AuditLog[receipt.requestHash], policy))
     ]
     IN
       /\ \A i \in startIdx..endIdx :
            replayResults[i] = receipts[i].decisionHash
       /\ UNCHANGED <<requests, decisions, receipts, policyVersion, ledgerHash, requestCounter>>

(*
  Verify
  
  Validates receipt integrity: hash chain, signatures, policy version consistency.
  
  Precondition: Receipts exist
  Postcondition: Integrity verified or corruption detected
*)

Verify(idx) ==
  /\ idx >= 1
  /\ idx <= Len(receipts)
  /\ LET receipt == receipts[idx]
         expectedPrevHash == IF idx = 1 
                            THEN ledgerHash 
                            ELSE receipts[idx - 1].hash
     IN
       /\ receipt.previousHash = expectedPrevHash
       /\ receipt.policyVersion \in ValidPolicies
       /\ UNCHANGED <<requests, decisions, receipts, policyVersion, ledgerHash, requestCounter>>

(*
  Next-State Relation
*)

Next ==
  \/ \E req \in Requests : RequestArrive(req)
  \/ \E idx \in 1..Len(requests) : Evaluate(idx)
  \/ \E rh \in DOMAIN decisions : Record(rh)
  \/ \E start, end \in 1..MaxReceipts : Replay(start, end)
  \/ \E idx \in 1..Len(receipts) : Verify(idx)

(*
  Type Invariant
*)

TypeOK ==
  /\ requests \in Seq(Requests)
  /\ decisions \in [Nat -> Decisions]
  /\ receipts \in Seq(Receipts)
  /\ policyVersion \in STRING
  /\ ledgerHash \in STRING
  /\ requestCounter \in Nat

(*
  Safety Invariants
*)

\* INV1: Determinism
\* Same request evaluated twice must produce identical decision
DeterminismInvariant ==
  \A r1, r2 \in 1..Len(requests) :
    (requests[r1] = requests[r2]) =>
      (decisions[Hash(requests[r1])] = decisions[Hash(requests[r2])])

\* INV2: Receipt Immutability
\* Once a receipt is recorded, it cannot be modified
ReceiptImmutabilityInvariant ==
  \A i \in 1..Len(receipts) :
    ~(\E j \in 1..Len(receipts) : i /= j /\ receipts[i] = receipts[j])

\* INV3: Hash Chain Integrity
\* Each receipt's previousHash must match previous receipt's hash
HashChainInvariant ==
  \A i \in 2..Len(receipts) :
    receipts[i].previousHash = Hash(receipts[i-1])

\* INV4: Policy Version Consistency
\* All receipts reference valid policy versions
PolicyVersionInvariant ==
  \A i \in 1..Len(receipts) :
    receipts[i].policyVersion \in ValidPolicies

\* Combined Safety Invariant
AllInvariants ==
  /\ TypeOK
  /\ DeterminismInvariant
  /\ ReceiptImmutabilityInvariant
  /\ HashChainInvariant
  /\ PolicyVersionInvariant

(*
  Fairness Constraints
*)

Fairness ==
  /\ WF_<<requests, decisions, receipts, policyVersion, ledgerHash, requestCounter>>(Next)

(*
  Specification
*)

Spec == Init /\ [][Next]_vars /\ Fairness

(*
  Properties to Model Check
*)

\* PROP1: Determinism is preserved across state transitions
DeterminismProperty ==
  []DeterminismInvariant

\* PROP2: Receipt chain is never corrupted
IntegrityProperty ==
  []HashChainInvariant

\* PROP3: Every decision eventually produces a receipt
LivenessProperty ==
  \A i \in 1..Len(requests) :
    (requests[i] \in requests) ~> (Hash(requests[i]) \in DOMAIN decisions)

=======================================================================
