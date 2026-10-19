# Interceptor ScaleReady

**Independent research prototype for river-cleanup deployment and sustainable operations.**

Interceptor ScaleReady explores a workflow for connecting research evidence, deployment dependencies, readiness assessments, operational actions, handover notes, and a consolidated report.

> This is an independent, early-stage concept. It is not an official product of The Ocean Cleanup or UNDP, and it does not certify the readiness of any real deployment. Illustrative records are not verified operational findings.

## Live demo

The live URL will be added here after deployment on Streamlit Community Cloud.

## Features

- Research question register
- Evidence register and source-to-claim traceability
- Deployment dependency checklist
- Deployment readiness profile
- Action ownership and handover tracking
- Integrated readiness report and CSV/TXT exports

## Run locally

Requires Python 3.11 or newer (Python 3.12 is a good deployment target).

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The application creates a local `data/` folder and initializes starter CSV records when needed. Local CSV files are intentionally excluded from Git so private working records are not accidentally published.

## Deploy publicly for a portfolio demo

1. Create a **public GitHub repository** named `interceptor-scaleready`.
2. Upload the contents of this project folder to the repository root (including `app.py`, `requirements.txt`, `.gitignore`, `.streamlit/`, and `docs/`). Do not upload `.venv/`, secrets, or your local `data/*.csv` files.
3. Sign in at <https://share.streamlit.io/> using GitHub and authorize access to the repository.
4. Choose **Create app**, select your repository, branch `main`, and entrypoint `app.py`.
5. Optionally choose a memorable app subdomain, then deploy.
6. Wait for the build to finish, open the generated `https://....streamlit.app` URL, and test each tab and export.
7. Paste the resulting live URL into the **Live demo** section above and share it with viewers.

## Important public-demo limitations

- This prototype uses CSV files on the app's local filesystem, not a hosted database.
- On a public deployment, visitors may be able to edit the same shared demo records. Do not enter confidential, personal, or operationally sensitive information.
- Files written to a hosted app's local filesystem are not durable storage; they can be lost when the app restarts or is rebuilt. Treat the hosted app as an illustrative demo, not a multi-user production service.
- Before using it with real teams or real deployment data, add authentication/authorization and a persistent database, then test concurrency, backups, audit history, and data handling.

## Architecture and demo materials

- [Architecture overview](docs/ARCHITECTURE.md)
- [5–7 minute demo script](docs/DEMO_SCRIPT.md)
- [Prospective-user feedback questions](docs/USER_FEEDBACK_QUESTIONS.md)

## Research principle

Distinguish documented facts from hypotheses and unknowns. A missing public record does not prove a problem exists. Evidence should support the specific claim being made, and readiness decisions remain with accountable humans.
