import datetime
from dateutil.relativedelta import relativedelta
import requests
import time
import json
import random


BASE_URL = "https://news.cnyes.com/api/v2/news"

def get_list(start_timestamp, end_timestamp, page):
    print("page: {}".format(page))
    result = requests.get(BASE_URL, params={"startAt":start_timestamp,"endAt":end_timestamp,"limit":30, "page":page}).json()
    json.dump(result, open("news_list/{}_{}_{}.json".format(start_timestamp, end_timestamp, page), "w"))

start_date = datetime.datetime(2017,1,1,0,0,0)

while True:
    start_timestamp = int(time.mktime(start_date.timetuple()))
    end_date = start_date + relativedelta(months=2)
    end_timestamp = int(time.mktime(end_date.timetuple()))
    print(start_date, end_date)
    print(start_timestamp, end_timestamp)
    result = requests.get(BASE_URL, params={"startAt":start_timestamp,"endAt":end_timestamp,"limit":30}).json()
    start_page = 0 #from 0
    last_page = int(result["items"]["last_page"])
    for i in range(start_page, last_page):
        get_list(start_timestamp, end_timestamp, i+1)
        time.sleep(random.randint(1, 7)/10)
    start_date += relativedelta(months=2)
    if start_date > datetime.datetime.now():
        break
