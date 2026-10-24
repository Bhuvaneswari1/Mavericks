# Hour 1 — LLM calls and a first tool agent

## Banking use case

A customer asks for service request SR1001. The assistant must call a lookup tool instead of inventing a status.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Know Python dictionaries, functions and basic terminal commands.


User request
    ↓
First API call: model receives the request and tool schema
    ↓
Model returns a tool call with request_id
    ↓
Python validates the tool name and request ID
    ↓
Python executes lookup() against the CSV
    ↓
Python sends the observation back as a tool message
    ↓
Second API call: model generates the final response

## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | Agent = model + tools + bounded control loop. A system prompt sets behavior; a tool schema describes allowed arguments. Contrast a single model answer with a verified lookup. |
| 12–36 | Run demo, inspect tool_call and observation. Read the schema and lookup function. Switch to live mode and inspect the model tool_calls response. |
| 36–60 | Observe tool result → final completion. Change SR1001 to SR1002 then SR9999. Compare concise and detailed system prompts; try a few-shot example with a fictional request. |

Run `python hour_01_llm_and_tools/first_call.py` before the tool lab. Change the system prompt, remove the two examples, and compare outputs in live mode.

## Files explained

- `first_call.py`: a first completion with a system prompt and two few-shot examples; input is the embedded example prompt and output is a terminal response.
- main.py: CLI parser, offline simulation, JSON function schema, first API call, allowlisted tool execution, tool-result message, second API call.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** `--request-id` plus `--requests` CSV; API settings only in live mode.

**Workflow:** Run demo, inspect tool_call and observation. Read the schema and lookup function. Switch to live mode and inspect the model tool_calls response.

**Output:** Offline: a simulated call and Pending observation. Live: SDK tool call, validated local observation, final natural-language answer.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python hour_01_llm_and_tools/main.py --request-id SR1001
```

For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Checkpoint and exercise

The output contains Pending for SR1001 and an explicit error for SR9999. Explain why a tool result is safer than guessing.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?
