from state import state
import time

def is_m5_open():
    return int(time.time()) % 300 < 10

def triple_macd_signal():
    m=state.get("macd",{})
    f=m.get("fast",[])
    md=m.get("mid",[])
    s=m.get("slow",[])

    if len(f)<2: return None

    if f[-1]>f[-2] and md[-1]>md[-2] and s[-1]>s[-2]:
        return "BUY"
    if f[-1]<f[-2] and md[-1]<md[-2] and s[-1]<s[-2]:
        return "SELL"

def spread_filter():
    ob=state["orderbook"]
    if not ob["bids"] or not ob["asks"]:
        return False

    return (float(ob["asks"][0][0]) - float(ob["bids"][0][0])) < 5

def adaptive_price(side):
    ob=state["orderbook"]
    bid=float(ob["bids"][0][0])
    ask=float(ob["asks"][0][0])
    spread=ask-bid

    return bid+spread*0.3 if side=="BUY" else ask-spread*0.3

def delta_filter():
    d=state["delta"]
    if d>10: return "BUY"
    if d<-10: return "SELL"

def imbalance_zone():
    ob=state["orderbook"]
    bid=sum(float(x[1]) for x in ob["bids"])
    ask=sum(float(x[1]) for x in ob["asks"])

    if bid>ask*2: return "BUY"
    if ask>bid*2: return "SELL"

def absorption_detection():
    c=state["candles_m1"]
    if len(c)<2: return None

    move=c[-1]["close"]-c[-2]["close"]
    d=state["delta"]

    if d>15 and move<5: return "SELL"
    if d<-15 and move>-5: return "BUY"
