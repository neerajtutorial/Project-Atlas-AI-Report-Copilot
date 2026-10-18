import re
from fastapi import Header, HTTPException
from .config import API_KEY

def require_api_key(x_api_key: str | None = Header(default=None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Missing or invalid API key')

INJECTION_TERMS = ('ignore all previous instructions', 'print the full contents', 'reveal system prompt', 'disregard your instructions')
UNSAFE_TERMS = ('list all client emails', 'other clients', 'personal data', 'delete all rows', 'drop table', 'truncate table', 'insert into', 'update clients', 'political party', 'who will win the next general election')
def classify(question: str) -> str:
    q = question.lower()
    if any(x in q for x in UNSAFE_TERMS): return 'unsafe' if any(x in q for x in ('email','delete','drop','truncate','insert','update','other clients','personal data','list all')) else 'out_of_scope'
    if any(x in q for x in ('election','politics','who will win')): return 'out_of_scope'
    if any(x in q for x in ('compare','difference','conflict','which report should i trust')): return 'comparison'
    if any(x in q for x in ('worth in 2030','cagr','project','forecast','calculate','2035')): return 'calculation'
    if any(x in q for x in ('sector has the most reports','how many reports','count of reports')): return 'sql'
    return 'factual_lookup'