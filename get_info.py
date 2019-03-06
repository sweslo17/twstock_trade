import requests
import pandas as pd
import numpy as np
import time
import random
import logging
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def date_trans(raw_date):
    try:
        return datetime(int(raw_date[0:3])+1911, int(raw_date[4:6]), int(raw_date[7:9]))
    except:
        print(raw_date)
        raise

def get_price(stock_no, start_date, end_date):
    all_df = pd.DataFrame()
    now_date = start_date
    while True:
        print("get {} price: {}".format(stock_no, now_date.strftime("%Y%m%d")))
        r = requests.get("http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}&_={}".format(now_date.strftime("%Y%m%d"), stock_no, int(time.time())))
        if r.status_code != 200:
            time.sleep(5)
            continue
        raw_json = r.json()
        data = raw_json["data"]
        fields = raw_json["fields"]
        time.sleep(random.randint(6,20)/2)
        all_df = pd.concat([all_df,pd.DataFrame(data=np.array(data), columns=fields)])
        now_date = now_date + relativedelta(months=1)
        if now_date >= end_date:
            break
    all_df["date"] = all_df["日期"].map(date_trans)
    return all_df

def get_info(stock_no, start_date, end_date):
    all_df = pd.DataFrame()
    now_date = start_date
    while True:
        print("get {} info: {}".format(stock_no, now_date.strftime("%Y%m%d")))
        r = requests.get("http://www.twse.com.tw/exchangeReport/BWIBBU?response=json&date={}&stockNo={}&_={}".format(now_date.strftime("%Y%m%d"), stock_no, int(time.time())))
        if r.status_code != 200:
            time.sleep(5)
            continue
        raw_json = r.json()
        data = raw_json["data"]
        fields = raw_json["fields"]
        time.sleep(random.randint(6,20)/2)
        all_df = pd.concat([all_df,pd.DataFrame(data=np.array(data), columns=fields)])
        now_date = now_date + relativedelta(months=1)
        if now_date >= end_date:
            break
    all_df["date"] = all_df["日期"].map(date_trans)
    return all_df

def get_stock_merge_info(stock_no, start_date, end_date):
    info_df = get_info(stock_no, start_date, end_date)
    price_df = get_price(stock_no, start_date, end_date)
    df = pd.merge(info_df, price_df, on="date")
    return df

if __name__ == '__main__':
    start_date = datetime(2013,1,1)
    end_date = datetime(2019,3,1)

    for stock_line in open("./crawl_list/ETF50.txt").readlines():
        try:
            stock_no = stock_line.split()[1]
            stock_name = stock_line.split()[0]
            if stock_no + ".xlsx" not in os.listdir("./crawl_result/ETF50/"):
                df = get_stock_merge_info(stock_no, start_date, end_date)
                df["stock_name"] = stock_name
                df.to_excel("./crawl_result/ETF50/{}.xlsx".format(stock_no))
        except:
            logging.exception("crawl error")
            f = open("./error.txt", "a")
            f.write(stock_no+"\n")
    
    for stock_line in open("./crawl_list/ETF100.txt").readlines():
        try:
            stock_no = stock_line.split()[1]
            stock_name = stock_line.split()[0]
            if stock_no + ".xlsx" not in os.listdir("./crawl_result/ETF100/"):
                df = get_stock_merge_info(stock_no, start_date, end_date)
                df["stock_name"] = stock_name
                df.to_excel("./crawl_result/ETF100/{}.xlsx".format(stock_no))
        except:
            logging.exception("crawl error")
            f = open("./error.txt", "a")
            f.write(stock_no+"\n")