import asyncio, uvicorn, json, websockets
from fastapi import FastAPI, Request
from state import state
from engine import loop

app=FastAPI()
clients=set()

# ✅ FIX ROOT
@app.get("/")
def root():
    return {"status":"BOT RUNNING 🚀"}

@app.post("/config")
async def config(req:Request):
    data=await req.json()
    state.update(data)
    return {"ok":True}

async def ws_handler(ws):
    clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        clients.remove(ws)

async def broadcast():
    while True:
        if clients:
            data=json.dumps(state)
            await asyncio.gather(*[c.send(data) for c in clients])
        await asyncio.sleep(0.3)

async def main():
    await websockets.serve(ws_handler,"0.0.0.0",8765)
    await asyncio.gather(loop(),broadcast())

if __name__=="__main__":
    asyncio.get_event_loop().create_task(main())
    uvicorn.run(app,host="0.0.0.0",port=8000)
