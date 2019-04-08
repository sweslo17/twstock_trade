from trade_logger import TradeLogger, EventType



def _index_cross(slow_idx_now, fast_idx_now, slow_idx_last, fast_idx_last, golden=True):
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