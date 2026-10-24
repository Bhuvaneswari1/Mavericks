# Hour 2 — RAG: give the agent bank knowledge

## Banking use case

A customer asks which documents are needed for account opening. Answer using the uploaded fictional policy with source IDs.

## Outcomes and prerequisites

Read root README setup first. Use the same synthetic bank inputs throughout. Complete the previous hour and explain its output before continuing.

p.add_argument('--policy', default=str(ROOT/'data/policies.csv'))
p.add_argument('--question', default='What documents for account opening?')
p.add_argument('--semantic', action='store_true')

documents(path) → chunks(documents) → self.items

chunks() splits documents into smaller pieces of up to 700 characters, with 100 characters of overlap. This policy is short, so it remains one chunk.
Because a.semantic is False, the program skips embedding creation and Chroma indexing.

4. Retrieval finds the relevant policy
In the default keyword mode, search() compares meaningful words in the question with words in each policy chunk.
Question: What documents for account opening?
                              ↓
Relevant overlap: account, opening
                              ↓
Matching policy: P001
The implementation ranks chunks by shared words and returns up to three chunks with at least two matching tokens.
P001 qualifies, so its text and source ID become the retrieved evidence.



## 60-minute workflow

| Time | Learner activity |
|---|---|
| 00–12 | RAG = retrieval augmented generation. Explain chunk, embedding, vector store and citation. Grounding makes evidence inspectable; it does not guarantee correctness. |
| 12–36 | Run CSV lexical baseline. Inspect chunks and source IDs. Run again with --semantic to build the local MiniLM + Chroma index. |
| 36–60 | Use the PDF fixture, compare returned passages, then ask an unsupported lunar-loan question. Call Knowledge.search as the reusable knowledge tool used in Hour 3. |

## Files explained

- main.py: CLI wrapper that constructs Knowledge, retrieves evidence and calls answer. Shared core.py owns loading, chunking, embedding/indexing and answering.
- `README.md`: this lesson's use case, timed workflow, input/output contract and run instructions.
- Shared source files are documented in `shared/README.md`; sample files in `data/README.md`.

## Input → workflow → output

**Input:** `--policy` CSV or text PDF; `--question`; optional `--semantic`.

**Workflow:** Run CSV lexical baseline. Inspect chunks and source IDs. Run again with --semantic to build the local MiniLM + Chroma index.

**Output:** Answer/excerpts plus sources, or Not found. In live mode retrieval evidence grounds one model completion.

## Run

Activate the appropriate environment. Run from project root, not this hourly directory.

```bash
python hour_02_rag/main.py --question "What documents for account opening?"
```

For the full TOC embedding pipeline, append `--semantic` to the command. This downloads the MiniLM model on first use; internet is required once. The default lexical baseline is an offline fallback.

For CLI labs (Hours 2–5), add `--policy data/policies.pdf` to the relevant CLI command to try PDF input.
Hour 1 uses structured request CSV only; Hour 6 accepts uploads in its sidebar.
The hourly files are Python scripts, not notebooks. Root `.env` is loaded automatically.

## Checkpoint and exercise

Find P001 for account opening; inspect evidence before accepting the answer. Unsupported questions should abstain; investigate if semantic mode retrieves unrelated passages.

Copy → run → inspect → modify. Change one input at a time, predict the result, and compare.
If stuck, return to DEMO_MODE=true, rerun the sample command and compare with the output
described above. For API errors inspect provider quotas and credentials locally. For input
errors follow `data/README.md`; do not edit validation to hide invalid data.

## Explain it back

1. Which file/function reads the input in this hour?
2. Which steps use Python rules, retrieval or a model?
3. What evidence supports the output, and what would cause you to reject it?

{
  "answer": "DEMO: retrieved excerpts (no LLM reasoning)\n[policies.csv:P001] account opening: ...",
  "sources": [
    "policies.csv:P001"
  ]
}

| Output | Explanation |
|---|---|
| `DEMO: retrieved excerpts` | The response contains retrieved text rather than an LLM-generated explanation |
| `[policies.csv:P001]` | The following evidence came from policy `P001` in `policies.csv` |
| `identity proof and address proof` | The policy information relevant to the question |
| `Staff verify the documents` | A condition recorded in the source policy |
| `No approval is promised` | A limitation recorded in the source policy |
| `"sources": ["policies.csv:P001"]` | A separate list of the retrieved source references |

Complete workflow for your command

Default question + policies.csv
              ↓
Read and validate policy CSV
              ↓
Convert rows into documents with source IDs
              ↓
Split documents into chunks
              ↓
Compare question words with chunk words
              ↓
Retrieve matching policy P001
              ↓
Demo mode: return the excerpt and its source
              ↓
Print formatted JSON