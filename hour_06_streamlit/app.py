"""Hour 6: a local Streamlit interface using the Hour-5 graph."""
import sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from shared.core import ROOT,demo,documents,records
from shared.graph import build
st.set_page_config(page_title='Banking Service Buddy',page_icon='🏦',layout='wide')
st.title('🏦 Banking Service Buddy')
st.caption('Fictional bank • synthetic records • educational use')
st.info('Offline demo: excerpts only; no LLM calls.' if demo() else 'Live mode: policy excerpts and your question are sent to your configured API provider.')
with st.sidebar:
    st.header('Inputs')
    st.write('Policies: CSV (policy_id, topic, content) or text PDF. Requests: CSV (request_id, service, status, next_action). Maximum 5 MB each.')
    policy=st.file_uploader('Policy file',type=['csv','pdf'])
    requests=st.file_uploader('Synthetic service requests',type=['csv'])
    semantic=st.checkbox('Use local embeddings + Chroma',help='First use downloads the HuggingFace model. Requires internet and extra memory.')
    st.warning('Use fictional data only. Never upload account numbers, PINs or OTPs. Optional LangSmith tracing also transmits run data when enabled in .env.')
question=st.text_input('Question',value='What documents for account opening?',max_chars=1000)
st.caption('Try: How do I handle a lost card? • Status of SR1001 • What is the lunar loan fee?')
if st.button('Run Banking Buddy',type='primary'):
    if not question.strip():
        st.session_state.pop('result',None)
        st.error('Enter a question.')
    else:
        try:
            with st.spinner('Running supervisor and workers…'),tempfile.TemporaryDirectory() as temp:
                policy_path=ROOT/'data/policies.csv'; request_path=ROOT/'data/requests.csv'
                for upload,stem in [(policy,'policies'),(requests,'requests')]:
                    if upload is not None:
                        if upload.size>5_000_000: raise ValueError('Use files smaller than 5 MB.')
                        path=Path(temp)/(stem+Path(upload.name).suffix.lower())
                        path.write_bytes(upload.getvalue())
                        if stem=='policies': policy_path=path
                        else: request_path=path
                # Validate both inputs before selecting a worker.
                documents(policy_path); records(request_path,['request_id','service','status','next_action'])
                result=build(policy_path,request_path,semantic).invoke({'question':question.strip()},config={'recursion_limit':10})
                st.session_state['result']=result
        except Exception as exc:
            st.session_state.pop('result',None)
            st.error(f'Unable to complete ({type(exc).__name__}). Check input schema, .env, installed dependencies, and connectivity. Run the CLI for detailed diagnostics.')
if 'result' in st.session_state:
    result=st.session_state['result']
    st.subheader('Response'); st.write(result['answer'])
    st.write('Sources:',', '.join(result.get('sources',[])) or 'None')
    st.caption(result['review'])
    with st.expander('Workflow state and trace'):
        st.write(' → '.join(result['steps'])); st.json(result)
    st.download_button('Download result JSON',json.dumps(result,indent=2),file_name='banking_result.json',mime='application/json')
