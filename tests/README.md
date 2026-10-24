# Offline checks

`test_workshop.py` checks known/unknown request IDs, policy retrieval, unsupported queries,
all supervisor routes, missing CSV headers and duplicate policy IDs. It uses unittest and
synthetic fixtures. Run `python -m unittest discover -s tests -v` from the project root.
Input is fixture files and temporary malformed CSVs; output is test results in the terminal.
These tests do not validate provider compatibility, LLM factual accuracy or paid framework runs.
The graph and UI runtime checks used during delivery are recorded in root VALIDATION.md.
`README.md` documents test scope and execution.
