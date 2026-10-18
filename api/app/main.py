from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Any
from pathlib import Path
import tempfile
from .security import require_api_key
from .db import query, execute, init_wait
from .agent import answer_question
from .knowledge import ingest_seed, ingest_text

app=FastAPI(title='Project Atlas Report Copilot',version='1.0.0')
class ChatRequest(BaseModel):
    client_id: str = Field(min_length=1,max_length=20)
    question: str = Field(min_length=3,max_length=4000)
class ChatResponse(BaseModel):
    answer: str
    citations: list[dict[str,Any]]
    confidence: float
    conflicts: list[dict[str,Any]]
    derived_values: list[dict[str,Any]]
    escalated: bool
    intent: str
class FeedbackRequest(BaseModel):
    conversation_id: int = Field(gt=0)
    rating: str = Field(pattern='^(up|down)$')
    comment: str | None = Field(default=None,max_length=1000)
@app.on_event('startup')
def startup():
    init_wait()
@app.get('/health')
def health():
    return {'status':'ok','service':'atlas-api'}
@app.post('/chat',response_model=ChatResponse,dependencies=[Depends(require_api_key)])
def chat(req:ChatRequest):
    try: return answer_question(req.client_id,req.question)
    except Exception as e: raise HTTPException(status_code=503,detail='The report service is temporarily unavailable. Please try again or contact an analyst.') from e
@app.post('/ingest',dependencies=[Depends(require_api_key)])
async def ingest(file:UploadFile=File(...),report_id:str=Form(...),title:str=Form(...),sector:str=Form('General')):
    if not file.filename or Path(file.filename).suffix.lower() not in ('.txt','.md','.html','.pdf'):
        raise HTTPException(status_code=400,detail='Only TXT, MD, HTML and PDF files are supported')
    raw=await file.read()
    if len(raw)>12*1024*1024: raise HTTPException(status_code=413,detail='File must be smaller than 12 MB')
    suffix=Path(file.filename).suffix.lower()
    if suffix=='.pdf':
        from pypdf import PdfReader
        import io
        reader=PdfReader(io.BytesIO(raw)); text='\n'.join(f'Page {i+1}: '+(p.extract_text() or '') for i,p in enumerate(reader.pages))
    else: text=raw.decode('utf-8',errors='replace')
    if not text.strip(): raise HTTPException(status_code=400,detail='No extractable text found')
    known=query('SELECT id FROM reports WHERE id=:id',{'id':report_id})
    if not known: raise HTTPException(status_code=404,detail='report_id must exist in reports table before ingesting')
    count=ingest_text(report_id,title,sector,text)
    return {'status':'ingested','report_id':report_id,'chunks_added':count}
@app.get('/escalations',dependencies=[Depends(require_api_key)])
def escalations(status:str='open'):
    if status not in ('open','in_progress','closed','all'): raise HTTPException(status_code=400,detail='Invalid status')
    sql='SELECT id,client_id,question,reason,status,created_at FROM escalations'
    params={}
    if status!='all': sql+=' WHERE status=:s'; params['s']=status
    sql+=' ORDER BY created_at DESC LIMIT 100'
    return [dict(r) for r in query(sql,params)]
@app.post('/feedback',dependencies=[Depends(require_api_key)])
def feedback(req:FeedbackRequest):
    exists=query('SELECT id FROM conversations WHERE id=:id',{'id':req.conversation_id})
    if not exists: raise HTTPException(status_code=404,detail='Conversation not found')
    execute('INSERT INTO feedback (conversation_id,rating,comment) VALUES (:id,:rating,:comment)',{'id':req.conversation_id,'rating':req.rating,'comment':req.comment})
    return {'status':'saved'}
@app.post('/admin/seed-ingest',dependencies=[Depends(require_api_key)])
def seed_ingest():
    try: return ingest_seed()
    except Exception as e: raise HTTPException(status_code=503,detail='Seed ingestion failed; inspect API logs') from e