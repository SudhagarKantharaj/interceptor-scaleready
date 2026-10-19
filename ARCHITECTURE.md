# Architecture overview

## High-level flow

```text
User
  |
  v
Streamlit UI (tabs, forms, tables, downloads)
  |
  v
Application logic (validation, linking, report assembly)
  |
  v
Local CSV files in ./data/
  |-- research_register.csv
  |-- research_evidence_register.csv
  |-- deployment_dependencies.csv
  |-- deployment_readiness_profile.csv
  `-- operational_actions.csv
```

## Design choices

- **Python + Streamlit:** quick to run locally and suitable for validating a workflow with a small number of users.
- **pandas:** reads, edits, validates, and exports tabular records.
- **CSV persistence:** transparent, easy to inspect, and inexpensive for a local prototype.
- **Source traceability:** connects findings to source material and evidence status.
- **Human decision ownership:** the prototype supports review and coordination; it does not automatically certify readiness.

## Current limitations and future options

CSV is suitable for a local prototype but not concurrent multi-user production use. Streamlit-hosted local files should not be treated as durable storage. If user research validates the need, future options include a persistent database, authentication, role-based permissions, audit history, backups, and secure hosting. Validate the workflow before adding these features.
