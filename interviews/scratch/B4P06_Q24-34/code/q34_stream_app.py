# Q34: SSE token streaming from a fake generator (no real LLM).
import asyncio, json, time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(); stats = {"started": 0, "completed": 0, "cancelled": 0}
class Chat(BaseModel):
    prompt: str
    max_tokens: int = Field(default=20, ge=1, le=200)

async def fake_llm(prompt, n, first_delay=0.30, per_token=0.05):
    await asyncio.sleep(first_delay)                 # "prefill": time to first token
    for i in range(n):
        yield f"tok{i} "; await asyncio.sleep(per_token)   # "decode": one token per step

@app.post("/v1/chat/stream")
async def chat(body: Chat, request: Request):
    async def sse():
        stats["started"] += 1
        try:
            async for tok in fake_llm(body.prompt, body.max_tokens):
                if await request.is_disconnected(): stats["cancelled"] += 1; return   # stop paying for tokens nobody reads
                yield f"data: {json.dumps({'token': tok})}\n\n"
            yield "data: [DONE]\n\n"; stats["completed"] += 1
        except asyncio.CancelledError:
            stats["cancelled"] += 1; raise
    return StreamingResponse(sse(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.get("/stats")
async def get_stats(): return stats
