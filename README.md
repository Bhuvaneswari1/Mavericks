# Banking Service Buddy — six-hour fresher workshop

Build one fictional bank service assistant, one hour at a time. Begin with a tool call,
add policy knowledge, compare two multi-agent frameworks, orchestrate workers with
LangGraph, and finish with a Streamlit application. All bank rules and records here
are invented training data. No transactions or real account access occur.

## Start here

Prerequisites: Python 3.11, a terminal, editor, and basic Python functions/dictionaries.
Run every command below **from this project root**, the directory containing this README.
The default demo mode needs no API key. It uses scripted role outputs and lexical
retrieval; it does not simulate actual LLM intelligence. Hour 5 and the final app still
execute a real LangGraph in demo mode.

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# macOS / Linux
cp .env.example .env
# Windows PowerShell instead: Copy-Item .env.example .env
python hour_01_llm_and_tools/main.py
python hour_02_rag/main.py
python hour_05_langgraph/main.py --question "Status of SR1001"
python -m streamlit run hour_06_streamlit/app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). Keep the terminal
open; Ctrl+C stops the server. Uploaded files are temporary; download the JSON before
closing if you want to retain a result. There is no database or durable conversation memory.

## Six-hour learning map

| Hour | Topic from supplied TOC | Banking increment | Artifact |
|---|---|---|---|
| 1 | LLM calls and function calling | Look up SR1001 using a tool | Tool observation and response |
| 2 | RAG, local embeddings, Chroma | Ground answers in bank policies | Cited answer or abstention |
| 3 | CrewAI sequential crew | Research, draft, review a service guide | Reviewed guide and task outputs |
| 4 | AG2 Classic conversations | Buddy/customer; planner/writer/critic | Bounded conversation transcript |
| 5 | LangGraph state and routing | Supervisor chooses policy/request worker | Final state with node path |
| 6 | Framework comparison and capstone | Assemble a local Streamlit assistant | Interactive app and JSON download |

Hours 1–5 use 12 minutes theory + 24 minutes first lab + 24 minutes extension.
Hour 6 uses 12 minutes comparison + 36 minutes build + 12 minutes demo. Total: 72 theory,
288 practical minutes. The TOC's onboarding story is intentionally replaced with your
banking use case. This package uses local Python scripts instead of Colab notebooks to
support the final local Streamlit app. LangSmith is an optional extension, absent from
the supplied TOC. Streamlit is your requested capstone addition.

## Project files and directories

| Path | Purpose |
|---|---|
| `.env.example` | Safe configuration template; copy to `.env` and fill locally |
| `.gitignore` | Excludes secrets, virtual environments, generated caches |
| `requirements.txt` | Main app, API, PDF and semantic retrieval dependencies |
| `requirements-crewai.txt` | Extra CrewAI lab dependency, use isolated environment |
| `requirements-ag2.txt` | AG2 Classic 0.14.1 lab dependency; imports as `autogen` |
| `shared/` | Common input contracts, API client, retrieval and graph |
| `data/` | Synthetic CSVs and a text PDF fixture |
| `hour_01_…` through `hour_06_…` | Six separately documented increments |
| `tests/` | Offline regression checks |
| `TRAINER_GUIDE.md` | Timing, checkpoints, exercises, evaluation, rescue steps |
| `SOURCES.md` | Official framework references and curriculum provenance |
| `VALIDATION.md` | Actual test results and unverified integrations |

Each subdirectory has its own README explaining all its source files, inputs and outputs.
Framework dependencies can conflict; install CrewAI and AG2 in separate virtual
environments, following the hour READMEs. These are compatibility requirements, not a
fully resolved lockfile. Rehearse with your provider, then save `pip freeze` for your cohort.

## Live API mode

Edit `.env`: set `DEMO_MODE=false`, your `OPENAI_API_KEY`, `OPENAI_MODEL`, and
`OPENAI_BASE_URL`. The template defaults to OpenAI. An OpenAI-compatible endpoint must
support chat completions, and Hour 1 also requires function calling. Provider compatibility
and model availability must be checked before class. Use your own account's model ID.
Never paste keys into Python, screenshots, chat, or uploaded data. Restart scripts/Streamlit
after editing `.env`. Existing shell variables override the file.

Hour 1 makes two bounded API requests; RAG makes one completion per answered policy
question. CrewAI/AG2 may make multiple calls. Iteration/round limits reduce runaway work,
but they do not impose a monetary budget: check provider usage and quotas during rehearsal.
Semantic retrieval downloads a local embedding model once; embeddings do not use the LLM key.

## Inputs and outputs

Policies accept CSV or text PDF. Service status accepts CSV only. These are separate
input contracts: PDFs supply knowledge, not structured request records. See `data/README.md`.
CLI prints results to the terminal; redirect with `> result.json` if desired (live CrewAI/AG2
also print framework logs, so their redirected output is not a pure JSON document).
The app shows answer, source IDs, review note and node trace and offers a JSON download.
A source reference means retrieval provenance; it does not prove every generated claim.

The graph uses a transparent keyword supervisor for beginners. A request ID takes
priority over policy words. Compound questions are not decomposed: ask one task at a time.
Policy questions use retrieved evidence; unsupported/general questions get branch follow-up.
The reviewer checks presence of sources; it is not a compliance or factual verification agent.

## Optional LangSmith

Set `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, and `LANGSMITH_PROJECT` in `.env`,
then restart. Run Hour 5 and inspect the graph and decorated supervisor/worker traces in
LangSmith. Tracing is off by default and can send question, evidence and output to LangSmith.
Use synthetic data. This extension traces the LangGraph path, not every CrewAI/AG2 call.

## Troubleshooting

- `ModuleNotFoundError`: activate the correct venv and install that hour's requirements.
- `401/403`: check the local key/provider permissions; never print the key.
- `429`: wait for provider reset, reduce calls, or return to demo mode.
- PDF has no text: export as text PDF or perform OCR externally; this app has no OCR.
- First semantic run is slow: allow model download; use lexical mode when offline.
- CSV error: use UTF-8, exact headers and nonblank required cells; quote commas in content.
- Wrong or unrelated retrieval: inspect source excerpts; tune chunks/threshold on held-out
  questions. Lexical overlap and semantic distance are classroom heuristics.
- Port occupied: add `--server.port 8502` to the Streamlit command.

## Checks

```bash
python -m unittest discover -s tests -v
```

Do not use this unauthenticated local workshop app with real banking data. Production
would require authenticated record access, authorization, privacy controls and reviewed
bank policies. Uploaded policy content is treated as untrusted evidence; prompt instructions
reduce but cannot eliminate prompt injection or hallucination in live mode.
