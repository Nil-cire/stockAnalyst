from typing import Dict

from twsecrawler import ref
from core import Candlestick
from database import DbMapper


def is_bollinger_deviate(check_date: str, stock_no: str):

    try:
        db = DbMapper.db_mapper(check_date)
        stock_info = db.find_single_stock(stock_no)
        date_price_info = stock_info["prices"][check_date]
        cur_p = date_price_info["end_p"]
        boll_high = date_price_info["index"]["boll"]["boll_high"]
        boll_low = date_price_info["index"]["boll"]["boll_low"]

    except Exception as e:
        print(f'!!! Fail to get bollinger or end_p value for stock = {stock_no}, at date = {check_date}')
        print(e)
        return False

    if cur_p > boll_high:
        return True

    if cur_p < boll_low:
        return True

    return False
