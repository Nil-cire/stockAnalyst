import time
import traceback
from typing import List

from database.TWSEdb import TWSEdb
from database import DbMapper
from twsecrawler import ref
import Basic
from core.Candlestick import Candlestick

sleep = 0


class IndexUpdater:

    cds = {}

    ma_day_list = [5, 10, 14, 20, 21, 60, 120, 150, 240]
    ma_list = []

    index_template = {
        "ma": {},
        "boll": {},
        "obv": {},
        "rsi": {}
    }

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

    def get_single_stock_index_data(self, stock_no: str, date: str):
        print(f'start update stock_no = {stock_no}')
        cds = self.get_stock_candles(stock_no, date)
        index = len(cds) - 1
        dates = list(cds)
        for ma_d in self.ma_day_list:
            try:
                ma = self.cal_ma(index, ma_d, cds)
                self.ma_list.append(round(ma, 2))
            except Exception as e:
                self.ma_list.append(0.00)
                print(e)

        sd20 = self.cal_sd(index, 20, cds)
        ma20 = self.ma_list[3]
        boll_high = round((ma20 + (2 * sd20)), 2)
        boll_mid = round(ma20)
        boll_low = round((ma20 - (2 * sd20)), 2)

        rsi5 = round(self.cal_rsi(5, index, cds), 2)
        rsi10 = round(self.cal_rsi(10, index, cds), 2)
        rsi14 = round(self.cal_rsi(14, index, cds), 2)
        rsi20 = round(self.cal_rsi(20, index, cds), 2)

        # fill templates
        self.ma_template["ma5"] = self.ma_list[0]
        self.ma_template["ma10"] = self.ma_list[1]
        self.ma_template["ma14"] = self.ma_list[2]
        self.ma_template["ma20"] = self.ma_list[3]
        self.ma_template["ma21"] = self.ma_list[4]
        self.ma_template["ma60"] = self.ma_list[5]
        self.ma_template["ma120"] = self.ma_list[6]
        self.ma_template["ma150"] = self.ma_list[7]
        self.ma_template["ma240"] = self.ma_list[8]

        self.bollinger_template["boll_high"] = boll_high
        self.bollinger_template["boll_mid"] = boll_mid
        self.bollinger_template["boll_low"] = boll_low

        y_obv = cds[dates[index-1]].obv
        y_price = cds[dates[index-1]].end_p
        t_price = cds[dates[index]].end_p
        t_amount = cds[dates[index]].amount
        t_obv = 0

        if t_price > y_price:
            t_obv = y_obv + t_amount
        if t_price < y_price:
            t_obv = y_obv - t_amount
        if t_price == y_price:
            t_obv = y_obv

        self.obv_template["obv"] = t_obv

        self.rsi_template["rsi5"] = rsi5
        self.rsi_template["rsi10"] = rsi10
        self.rsi_template["rsi14"] = rsi14
        self.rsi_template["rsi20"] = rsi20

        self.index_template["ma"] = self.ma_template
        self.index_template["boll"] = self.bollinger_template
        self.index_template["obv"] = self.obv_template
        self.index_template["rsi"] = self.rsi_template

        return self.index_template

    def get_stock_candles(self, stock_no: str, date: str):
        start_day = date[0: 4] + "0101"
        end_day = date[0: 4] + "1231"
        self.cds = Basic.get_candlesticks(stock_no, start_day, end_day)
        return self.cds

    def update_ma(self, ma5, ma10, ma14, ma20, ma21, ma60, ma120, ma150, ma240):
        self.ma_template["ma5"] = ma5
        self.ma_template["ma10"] = ma10
        self.ma_template["ma14"] = ma14
        self.ma_template["ma20"] = ma20
        self.ma_template["ma21"] = ma21
        self.ma_template["ma60"] = ma60
        self.ma_template["ma120"] = ma120
        self.ma_template["ma150"] = ma150
        self.ma_template["ma240"] = ma240

    def update_bollinger(self, boll_high, boll_mid, boll_low):
        self.bollinger_template["boll_high"] = boll_high
        self.bollinger_template["boll_mid"] = boll_mid
        self.bollinger_template["boll_low"] = boll_low

    def update_obv(self, obv):
        self.obv_template["obv"] = obv

    def update_rsi(self, rsi5, rsi10, rsi14, rsi20):
        self.rsi_template["rsi5"] = rsi5
        self.rsi_template["rsi10"] = rsi10
        self.rsi_template["rsi14"] = rsi14
        self.rsi_template["rsi20"] = rsi20

    @staticmethod
    def cal_ma(day_index: int, day_interval: int, cds):
        key_list = list(cds)
        total_p = 0
        for d in range(day_index - (day_interval - 1), day_index + 1):
            total_p += cds[key_list[d]].end_p
        maa = total_p / day_interval
        return maa

    @staticmethod
    def cal_sd(day_index: int, day_interval: int, cds):
        key_list = list(cds)
        total_p = 0
        sum_p = 0
        for d in range(day_index - (day_interval - 1), day_index + 1):
            sum_p += cds[key_list[d]].end_p

        avg = sum_p / day_interval

        for d in range(day_index - (day_interval - 1), day_index + 1):
            temp = cds[key_list[d]].end_p - avg
            total_p += temp ** 2
        t2 = total_p / day_interval
        return round((t2 ** 0.5), 2)

    @staticmethod
    def cal_rsi(day_interval: int, day_index: int, cds):
        key_list = list(cds)
        total_up = 0
        total_down = 0
        for d in range(day_index - (day_interval - 1), (day_index + 1)):
            cd_yesterday: Candlestick = cds[key_list[(d-1)]]
            cd: Candlestick = cds[key_list[d]]
            price_today = cd.end_p
            price_yesterday = cd_yesterday.end_p
            delta = price_today - price_yesterday

            if delta > 0:
                total_up += delta
            if delta < 0:
                total_down += (- delta)

        return 100 * (total_up / (total_up + total_down))


    # def update_to_db


