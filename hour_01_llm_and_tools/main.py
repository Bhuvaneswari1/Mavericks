"""Hour 1: inspect the explicit reason → act → observe loop."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.core import demo,lookup,settings,model,ROOT

def run(request_id, requests):
    if demo():
        return {'mode':'offline simulation','tool_call':{'name':'lookup_request','arguments':{'request_id':request_id}},'observation':lookup(request_id,requests)}
    from openai import OpenAI
    client=OpenAI(**settings(),timeout=45,max_retries=1)
    messages=[{'role':'system','content':'Look up the requested service ID using the tool. Do not invent a status.'},
              {'role':'user','content':f'Look up request {request_id}'}]
    tools=[{'type':'function','function':{'name':'lookup_request','description':'Look up a synthetic banking service request',
        'parameters':{'type':'object','properties':{'request_id':{'type':'string'}},'required':['request_id'],'additionalProperties':False}}}]
    first=client.chat.completions.create(model=model(),messages=messages,tools=tools,
        tool_choice={'type':'function','function':{'name':'lookup_request'}},max_tokens=400)
    msg=first.choices[0].message
    messages.append(msg.model_dump(exclude_none=True))
    observations=[]
    for call in msg.tool_calls or []:
        args=json.loads(call.function.arguments)
        if call.function.name!='lookup_request' or args.get('request_id')!=request_id:
            raise ValueError('Unexpected tool or request ID.')
        result=lookup(args['request_id'],requests)
        observations.append(result)
        messages.append({'role':'tool','tool_call_id':call.id,'content':json.dumps(result)})
    if not observations:
        raise ValueError('Provider did not return a tool call.')
    final=client.chat.completions.create(model=model(),messages=messages,max_tokens=400)
    return {'mode':'live','observations':observations,'answer':final.choices[0].message.content}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--request-id',default='SR1001'); p.add_argument('--requests',default=str(ROOT/'data/requests.csv'))
    a=p.parse_args(); print(json.dumps(run(a.request_id,a.requests),indent=2))
