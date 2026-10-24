# Hour 6 — Capstone: assemble Banking Service Buddy

## Banking use case

Deliver a local interface where learners upload bank policy CSV/PDF and synthetic request CSV, ask questions and download the result.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Complete the previous hour and explain its output before continuing.

## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | Compare CrewAI roles/tasks, AG2 conversations and LangGraph explicit routing. Pick LangGraph for this capstone. Discuss loops, cost, hallucination and source checking. |
| 12–48 | Build (36 min): launch Streamlit, inspect inputs, run all three graph routes, upload the PDF, download a JSON result. Pair up: one operates, one checks evidence. |
| 48–60 | Demo (12 min): each pair answers one unseen supported question, one unknown question, and one request lookup; explain the path and limitations. |

## Files explained

- app.py: Streamlit layout, upload controls, temporary file lifecycle, validation, graph execution, session-state result, error UI and JSON download.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** Browser question; optional policy CSV/PDF and request CSV uploads; semantic checkbox; root .env.

**Workflow:** Supervisor chooses a worker, worker reads validated evidence, reviewer attaches provenance note, UI renders state.

**Output:** Browser answer, sources, review and node path; downloadable banking_result.json.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python -m streamlit run hour_06_streamlit/app.py
```
in .env

DEMO_MODE=true

then run the app

python -m streamlit run hour_06_streamlit/app.py \
  --server.fileWatcherType none


For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Checkpoint and exercise

Demonstrate CSV and PDF inputs, SR1001, unknown SR9999 and unsupported question. Stop app with Ctrl+C; downloaded JSON remains with the learner.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?