# db = ""
# collection = ""

index_template = {
    "ma": {},
    "boll": {},
    "obv": {},
    "rsi": {}
}

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


def initialize_index(date: str, country: str = "TWSE"):

    year = date[0: 4]
    start_day = year + "0101"
    end_day = year + "0924"

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
    # ordered_sticks: dict = Basic.get_candlesticks(str(5608), start_day, end_day, db)
    stick_count = len(ordered_sticks)
    print(stick_count)
    key_list = list(ordered_sticks)

    # update stock
    count = 0
    total_count = 0
    for stock_no in listed_dict.keys():
        ordered_sticks: dict = Basic.get_candlesticks(str(stock_no), start_day, end_day, db)
        stick_count = len(ordered_sticks)
        key_list = list(ordered_sticks)

        total_count += 1

        obv = 0

        # update every_day for a stock
        for i in range(0, stick_count):

            key_date = key_list[i]
            if i > 0:
                y_key_date = key_list[i-1]

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
                obv = 0
                if i == 0:
                    obv = 0
                else:

                    y_obv = ordered_sticks[y_key_date].obv
                    y_price = ordered_sticks[y_key_date].end_p
                    t_price = ordered_sticks[key_date].end_p
                    t_amount = ordered_sticks[key_date].amount

                    if t_price > y_price:
                        obv = y_obv + t_amount
                    if t_price < y_price:
                        obv = y_obv - t_amount
                    if t_price == y_price:
                        obv = y_obv

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

                new_index_template = index_template
                new_index_template["ma"] = new_ma_temp
                new_index_template["boll"] = new_bollinger_temp
                new_index_template["obv"] = new_obv_temp
                new_index_template["rsi"] = new_rsi_temp

                # do updates
                # # ma
                # ma_update_key = f'prices.{key_date}.index.ma'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {ma_update_key: new_ma_temp}})
                #
                # # bollinger
                # bollinger_update_key = f'prices.{key_date}.index.boll'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {bollinger_update_key: new_bollinger_temp}})
                #
                # # obv
                # obv_update_key = f'prices.{key_date}.index.obv'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {obv_update_key: new_obv_temp}})
                #
                # # rsi
                # rsi_update_key = f'prices.{key_date}.index.rsi'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: rsi_template}})

                # all indexes
                rsi_update_key = f'prices.{key_date}.index'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: new_index_template}})

                count += 1
                # time.sleep(sleep)
                print(f'Success to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
            except Exception as e:
                print(f'!!! Fail to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
                print(e)
    print(f'Done update listed stock indexes, total updates = {count} / total = {total_count}')

    count = 0
    total_count = 0
    for stock_no in unlisted_dict.keys():
        ordered_sticks: dict = Basic.get_candlesticks(str(stock_no), start_day, end_day, db)
        stick_count = len(ordered_sticks)
        key_list = list(ordered_sticks)

        total_count += 1

        obv = 0

        # update every_day for a stock
        for i in range(0, stick_count):

            key_date = key_list[i]
            if i > 0:
                y_key_date = key_list[i-1]

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
                obv = 0
                if i == 0:
                    obv = 0
                else:
                    y_obv = ordered_sticks[y_key_date].obv
                    y_price = ordered_sticks[y_key_date].end_p
                    t_price = ordered_sticks[key_date].end_p
                    t_amount = ordered_sticks[key_date].amount

                    if t_price > y_price:
                        obv = y_obv + t_amount
                    if t_price < y_price:
                        obv = y_obv - t_amount
                    if t_price == y_price:
                        obv = y_obv

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

                new_index_template = index_template
                new_index_template["ma"] = new_ma_temp
                new_index_template["boll"] = new_bollinger_temp
                new_index_template["obv"] = new_obv_temp
                new_index_template["rsi"] = new_rsi_temp

                # do updates
                # # ma
                # ma_update_key = f'prices.{key_date}.index.ma'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {ma_update_key: new_ma_temp}})
                #
                # # bollinger
                # bollinger_update_key = f'prices.{key_date}.index.boll'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {bollinger_update_key: new_bollinger_temp}})
                #
                # # obv
                # obv_update_key = f'prices.{key_date}.index.obv'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {obv_update_key: new_obv_temp}})
                #
                # # rsi
                # rsi_update_key = f'prices.{key_date}.index.rsi'
                # db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: rsi_template}})

                # all indexes
                rsi_update_key = f'prices.{key_date}.index'
                db.my_col.update_one({"_id": int(stock_no)}, {"$set": {rsi_update_key: new_index_template}})

                count += 1
                # time.sleep(sleep)
                print(f'Success to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
            except Exception as e:
                print(f'!!! Fail to add stock indexes data, stock_no = {stock_no}, date = "{key_date}"')
                print(e)
    print(f'Done update listed stock indexes, total updates = {count} / total = {total_count}')

    db.my_client.close()
