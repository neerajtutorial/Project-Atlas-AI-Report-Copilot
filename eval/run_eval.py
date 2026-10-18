"""Small smoke/evaluation runner. Results are observations, not a claim of passing all rubric tests."""
import json, os, time, requests
BASE=os.getenv('ATLAS_URL','http://localhost:8000'); KEY=os.getenv('API_KEY','local-dev-key-change-me')
with open(os.path.join(os.path.dirname(__file__),'questions.json'),encoding='utf-8') as f: cases=json.load(f)
rows=[]
for c in cases:
    start=time.time()
    try:
        r=requests.post(BASE+'/chat',headers={'X-API-Key':KEY},json={'client_id':c['client_id'],'question':c['question']},timeout=30)
        data=r.json(); ok=r.status_code==200
        rows.append({'id':c['id'],'status':r.status_code,'latency_s':round(time.time()-start,2),'confidence':data.get('confidence'),'escalated':data.get('escalated'),'answer':data.get('answer','')[:240],'expected':c['expected'],'manual_review_required':True})
    except Exception as e: rows.append({'id':c['id'],'status':'ERROR','error':str(e),'expected':c['expected'],'manual_review_required':True})
out=os.path.join(os.path.dirname(__file__),'results.json')
with open(out,'w',encoding='utf-8') as f: json.dump(rows,f,indent=2,ensure_ascii=False)
print(f'Wrote {len(rows)} cases to {out}. Manual scoring is required; this runner does not claim correctness automatically.')