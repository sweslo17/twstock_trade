import toolbox

def trans_int(input):
    try:
        return int(input)
    except:
        print(input)
        return None
    
def trans_float(input):
    try:
        return float(input)
    except:
        print(input)
        return None


def preprocess(df):
    """
    基礎數值轉換，日期排序
    
    Arguments:
        df {DataFrame}
    
    Returns:
        {DataFrame}
    """
    df["收盤價"] = df["收盤價"].map(trans_float)
    df["最高價"] = df["最高價"].map(trans_float)
    df["最低價"] = df["最低價"].map(trans_float)
    df.sort_values(by="date").reset_index()
    return df


def append_all_index(df):
    """
    加入技術指標KD, RSI, MA
    
    Arguments:
        df {DataFrame}
    
    Returns:
        {DataFrame}
    """
    df["MA_5"] = df["收盤價"].rolling(window=5).mean()
    df["MA_10"] = df["收盤價"].rolling(window=10).mean()
    df["MA_20"] = df["收盤價"].rolling(window=20).mean()
    df["RSI_5"] = toolbox.RSI(df, "收盤價", window=5)
    df["RSI_10"] = toolbox.RSI(df, "收盤價", window=10)
    df["RSV"], df["K_9"], df["D_9"] = toolbox.KD(df, "收盤價", window=9)
    return df