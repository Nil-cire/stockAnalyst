import traceback
from typing import List

from database.TWSEdb import TWSEdb
from database import DbMapper
from twsecrawler import ref
import Basic
from core.Candlestick import Candlestick


# db = ""
# collection = ""

ma_template = {
    "ma5": 0.0,
    "ma10": 0.0,
    "ma14": 0.0,
    "ma20": 0.0,
    "ma21": 0.0,
    "ma60": 0.0,
    "ma120": 0.0,
    "ma150": 0.0,
    "ma240": 0.0
}

bollinger_template = {
    "boll_high": 0.0,
    "boll_mid": 0.0,
    "boll_low": 0.0
}

obv_template = {
    "obv": 0
}

rsi_template = {
    "rsi5": 0.0,
    "rsi10": 0.0,
    "rsi14": 0.0,
    "rsi20": 0.0
}


def update_ma(stock: str, date: str, country: str = "TWSE"):
    db = DbMapper.db_mapper(date, country)
    listed_dict = ref.get_listed_dict()
    unlisted_dict = ref.get_unlisted_dict()

    for key in listed_dict.keys():
        pass


def initialize_ma(date: str, country: str = "TWSE"):

    year = date[0: 4]
    start_day = year + "0101"
    end_day = year + "1231"

    ma_day_list = [5, 10, 14, 20, 21, 60, 120, 150, 240]

    db = DbMapper.db_mapper(date, country)
    listed_dict = ref.get_listed_dict()
    unlisted_dict = ref.get_unlisted_dict()

    ordered_sticks: dict = {}

    def cal_ma(day_index: int, day_interval: int):
        total_p = 0
        for d in range(day_index - (day_interval - 1), day_index + 1):
            total_p += ordered_sticks[key_list[d]].end_p
        maa = total_p / day_interval
        return maa

    def cal_sd(day_index: int, avg: float, day_interval: int):
        total_p = 0
        for d in range(day_index - (day_interval - 1), day_index + 1):
            temp = ordered_sticks[key_list[d]].end_p - avg
            total_p += temp ** 2
        t2 = total_p / day_interval
        return round((t2 ** 0.5), 2)

    def cal_rsi(day_interval: int, day_index: int):
        total_up = 0
        total_down = 0
        for d in range(day_index - (day_interval - 1), (day_index + 1)):
            cd_yesterday: Candlestick = ordered_sticks[key_list[(d-1)]]
            cd: Candlestick = ordered_sticks[key_list[d]]
            price_today = cd.end_p
            price_yesterday = cd_yesterday.end_p
            delta = price_today - price_yesterday

            if delta > 0:
                total_up += delta
            if delta < 0:
                total_down += (- delta)

        return 100 * (total_up / (total_up + total_down))

    # ordered_sticks: dict = Basic.get_candlesticks(str(stock_no), start_day, end_day, db)
    ordered_sticks: dict = Basic.get_candlesticks(str(5608), start_day, end_day, db)
    stick_count = len(ordered_sticks)
    print(stick_count)
    key_list = list(ordered_sticks)

    # update stock
    count = 0
    for stock_no in listed_dict.keys():
        ordered_sticks: dict = Basic.get_candlesticks(str(stock_no), start_day, end_day, db)
        stick_count = len(ordered_sticks)
        key_list = list(ordered_sticks)

        obv = 0

        # update every_day for a stock
        for i in range(0, stick_count):

            key_date = key_list[i]

            ma_list = {}
            sd20 = 0.0
            rsi_5 = 0.00
            rsi_10 = 0.00
            rsi_14 = 0.00
            rsi_20 = 0.00

            try:
                # ma: many of them
                for ma_day in ma_day_list:
                    day = ma_day
                    if i >= day - 1:
                        ma = round(cal_ma(i, day), 2)
                        ma_list[str(day)] = ma

                        # bollinger
                        if day == 20:
                            sd20 = cal_sd(i, ma, day)
                    else:
                        ma_list[str(day)] = 0.0

                # obv
                if i == 0:
                    obv = 0
                if i > 0 and ordered_sticks[key_date].trend == "UP":
                    obv += ordered_sticks[key_date].amount
                if i > 0 and ordered_sticks[key_date].trend == "DOWN":
                    obv -= ordered_sticks[key_date].amount
                if i > 0 and ordered_sticks[key_date].trend == "EVEN":
                    pass

                # rsi
                if i >= 5:
                    rsi_5 = round(cal_rsi(5, i), 2)
                if i >= 10:
                    rsi_10 = round(cal_rsi(10, i), 2)
                if i >= 14:
                    rsi_14 = round(cal_rsi(14, i), 2)
                if i >= 20:
                    rsi_20 = round(cal_rsi(20, i), 2)

                # fill templates
                new_ma_temp = ma_template
                new_ma_temp["ma5"] = ma_list["5"]
                new_ma_temp["ma10"] = ma_list["10"]
                new_ma_temp["ma14"] = ma_list["14"]
                new_ma_temp["ma20"] = ma_list["20"]
                new_ma_temp["ma21"] = ma_list["21"]
                new_ma_temp["ma60"] = ma_list["60"]
                new_ma_temp["ma120"] = ma_list["120"]
                new_ma_temp["ma150"] = ma_list["150"]
                new_ma_temp["ma240"] = ma_list["240"]

                ma20 = ma_list["20"]
                new_bollinger_temp = bollinger_template
                new_bollinger_temp["boll_high"] = ma20 + (2 * sd20)
                new_bollinger_temp["boll_mid"] = ma20
                new_bollinger_temp["boll_low"] = ma20 - (2 * sd20)

                new_obv_temp = obv_template
                new_obv_temp["obv"] = obv

                new_rsi_temp = rsi_template
                new_rsi_temp["rsi5"] = rsi_5
                new_rsi_temp["rsi10"] = rsi_10
                new_rsi_temp["rsi14"] = rsi_14
                new_rsi_temp["rsi20"] = rsi_20

                # do updates
                # ma
                ma_update_key = f'prices.{key_date}.index.ma'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {ma_update_key: new_ma_temp}})

                # bollinger
                bollinger_update_key = f'prices.{key_date}.index.boll'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {bollinger_update_key: new_bollinger_temp}})

                # obv
                obv_update_key = f'prices.{key_date}.index.obv'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {obv_update_key: new_obv_temp}})

                # rsi
                rsi_update_key = f'prices.{key_date}.index.rsi'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: rsi_template}})

                count += 1
                print(f'Success to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
            except Exception as e:
                print(f'!!! Fail to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
                print(e)
    print(f'Done update listed stock indexes, total updates = {count}')

    count = 0
    for stock_no in unlisted_dict.keys():
        ordered_sticks: dict = Basic.get_candlesticks(str(stock_no), start_day, end_day, db)
        stick_count = len(ordered_sticks)
        key_list = list(ordered_sticks)

        obv = 0

        # update every_day for a stock
        for i in range(0, stick_count):

            key_date = key_list[i]

            ma_list = {}
            sd20 = 0.0
            rsi_5 = 0.00
            rsi_10 = 0.00
            rsi_14 = 0.00
            rsi_20 = 0.00

            try:
                # ma: many of them
                for ma_day in ma_day_list:
                    day = ma_day
                    if i >= day - 1:
                        ma = round(cal_ma(i, day), 2)
                        ma_list[str(day)] = ma

                        # bollinger
                        if day == 20:
                            sd20 = cal_sd(i, ma, day)
                    else:
                        ma_list[str(day)] = 0.0

                # obv
                if i == 0:
                    obv = 0
                if i > 0 and ordered_sticks[key_date].trend == "UP":
                    obv += ordered_sticks[key_date].amount
                if i > 0 and ordered_sticks[key_date].trend == "DOWN":
                    obv -= ordered_sticks[key_date].amount
                if i > 0 and ordered_sticks[key_date].trend == "EVEN":
                    pass

                # rsi
                if i >= 5:
                    rsi_5 = round(cal_rsi(5, i), 2)
                if i >= 10:
                    rsi_10 = round(cal_rsi(10, i), 2)
                if i >= 14:
                    rsi_14 = round(cal_rsi(14, i), 2)
                if i >= 20:
                    rsi_20 = round(cal_rsi(20, i), 2)

                # fill templates
                new_ma_temp = ma_template
                new_ma_temp["ma5"] = ma_list["5"]
                new_ma_temp["ma10"] = ma_list["10"]
                new_ma_temp["ma14"] = ma_list["14"]
                new_ma_temp["ma20"] = ma_list["20"]
                new_ma_temp["ma21"] = ma_list["21"]
                new_ma_temp["ma60"] = ma_list["60"]
                new_ma_temp["ma120"] = ma_list["120"]
                new_ma_temp["ma150"] = ma_list["150"]
                new_ma_temp["ma240"] = ma_list["240"]

                ma20 = ma_list["20"]
                new_bollinger_temp = bollinger_template
                new_bollinger_temp["boll_high"] = ma20 + (2 * sd20)
                new_bollinger_temp["boll_mid"] = ma20
                new_bollinger_temp["boll_low"] = ma20 - (2 * sd20)

                new_obv_temp = obv_template
                new_obv_temp["obv"] = obv

                new_rsi_temp = rsi_template
                new_rsi_temp["rsi5"] = rsi_5
                new_rsi_temp["rsi10"] = rsi_10
                new_rsi_temp["rsi14"] = rsi_14
                new_rsi_temp["rsi20"] = rsi_20

                # do updates
                # ma
                ma_update_key = f'prices.{key_date}.index.ma'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {ma_update_key: new_ma_temp}})

                # bollinger
                bollinger_update_key = f'prices.{key_date}.index.boll'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {bollinger_update_key: new_bollinger_temp}})

                # obv
                obv_update_key = f'prices.{key_date}.index.obv'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {obv_update_key: new_obv_temp}})

                # rsi
                rsi_update_key = f'prices.{key_date}.index.rsi'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: rsi_template}})

                count += 1
                print(f'Success to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
            except Exception as e:
                print(f'!!! Fail to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
                print(e)
    print(f'Done update listed stock indexes, total updates = {count}')

