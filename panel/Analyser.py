from database.TWSEdb import TWSEdb
from twsecrawler import ref
from twsecrawler.StockBaseCrawler import StockBaseCrawler
from bs4 import BeautifulSoup as bs
import time


def add_new_listed_stock_to_db():
    listed_dict = ref.get_listed_stocks_info()

    db = TWSEdb("stock_twse", "basePrice")

    for (key, value) in listed_dict.items():
        if len(key) < 5:
            try:
                db.add_stock_info(key, value[1], "TWSE", value[3], value[2], value[4], "NTD", 2)
            except Exception as e:
                print(e)


def add_new_unlisted_stock_to_db():
    listed_dict = ref.get_unlisted_stocks_info()

    db = TWSEdb("stock_twse", "basePrice")

    for (key, value) in listed_dict.items():
        if len(key) < 5:
            try:
                db.add_stock_info(key, value[1], "TWSE", value[3], value[2], value[4], "NTD", 2)
            except Exception as e:
                print(e)


def update_single_stock_price_by_month(stock_no: str, date: str, db: TWSEdb = None):
    if TWSEdb is None:
        db = TWSEdb("stock_twse", "basePrice")
    res = StockBaseCrawler.craw_data_from_twse(stock_no, date)
    if res != "":
        b_data = bs(res, "html.parser")
        big_data = b_data.find_all("tbody")[0]
        data = big_data.find_all("tr")

        for d in data:
            detail = d.find_all("td")
            format_string = detail[0].text.replace("/", "")
            new_date = str(int(format_string[0: 3]) + 1911) + format_string[3:7]
            high_p = detail[4].text
            low_p = detail[5].text
            start_p = detail[3].text
            end_p = detail[6].text
            amount = detail[1].text.replace(",", "")

            db.add_price_data(int(stock_no), new_date, float(high_p), float(low_p), float(start_p), float(end_p), int(amount))


def update_all_listed_stock_price_by_month(date: str):
    listed_dict = ref.get_listed_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in listed_dict:
        if len(key) < 5:
            try:
                time.sleep(8)
                update_single_stock_price_by_month(str(key), date, db)
            except Exception as e:
                print(e)


def update_all_unlisted_stock_price_by_month(date: str):
    unlisted_dict = ref.get_unlisted_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in unlisted_dict:
        if len(key) < 5:
            try:
                time.sleep(8)
                update_single_stock_price_by_month(str(key), date, db)
            except Exception as e:
                print(e)
