# Trainer run sheet

Before class: install Python 3.11; rehearse each environment; pre-download MiniLM; confirm
provider tool-call support and available quotas. Run every lesson with DEMO_MODE=true,
then rehearse the live paths separately. Keep demo mode available when network fails.
Avoid switching framework environments in one shell without checking `python -m pip --version`.
Do not distribute a shared key in source files. Give participants scoped credentials securely.

## Pacing and checkpoints

| Hour | Check at ~minute 22 | Check at ~minute 45 | Exit ticket |
|---|---|---|---|
| 1 | SR1001 prints Pending | Learner identifies tool schema/result | Explain reason → act → observe |
| 2 | Source P001 appears | PDF and semantic retrieval work | Explain unknown-answer behavior |
| 3 | Research task returns evidence | Three task outputs are visible | Explain why reviewer can still fail |
| 4 | Two-agent chat terminates | Group reaches Critic or bounded stop | Explain termination versus max rounds |
| 5 | Learner traces policy route | All three routes tested | Explain state and conditional edge |
| 6 | Streamlit runs | Upload and export work | Demo and source-check an unseen question |

The full six hours contain 72 minutes theory and 288 practical minutes. Any breaks consume
lab time; add breaks outside the six instructional hours if your schedule permits. Pair
programming: driver runs, navigator predicts and checks, then swap each hour.

## Worked demonstration

1. SR1001 → Pending and branch follow-up; SR9999 → not found.
2. Account opening → identity/address proof, P001 or PDF page 1.
3. Lost card → official app/branch; assistant cannot block a card.
4. Lunar loan fee → unsupported; inspect false positives if semantic cutoff admits a passage.
5. Upload malformed CSV → readable error; restore sample file.
6. Download JSON and identify route, sources, steps and review note.

## Framework comparison

| Framework | Natural fit here | Main teaching caution |
|---|---|---|
| CrewAI | Sequential research/draft/review tasks | Extra roles do not ensure correctness |
| AG2 Classic | Explicit conversations and group critique | Bound turns; disable code execution |
| LangGraph | Inspectable routing and shared state | Route rules are only as complete as their design |

The AG2 classic namespace `autogen` used here differs from Microsoft's newer Agent Framework.
The capstone reuses the same data/tools, but does not nest CrewAI and AG2 inside LangGraph;
those are alternate orchestration lessons. The final graph uses policy and request workers.

## Evaluation (10 points)

Award 2 points each for correct input preparation, explaining evidence retrieval, explaining
framework hand-offs, demonstrating graph routing, and showing a supported plus unsupported
question in Streamlit. Require the learner to open the cited source and compare the claim.

## Rescue and extensions

API unavailable: set demo mode and label simulations honestly. Embedding model unavailable:
remove --semantic / clear the UI checkbox. PDF extraction fails: use supplied text PDF or CSV.
A dependency conflict: use the separate environment, never change imports randomly.
After successful rehearsal, create environment-specific lockfiles using `python -m pip freeze`.
Extensions: add a new policy, evaluate retrieval on 10 held-out questions, add authentication
as a separate project, or replace keyword routing with a constrained model classifier.
