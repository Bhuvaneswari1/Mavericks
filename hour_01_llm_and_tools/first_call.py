"""Start here: plain completion, system prompt, then few-shot prompting."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.core import complete,demo
SYSTEM='You help customers of a fictional demo bank. Do not invent policy. Explain simply; never ask for a PIN or OTP.'
PROMPT='''Examples:
Customer: Can you approve my account?
Assistant: Branch staff must verify your documents. I cannot approve accounts.
Customer: Can I send my OTP?
Assistant: Never share your OTP.
Customer: What can this assistant help with?'''
if __name__=='__main__':
    print('DEMO: I can explain supplied fictional policies and look up synthetic service requests.' if demo() else complete(SYSTEM,PROMPT))
