import time, hmac, hashlib, base64, requests

BASE = "https://api.bitget.com"

def sign(secret, ts, method, path, body=""):
    msg = str(ts)+method+path+body
    return base64.b64encode(
        hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
    ).decode()

def headers(state, method, path, body=""):
    ts=str(int(time.time()*1000))
    return {
        "ACCESS-KEY": state["api_key"],
        "ACCESS-SIGN": sign(state["api_secret"],ts,method,path,body),
        "ACCESS-TIMESTAMP": ts,
        "ACCESS-PASSPHRASE": state["passphrase"],
        "Content-Type":"application/json"
    }

def get_balance(state):
    path="/api/v2/mix/account/accounts"
    h=headers(state,"GET",path)
    r=requests.get(BASE+path,headers=h)
    return r.json()
