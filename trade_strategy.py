from trade_logger import TradeLogger, EventType



def _index_cross(slow_idx_now, fast_idx_now, slow_idx_last, fast_idx_last, golden=True):
    """
    偵測黃金交叉/死亡交叉
    
    Arguments:
        slow_idx_now {float} -- 前一點的慢線值
        fast_idx_now {float} -- 前一點的快線值
        slow_idx_last {float} -- 現在的慢線值
        fast_idx_last {float} -- 現在的快線值
    
    Keyword Arguments:
        golden {bool} -- 是否為黃金交叉 (default: {True})
    
    Returns:
        bool
    """
    if golden:
        if (slow_idx_last >= fast_idx_last) and (slow_idx_now < fast_idx_now):
            return True
        return False
    else:
        if (slow_idx_last <= fast_idx_last) and (slow_idx_now > fast_idx_now):
            return True
        return False
    return False


def baseline(df, money_in_pocket, from_date, to_date, stock_share=0):
    """
    baseline model
    一開始就all in領股利
    
    Arguments:
        df {DataFrame}
        money_in_pocket {float} -- 可以用來操作的金錢
        from_date {datetime} -- 開始時間
        to_date {datetime} -- 結束時間
    
    Keyword Arguments:
        stock_share {int} -- 一開始持有的股票 (default: {0})
    
    Returns:
        money_in_pocket {int} -- 剩餘金錢
        stock_share {int} -- 持有股票
        price {float} -- 最後的收盤價
        logger {TradeLogger} -- 交易記錄
    """
    trade_logger = TradeLogger()
    stock_share = 0
    process_df = df[(df["date"]>=from_date) & (df["date"]<=to_date)]
    stock_share = int(money_in_pocket/process_df.iloc[0]["收盤價"])
    money_in_pocket -= stock_share*process_df.iloc[0]["收盤價"]
    trade_logger.buy_stock(from_date, stock_share, process_df.iloc[0]["收盤價"], money_in_pocket)
    
    for idx, row in process_df.iterrows():
        if row['是否為除息日']:
            money_in_pocket += stock_share*row["現金股利"]
            trade_logger.get_interest(row["date"], stock_share, row["現金股利"], money_in_pocket)
        if row['是否為除權日']:
            money_in_pocket += stock_share*row["股票股利"]
            trade_logger.get_interest(row["date"], stock_share, row["股票股利"], money_in_pocket)
    #結算
    return money_in_pocket, stock_share, process_df.iloc[-1]["收盤價"], trade_logger


def KD_basic(df, money_in_pocket, from_date, to_date, K_threshold=(20,80), D_threshold=(20,80), stock_share=0):
    """
    KD基礎model
    K,D>threshold賣出，K,D<threshold買進，加入是否黃金交叉判斷
    
    Arguments:
        df {DataFrame}
        money_in_pocket {float} -- 可以用來操作的金錢
        from_date {datetime} -- 開始時間
        to_date {datetime} -- 結束時間
    
    Keyword Arguments:
        K_threshold {tuple} -- K值threshold (default: {(20,80)})
        D_threshold {tuple} -- D值threshold (default: {(20,80)})
        stock_share {int} -- 一開始持有的股票 (default: {0})
    
    Returns:
        money_in_pocket {int} -- 剩餘金錢
        stock_share {int} -- 持有股票
        price {float} -- 最後的收盤價
        logger {TradeLogger} -- 交易記錄
    """
    trade_logger = TradeLogger()
    process_df = df[(df["date"]>=from_date) & (df["date"]<=to_date)]
    last_K = process_df.iloc[0]["K_9"]
    last_D = process_df.iloc[0]["D_9"]
    for idx, row in process_df.iterrows():
        if row['是否為除息日']:
            money_in_pocket += stock_share*row["現金股利"]
            trade_logger.get_interest(row["date"], stock_share, row["現金股利"], money_in_pocket)
        if row['是否為除權日']:
            money_in_pocket += stock_share*row["股票股利"]
            trade_logger.get_interest(row["date"], stock_share, row["股票股利"], money_in_pocket)
        if row["K_9"] <= K_threshold[0] and row["D_9"] <= D_threshold[0]:# and _index_cross(row["D_9"], row["K_9"], last_D, last_K, golden=True):
            if money_in_pocket >= row["收盤價"]:
                money_in_pocket -= row["收盤價"]
                stock_share += 1
                trade_logger.buy_stock(row["date"], 1, row["收盤價"], money_in_pocket)
        elif row["K_9"] >= K_threshold[1] and row["D_9"] >= D_threshold[1]:# and _index_cross(row["D_9"], row["K_9"], last_D, last_K, golden=False):
            if stock_share > 0:
                stock_share -= 1
                money_in_pocket += row["收盤價"]
                trade_logger.sell_stock(row["date"], 1, row["收盤價"], money_in_pocket)
        last_K = row["K_9"]
        last_D = row["D_9"]
    return money_in_pocket, stock_share, process_df.iloc[-1]["收盤價"], trade_logger