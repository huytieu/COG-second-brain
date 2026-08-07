# Evidence Ledger

Use one row per observed acceptance-criterion result. Evidence should describe what was actually observed and point to the artifact, command, URL, or file that supports the result.

| Acceptance criterion | Checkpoint | Result | Observation | Artifact |
|---|---|---|---|---|

## Evidence row contract

```text
EVIDENCE <AC-id> | <checkpoint> | PASS|FAIL | <observation> | <artifact-path-or-command>
```

`SKIP` is intentionally not an evidence result. A skipped checkpoint is a lifecycle event, not proof that an acceptance criterion passed or failed. Record skipped checkpoints in `checkpoints.tsv` only.

A criterion is ready to ship only when it has at least one relevant `PASS` evidence row. Keep raw checkpoint events in `checkpoints.tsv`; use this ledger for criterion-traced verification evidence.
