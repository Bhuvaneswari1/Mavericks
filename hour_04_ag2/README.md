# Hour 4 — Conversation-driven agents with AG2 Classic

## Banking use case

Have a banking buddy answer a customer; then let planner, writer and critic refine the same source-grounded service response.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Complete the previous hour and explain its output before continuing.

## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | ConversableAgent exchanges messages. GroupChat holds conversation; GroupChatManager coordinates it. Discuss round robin versus automatic speaker selection, DONE! and bounded turns. |
| 12–36 | Run two-agent mode. In live mode inspect initiate_chat and chat_history. Human input is NEVER for reproducible automated runs; discuss ALWAYS as a classroom experiment. |
| 36–60 | Run --group. Read the Planner → Writer → Critic hand-offs and DONE! stop. Change max_round deliberately and explain early truncation. |

## Files explained

- main.py: bounded agents with code execution disabled, evidence seeded into prompts, two-agent initiate_chat branch, GroupChat/GroupChatManager branch and termination predicate.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** Policy CSV/PDF and question. Live mode requires AG2 Classic installed and provider credentials.

**Workflow:** Run two-agent mode. In live mode inspect initiate_chat and chat_history. Human input is NEVER for reproducible automated runs; discuss ALWAYS as a classroom experiment.

**Output:** A JSON transcript; live group mode also prints AG2 conversation logs.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python hour_04_ag2/main.py --group --question "What documents for account opening?"
```

For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Isolated live lab setup

Use a new terminal at the project root (Python 3.11).

```bash
python -m venv .venv-ag2
# macOS / Linux
source .venv-ag2/bin/activate
# Windows PowerShell: .venv-ag2\Scripts\Activate.ps1
python -m pip install -r requirements-ag2.txt
```

Edit the same root `.env`, set DEMO_MODE=false and fill your provider settings.
The offline simulation needs no framework installation but does not exercise its API.
Return to the main `.venv` for Hours 5–6.

## Checkpoint and exercise

Conversation ends at DONE! or the turn/round cap; cited claims match supplied evidence. Round-robin group selection is intentionally deterministic.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?

Your three messages are produced as follows:
Speaker	Output content	How it is created
Customer	Your account-opening question	Copies question
Buddy	Retrieved policy text and source	Converts evidence into a JSON string
Critic	Source-checking reminder ending in DONE!

