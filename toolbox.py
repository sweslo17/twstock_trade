# Import Built-Ins
import logging

# Import Third-Party
import pandas as pd
import numpy as np

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


def SMA(df, column="Close", period=20):

    sma = df[column].rolling(window=period, min_periods=period - 1).mean()
    return df.join(sma.to_frame('SMA'))



def EMA(df, column="Close", period=20):

    ema = df[column].ewm(span=period, min_periods=period - 1).mean()
    return df.join(ema.to_frame('EMA'))



def RSI(df, column="Close", window=14):
    # wilder's RSI
 
    delta = df[column].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.ewm(com=window - 1,  adjust=False).mean()
    rDown = down.ewm(com=window - 1, adjust=False).mean().abs()

    rsi = 100 - 100 / (1 + rUp / rDown)    

    return rsi

def RSV(inputs):
    return (inputs[-1]-inputs.min())/(inputs.max()-inputs.min())*100

def K_value(rsv_series):
    results = []
    for rsv in rsv_series:
        if pd.isna(rsv):
            results.append(rsv)
            last_k = rsv
        else:
            if pd.isna(last_k):
                results[-1] = 50
                last_k = 50
            now_k = last_k*(2/3)+rsv*(1/3)
            results.append(now_k)
            last_k = now_k
    return pd.Series(results)

def D_value(K_series):
    results = []
    for k in K_series:
        if pd.isna(k):
            results.append(k)
            last_d = k
        else:
            if pd.isna(last_d):
                results[-1] = 50
                last_d = 50
            now_d = last_d*(2/3)+k*(1/3)
            results.append(now_d)
            last_d = now_d
    return pd.Series(results)

def KD(df, column="收盤價", window=9):
    rsv_series = df[column].rolling(window).apply(RSV)
    k_series = K_value(rsv_series)
    d_series = D_value(k_series)
    return rsv_series, k_series, d_series
