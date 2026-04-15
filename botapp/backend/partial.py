from state import state
from bitget_api import close_position

def partial_tp():

    m=state.get("macd",{})
    f=m.get("fast",[])
    md=m.get("mid",[])

    if len(f)<2: return

    # weakening
    if f[-1]<f[-2] or md[-1]<md[-2]:
        print("⚡ PARTIAL CLOSE")

        close_position("SELL",0.001)
