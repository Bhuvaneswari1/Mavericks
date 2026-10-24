# Shared building blocks

Use case: keep one authoritative ingestion and lookup implementation across all six hours.
Import this code from hourly entry points; do not run these files directly.

| File | Explanation | Input | Output |
|---|---|---|---|
| `__init__.py` | Marks shared as an importable Python package | None | Package imports |
| `core.py` | Loads root `.env`, validates CSV/PDF, chunks text, retrieves, calls API and looks up requests | File paths, question, optional credentials | Documents, excerpts, answer/source dictionary, request row |
| `graph.py` | Typed state, keyword supervisor, workers, review node, graph builder | Policy/request paths and question state | Compiled LangGraph / final state |
| `README.md` | Explains contracts and reuse | Reader | Understanding |

`documents` reads policy CSV rows or extracts PDF pages with source IDs. `chunks` uses
700-character chunks and 100-character overlap (a chunk is a small piece of a document).
`Knowledge.search` uses lexical token overlap by default. `semantic=True` replaces this
with MiniLM embeddings and an in-memory Chroma index through LangChain integrations.
An embedding is a numeric representation of meaning. Each build creates a fresh index;
there is no persistent Chroma database or stale cross-upload collection.
`answer` either returns retrieved excerpts in demo mode or sends them to a model in live mode.
`lookup` checks request IDs locally; request status never depends on an LLM.

Graph workflow: START → supervisor → policy/request/general → reviewer → END.
State is a dictionary containing question, route, answer, sources, steps and review.
Node updates replace the corresponding keys. Each path terminates without looping;
callers also set recursion_limit=10. LangSmith decorators instrument selected graph nodes.

Input limits: 5 MB per file; CSV 1–5000 rows; PDF 50 pages; policy IDs/request IDs unique
when their corresponding loader is used. PDFs must be unencrypted and contain text.
No authentication is implemented; request IDs are synthetic classroom fixtures.
