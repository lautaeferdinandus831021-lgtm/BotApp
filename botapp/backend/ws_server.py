import asyncio, json
from state import state

clients=set()

async def handler(ws):
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
        await asyncio.sleep(0.2)
