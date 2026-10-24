# Inputs: fictional bank policies and service requests

All records and bank rules are invented; amounts, rates and eligibility are deliberately absent.

| File | Content / role | Expected output |
|---|---|---|
| `policies.csv` | Four policy rows: account opening, lost card, service status, address update | Cited excerpts such as `policies.csv:P001` |
| `policies.pdf` | One-page extractable text fixture covering account opening/lost card | Citations such as `policies.pdf:page 1` |
| `requests.csv` | Two synthetic service request records | SR1001 Pending; SR1002 Resolved |
| `README.md` | Input preparation and output guidance | Learner instructions |

## Prepare a CSV

Use Excel or a text editor and save as **CSV UTF-8**. Keep exact headers:

Policies: `policy_id,topic,content` — all three required; unique policy_id.
Requests: `request_id,service,status,next_action` — all four required; unique request_id.
Use IDs in the SR followed by digits format (e.g. SR1003) for graph routing.
Do not include blank required cells. Surround content containing commas with double quotes.
Do not reuse a policy file as a request file. Extra columns are ignored by retrieval, but
request lookup returns the whole matched row: use only the documented columns.

## Prepare a PDF

Export fictional policies from a text document as PDF. Select and copy a sentence to confirm
it contains text. Scanned images need OCR first. No password protection. At most 50 pages
and 5 MB. PDF layout/table extraction may lose reading order: inspect excerpts before trusting them.
The sample PDF is a shorter alternative fixture, not an exact copy of all CSV policies.

## Run and inspect

From project root:

```bash
python hour_02_rag/main.py --policy data/policies.pdf --question "What documents for account opening?"
python hour_01_llm_and_tools/main.py --requests data/requests.csv --request-id SR1002
```

In Streamlit, upload one policy file and optionally a request CSV. If omitted, each defaults
to the corresponding sample CSV. Outputs include only source filenames/row IDs or page
numbers, never absolute file paths. JSON export contains the final graph state.
