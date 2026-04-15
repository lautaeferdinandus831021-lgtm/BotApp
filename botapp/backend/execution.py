from macd import triple_macd
from bitget_api import place_order, place_oco
from state import state

def execute():

    sig = triple_macd(state["candles_m1"])
    if not sig:
        return

    price = state["price"]
    size = 0.01

    # hedge: buka dua arah (limit atas & bawah)
    if sig == "BUY":
        entry = price
        tp = price + 5
        sl = price - 5

    else:
        entry = price
        tp = price - 5
        sl = price + 5

    place_order(sig, entry, size)
    place_oco(sig, tp, sl, size)

    state["position"] = sig
    state["entry"] = entry
    state["tp"] = tp
    state["sl"] = sl
