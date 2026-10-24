# Validation report

Validation performed 21 October 2026.

## Passed

- Seven unittest regressions: CSV schema rejection, duplicate policy IDs, known/unknown
  request lookup, supported/unsupported lexical retrieval and route classification.
- Python compilation of all application source files.
- CLI demo runs for Hour 1, Hour 3 and Hour 4 with explicitly labeled simulation outputs.
- Real LangGraph execution for policy, known request, unknown request and general routes;
  every path reached the reviewer and terminated.
- pypdf extraction of the supplied sample PDF, including account-opening text.
- Streamlit AppTest: initial render, policy response, request response, empty-input rejection,
  and removal of a prior result after empty input.

Runtime smoke checks used Python 3.12, LangGraph 1.2.16, LangSmith 0.14.11,
Streamlit 1.66.0, pypdf 6.21.1 and python-dotenv 1.2.4 in an isolated environment.
Python 3.11 is recommended for the workshop framework environments; it was not available
for a separate runtime rehearsal here. Framework source/API references appear in SOURCES.md.

## Not verified in this delivery

- Paid/live LLM requests, provider-specific tool calling or generated-answer correctness.
- Real CrewAI and AG2 execution; their offline simulations were exercised only.
- Full semantic dependency installation, MiniLM download, Chroma embedding retrieval quality.
- LangSmith cloud trace submission (no API credentials supplied).
- File upload/download browser interactions, OCR, visual browser screenshot review.
- A fully resolved installation of all requirements together; separate framework environments
  are provided to reduce conflicts. Freeze exact dependencies after trainer rehearsal.

AppTest exercises Streamlit programmatically; it does not replace visual/browser QA.
These limitations are deliberate and should guide the pre-class rehearsal in TRAINER_GUIDE.md.
