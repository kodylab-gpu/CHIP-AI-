import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message] = Field(default_factory=list, max_length=20)
    mode: str = 'chat'

PROMPTS = {
    'chat': 'You are Chip AI, a helpful multilingual assistant.',
    'code': 'You are Chip AI, a careful programming assistant.',
    'research': 'You are Chip AI. Analyze carefully. You cannot browse live websites; do not claim to have searched online.',
    'translate': 'You are Chip AI, a precise translator.',
    'tutor': 'You are Chip AI, a patient educational tutor.'
}

@app.get('/api/health')
async def health():
    return {'status': 'ok', 'configured': bool(os.getenv('AI_API_KEY') and os.getenv('AI_MODEL'))}

@app.post('/api/chat')
async def chat(payload: ChatRequest):
    key = os.getenv('AI_API_KEY')
    model = os.getenv('AI_MODEL')
    base = os.getenv('AI_BASE_URL', 'https://openrouter.ai/api/v1').rstrip('/')
    if not key or not model:
        raise HTTPException(status_code=503, detail='AI_API_KEY va AI_MODEL Vercel sozlamalarida kiritilmagan.')
    if not base.startswith('https://'):
        raise HTTPException(status_code=500, detail='AI_BASE_URL HTTPS bo‘lishi kerak.')
    messages = [{'role':'system','content':PROMPTS.get(payload.mode, PROMPTS['chat']) + ' Respond in the user language.'}]
    messages += [{'role':m.role, 'content':m.content[:10000]} for m in payload.messages if m.role in ('user','assistant')]
    if not any(m['role']=='user' for m in messages):
        raise HTTPException(status_code=400, detail='Xabar kiriting.')
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            res = await client.post(base + '/chat/completions', headers={'Authorization':'Bearer '+key}, json={'model':model, 'messages':messages})
        if res.status_code >= 400:
            raise HTTPException(status_code=502, detail=f'AI provayder xatosi ({res.status_code}). Model, kalit va limitni tekshiring.')
        reply = res.json()['choices'][0]['message']['content']
        return {'reply': str(reply)}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail='AI javobi kechikdi.')
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail='AI provayderga ulanishda xatolik.')
    except (KeyError, IndexError, TypeError, ValueError):
        raise HTTPException(status_code=502, detail='AI provayderidan noto‘g‘ri javob keldi.')
