import asyncio, json, websockets
from fastapi import FastAPI, Request
from state import state
from engine import loop
import uvicorn

app = FastAPI()
clients = set()

@app.get("/")
def root():
    return {"status": "BOT RUNNING 🚀"}

@app.post("/config")
async def config(req: Request):
    data = await req.json()
    state.update(data)
    return {"ok": True}

# ================= WS =================
async def ws_handler(ws):
    clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        clients.remove(ws)

async def ws_server():
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        print("WS RUNNING 8765 🚀")
        await asyncio.Future()

# ================= BROADCAST =================
async def broadcast():
    while True:
        if clients:
            data = json.dumps(state)
            await asyncio.gather(*[c.send(data) for c in clients])
        await asyncio.sleep(0.3)

# ================= MAIN =================
async def start():
    await asyncio.gather(
        ws_server(),
        loop(),
        broadcast()
    )

if __name__ == "__main__":
    loop_async = asyncio.get_event_loop()
    loop_async.create_task(start())

    uvicorn.run(app, host="0.0.0.0", port=8000)
