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

@app.post('/api/chat')
async def chat(payload: ChatRequest):
    key = os.getenv('AI_API_KEY')
    model = os.getenv('AI_MODEL')
    base = os.getenv('AI_BASE_URL', 'https://openrouter.ai/api/v1').rstrip('/')
    if not key or not model:
        raise HTTPException(status_code=503, detail='AI_API_KEY va AI_MODEL Vercel Environment Variables ichida sozlanmagan.')
    if not base.startswith('https://'):
        raise HTTPException(status_code=500, detail='AI_BASE_URL HTTPS bo‘lishi kerak.')
    prompts = {
        'chat': 'You are Chip AI. Be a helpful multilingual assistant.',
        'code': 'You are Chip AI, a careful programming assistant.',
        'research': 'You are Chip AI. Analyze carefully. You do not have live web browsing; do not claim you searched online.',
        'translate': 'You are Chip AI, a precise translator.',
        'tutor': 'You are Chip AI, a patient educational tutor.'
    }
    msgs = [{'role': 'system', 'content': prompts.get(payload.mode, prompts['chat']) + ' Respond in the user’s language.'}]
    msgs.extend({'role': m.role, 'content': m.content[:10000]} for m in payload.messages if m.role in ('user', 'assistant'))
    if not any(m['role'] == 'user' for m in msgs):
        raise HTTPException(status_code=400, detail='Xabar kiritilmagan.')
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            res = await client.post(base + '/chat/completions', headers={'Authorization': 'Bearer ' + key}, json={'model': model, 'messages': msgs})
            if res.status_code >= 400:
                raise HTTPException(status_code=502, detail=f'AI provayder xatosi ({res.status_code}). Model, kalit yoki limitni tekshiring.')
            answer = res.json()['choices'][0]['message']['content']
            return {'reply': str(answer)}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail='AI javobi kechikdi. Qayta urinib ko‘ring.')
    except (httpx.RequestError, KeyError, IndexError, TypeError, ValueError):
        raise HTTPException(status_code=502, detail='AI provayderidan javob olishda xatolik.')
