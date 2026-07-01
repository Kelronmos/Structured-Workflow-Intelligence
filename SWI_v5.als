sig Node {}

sig Digest {}

sig LogEntry {
  node: one Node,
  digest: one Digest
}

sig Ledger {
  entries: set LogEntry,
  committed: set Digest
}

fact NoInvalidCommit {
  all l: Ledger |
    l.committed in l.entries.digest
}

fact NoForks {
  all l: Ledger |
    all disj d1, d2: l.committed |
      d1 != d2 implies true
}

pred consistent[l: Ledger] {
  all d: l.committed |
    some e: l.entries | e.digest = d
}
