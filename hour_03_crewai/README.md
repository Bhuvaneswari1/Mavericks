# Hour 3 — First multi-agent crew with CrewAI

## Banking use case

Produce a reviewed service guide answering the same customer question: researcher gathers bank policy, writer drafts, reviewer checks.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Complete the previous hour and explain its output before continuing.

## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | CrewAI Agent = role, Task = assignment, Crew = execution team. Sequential tasks pass context. More agents increase calls and may repeat errors. |
| 12–36 | Read the three roles. Run offline role simulation. Install the isolated CrewAI lab environment, enable live mode, and inspect research and draft outputs. |
| 36–60 | Run the three-task crew. Compare writer output with reviewer output. Remove a source in the draft and discuss whether the reviewer catches it; never assume it will. |

## Files explained

- main.py: closure-based @tool policy_search, three Agent objects, Tasks with explicit context, sequential Crew and kickoff.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** Policy CSV/PDF, question, live provider configuration for the actual crew.

**Workflow:** Read the three roles. Run offline role simulation. Install the isolated CrewAI lab environment, enable live mode, and inspect research and draft outputs.

**Output:** Offline labeled simulation, or real CrewAI reviewed guide and per-task outputs plus execution logs.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python hour_03_crewai/main.py --question "What documents for account opening?"
```

For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Isolated live lab setup

Use a new terminal at the project root (Python 3.11).

```bash
python -m venv .venv-crew
# macOS / Linux
source .venv-crew/bin/activate
# Windows PowerShell: .venv-crew\Scripts\Activate.ps1
python -m pip install -r requirements-crewai.txt
```

Edit the same root `.env`, set DEMO_MODE=false and fill your provider settings.
The offline simulation needs no framework installation but does not exercise its API.
Return to the main `.venv` for Hours 5–6.

## Checkpoint and exercise

Research has policy IDs; writer preserves them; reviewer removes unsupported promises. Check each claim against the source.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?

python hour_03_crewai/main.py \
  --question "Explain the account-opening process as a short customer guide."

{
  "mode": "offline role simulation; CrewAI is not executed",
  "researcher": {
    "answer": "DEMO: retrieved excerpts (no LLM reasoning)\n[policies.csv:P001] account opening: Fictional Demo Bank: open a savings account by submitting identity proof and address proof at a branch. Staff verify the documents. No approval is promised.",
    "sources": [
      "policies.csv:P001"
    ]
  },
  "writer": "DEMO: retrieved excerpts (no LLM reasoning)\n[policies.csv:P001] account opening: Fictional Demo Bank: open a savings account by submitting identity proof and address proof at a branch. Staff verify the documents. No approval is promised.",
  "reviewer": "Check citations and do not promise approvals. Human review still required."
}

without crewAI libraries

Question + policy CSV
          ↓
    Knowledge(policy)
          ↓
answer(question, knowledge)
          ↓
Retrieve matching policy P001
          ↓
Build a simulated three-role result
          ↓
Print JSON

To run the actual CrewAI workflow:
1. Activate the CrewAI environment and install its dependencies:

python -m pip install -r requirements-crewai.txt

python hour_03_crewai/main.py \
  --question "Explain the account-opening process as a short customer guide."

The live CrewAI architecture
When demo() returns False, execution continues into the CrewAI section:

                       Configured LLM
                       ↙     ↓     ↘
                 Researcher Writer Reviewer
                      ↓       ↑       ↑
                policy_search │       │
                      ↓       │       │
                Knowledge     │       │
                      ↓       │       │
                Policy facts ─┘       │
                      └───────────────┘

Sequential execution:
Research task → Draft task → Review task → Final result

CrewAI handles running the tasks in order and passing their outputs to the next agent. You configure that here:
process=Process.sequential

Why run it in this workshop?
Demo mode only retrieves text, copies it into the writer field, and prints a fixed review reminder. Running CrewAI lets you observe actual model-generated research, drafting, and review—and inspect whether each step helps.
Do you need CrewAI for every banking question? No.
For a simple question such as “Which documents are required?”, Hour 2’s retrieval plus one LLM call may be sufficient. CrewAI becomes useful when the task benefits from several distinct stages, such as preparing a detailed service guide from multiple policies.


Install the workshop’s AG2 dependencies:
python -m pip install -r requirements-ag2.txt
The project uses AG2 Classic, imported in your code as:
from autogen import ConversableAgent, GroupChat, GroupChatManager
2. Update your root .env
If .env does not exist, copy .env.example first.
Configure:
DEMO_MODE=false
OPENAI_API_KEY=your_actual_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=your_available_model_id
Replace the key and model placeholders with your actual values. Live execution sends requests to the configured provider and may incur charges.
If the output still says offline transcript simulation, check whether your terminal has DEMO_MODE=true set. Existing environment variables override .env. Clear that override:
macOS / Linux
unset DEMO_MODE
Windows PowerShell
Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
3. Run the two-agent conversation
python hour_04_ag2/main.py \
  --question "What documents for account opening?"
Without --group, your code runs:
Customer → Buddy → DONE!
An illustrative final output is:
{
  "mode": "live AG2 two-agent",
  "messages": [
    {
      "role": "assistant",
      "content": "What documents for account opening?"
    },
    {
      "role": "user",
      "content": "Submit identity proof and address proof at a branch. Staff verify the documents; approval is not promised. [policies.csv:P001] DONE!"
    }
  ]
}
The precise fields, role labels, and wording can differ. chat_history role labels reflect the conversation’s perspective; use message content and any speaker names to interpret the transcript.
4. Run the managed group conversation
python hour_04_ag2/main.py --group \
  --question "What documents for account opening?"
This runs:
Customer → Planner → Writer → Critic
                 GroupChatManager coordinates turns
An illustrative final output is:
{
  "mode": "live AG2 managed group",
  "messages": [
    {
      "name": "Customer",
      "content": "What documents for account opening?"
    },
    {
      "name": "Planner",
      "content": "Explain the required documents and staff verification using policy P001."
    },
    {
      "name": "Writer",
      "content": "Prepare identity proof and address proof, then submit them at a branch. Staff verify them. [policies.csv:P001]"
    },
    {
      "name": "Critic",
      "content": "The guide matches policy P001. Clarify that submitting documents does not guarantee approval. [policies.csv:P001] DONE!"
    }
  ]
}
Actual messages may include fields such as role, and agents may respond differently. Framework logs can appear before the final JSON.
Differences between the three modes
Feature	Offline demo	Live two-agent	Live group
Configuration	DEMO_MODE=true	DEMO_MODE=false	DEMO_MODE=false
Command flag	Either	Without --group	With --group
AG2 executes	No	Yes	Yes
LLM calls	None	Buddy generates responses	Planner, Writer, and Critic generate responses
Conversation	Fixed Customer/Buddy/Critic messages	Customer ↔ Buddy	Managed group conversation
Evidence	Retrieved policy excerpts	Same excerpts supplied to Buddy	Same excerpts supplied to group agents
Drafting and review	Scripted display only	One answering agent	Separate planning, drafting, and review
Termination	Python returns immediately	DONE! or configured limits	DONE! or configured limits
Output mode	offline transcript simulation; AG2 is not executed	live AG2 two-agent	live AG2 managed group


In all three modes, your Python code retrieves policy evidence before the conversation starts. Switching on AG2 changes how agents discuss and compose the answer; it does not change this example into agent-controlled retrieval.