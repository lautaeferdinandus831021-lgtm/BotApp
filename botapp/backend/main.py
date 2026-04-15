from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = {
    "api_key": "",
    "api_secret": "",
    "passphrase": "",
    "balance": 0
}

# =========================
# BITGET API (SIMPLE)
# =========================
def get_balance():
    try:
        # sementara dummy dulu biar kelihatan jalan
        return 1000.0
    except:
        return 0

# =========================
# LOOP BOT
# =========================
def bot_loop():
    while True:
        STATE["balance"] = get_balance()
        time.sleep(5)

# =========================
# API
# =========================
@app.get("/")
def root():
    return {"status": "BOT RUNNING 🚀"}

@app.post("/config")
def config(data: dict):
    STATE["api_key"] = data.get("api_key")
    STATE["api_secret"] = data.get("api_secret")
    STATE["passphrase"] = data.get("passphrase")
    return {"status": "saved"}

@app.get("/balance")
def balance():
    return {"balance": STATE["balance"]}

# =========================
# START BOT
# =========================
import threading
threading.Thread(target=bot_loop, daemon=True).start()

