import pandas as pd

def macd(series, fast, slow):
    return series.ewm(span=fast).mean() - series.ewm(span=slow).mean()

def triple_macd(candles):
    if len(candles) < 30:
        return None

    close = pd.Series([c["close"] for c in candles])

    m1 = macd(close,2,3)
    m2 = macd(close,3,4)
    m3 = macd(close,4,5)

    sig1 = m1.iloc[-1] > 0
    sig2 = m2.iloc[-1] > 0
    sig3 = m3.iloc[-1] > 0

    if sig1 and sig2 and sig3:
        return "BUY"
    if not sig1 and not sig2 and not sig3:
        return "SELL"
    return None
