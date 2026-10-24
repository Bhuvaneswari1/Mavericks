# Hour 5 — Graph orchestration with LangGraph

## Banking use case

Route a customer question to policy knowledge or a request-status worker, then attach a review note.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Complete the previous hour and explain its output before continuing.

## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | State is the shared dictionary; nodes do work; edges select the next node. Compare a graph supervisor with a sequential crew and conversation manager. |
| 12–36 | Inspect shared/graph.py. Trace supervisor → policy worker → reviewer. Run account opening, SR1001 and hello to exercise all routes. |
| 36–60 | Turn on optional LangSmith with synthetic inputs. Inspect state updates and sources. Add a new policy row and confirm retrieval sees it on the next run. |

## Files explained

- main.py: CLI parser and compiled graph invocation. shared/graph.py: TypedDict state, supervisor, policy/request/general workers, conditional edges, reviewer and END.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** Policy path, request CSV path and question; optional --semantic. LangGraph runs even in demo mode.

**Workflow:** Supervisor chooses a worker, worker reads validated evidence, reviewer attaches provenance note, UI renders state.

**Output:** JSON state: route=request, Pending response, source reference, node path and review note.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python hour_05_langgraph/main.py --question "Status of SR1001"
```

For the full TOC embedding pipeline, append `--semantic` to the command. This downloads the MiniLM model on first use; internet is required once. The default lexical baseline is an offline fallback.

For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Checkpoint and exercise

All routes terminate; SR9999 yields not found, unknown policy questions do not invent fees. The supervisor is rule based, not an LLM supervisor.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?

1. Your command supplies the inputs
python hour_05_langgraph/main.py --question "Status of SR1001"
The argument parser produces:
Argument	Value
a.question	"Status of SR1001"
a.policy	Default data/policies.csv path
a.requests	Default data/requests.csv path
a.semantic	False, because --semantic was omitted


The policy path is still supplied when building the graph, although this question follows the request-status route.
2. build() creates the graph
build(Path(a.policy), Path(a.requests), a.semantic)
The build() function in shared/graph.py defines the nodes, connects them with edges, and returns a compiled graph.
The application’s architecture is:
                         START
                           ↓
                      Supervisor
                           ↓
                   Select one route
                 ┌─────────┼─────────┐
                 ↓         ↓         ↓
              Policy    Request    General
              worker    worker     response
                 └─────────┼─────────┘
                           ↓
                        Reviewer
                           ↓
                          END
Component	Responsibility
Supervisor	Selects a route using Python rules
Policy worker	Retrieves policy evidence and prepares an answer
Request worker	Looks up a synthetic request in the CSV
General node	Explains supported topics and suggests branch follow-up
Reviewer	Adds a note based on whether source references exist


Only one of the three branches runs for each question.
3. invoke() starts execution with an initial state
.invoke(
    {'question': a.question},
    config={'recursion_limit': 10}
)
The initial state is:
{
  "question": "Status of SR1001"
}
State is the shared dictionary that travels through the graph. Each node reads what it needs and returns updates.
recursion_limit=10 limits graph execution steps to guard against runaway execution. It is not a limit of ten API calls. This graph has no looping edges and normally terminates directly.
4. The supervisor chooses the request route
The supervisor calls:
route_question(s['question'])
The routing function first checks for an ID matching this pattern:
r'\bSR\d+\b'
That means SR followed by one or more digits, such as SR1001.
Your question contains SR1001, so the supervisor returns:
{
    'route': 'request',
    'steps': ['supervisor']
}
The state now contains:
{
  "question": "Status of SR1001",
  "route": "request",
  "steps": ["supervisor"]
}
A conditional edge uses "route": "request" to select the request worker. The supervisor here is rule-based; an LLM does not make this decision.
5. The request worker reads the CSV
The worker extracts and normalizes the request ID:
rid = re.search(
    r'\bSR\d+\b',
    s['question'],
    re.I
).group().upper()
For your question:
rid = "SR1001"
It then calls:
row = lookup(rid, requests)
The matching CSV row supplies:
{
  "request_id": "SR1001",
  "service": "Address update",
  "status": "Pending",
  "next_action": "Visit the demo branch with address proof"
}
The worker formats that data into the answer and updates the state:
{
  "answer": "SR1001: Address update — Pending. Next action: Visit the demo branch with address proof",
  "sources": ["requests.csv:SR1001"],
  "steps": ["supervisor", "request_worker"]
}
The answer is built using a Python formatted string. The CSV supplies the facts; no model generates this request-status answer.
6. The reviewer attaches a provenance note
The reviewer checks:
s.get('sources')
Because the request worker supplied a source reference, it adds:
{
  "review": "Source references attached; human verification required.",
  "steps": ["supervisor", "request_worker", "reviewer"]
}
This reviewer checks the presence of source references. It does not independently verify that the CSV is correct or perform an LLM-based review.
The graph then reaches END.
7. Connecting every output field to the workflow
Output field	Created by	Meaning
question	Initial input	Your original question
route: "request"	Supervisor	Selects the request-status branch
answer	Request worker	Formats the matched CSV row
sources	Request worker	Identifies the CSV and request record
steps	Each executed node	Records the path through the graph
review	Reviewer	Notes that references exist and human verification is needed


Your actual execution path is therefore:
"Status of SR1001"
        ↓
Supervisor detects SR1001
        ↓
route = "request"
        ↓
Request worker → lookup("SR1001", requests.csv)
        ↓
Address update / Pending / branch follow-up
        ↓
Reviewer attaches source-reference note
        ↓
END → final state printed as JSON
In the printed answer:
\u2014
is JSON’s escaped representation of the em dash —. To display that character directly, use:
json.dumps(result, indent=2, ensure_ascii=False)
Why use LangGraph here?
For one CSV lookup, a regular Python function would be sufficient. LangGraph becomes useful when the application has multiple routes and you want to make their execution explicit:
- Different questions reach different workers.
- Nodes share a defined state.
- Every branch passes through a common review stage.
- You can inspect the route, intermediate updates, and final result.
Here, LangGraph provides the workflow structure. Your Python functions provide the routing rules, data lookup, and response formatting.

Request-status questions → request route
python hour_05_langgraph/main.py --question "Status of SR1001"
Expected: Address update — Pending, with branch follow-up.
python hour_05_langgraph/main.py --question "What is the status of SR1002?"
Expected: Debit card replacement — Resolved, with collection instructions.
python hour_05_langgraph/main.py --question "Check request SR9999"
Expected: Request not found, with no source reference.
The workflow for these questions is:
supervisor → request_worker → reviewer
Bank-policy questions → policy route
python hour_05_langgraph/main.py --question "What documents are required for account opening?"
Expected evidence: Identity proof and address proof — policies.csv:P001.
python hour_05_langgraph/main.py --question "What should I do if I lose my card?"
Expected evidence: Use the official app or contact the branch to request blocking — policies.csv:P002.
python hour_05_langgraph/main.py --question "What documents are required for an address update?"
Expected evidence: Submit address proof at a branch for staff review — policies.csv:P004.
python hour_05_langgraph/main.py --question "What is the lunar account opening fee?"
Use this to inspect unsupported-question handling. Keyword retrieval may still return the account-opening policy because words overlap. Check that the evidence contains no fee information; live answers should acknowledge that limitation.

