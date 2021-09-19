from typing import Dict

from twsecrawler import ref
from core import Candlestick


def is_obv_deviate(sticks, interval: int, date: str) -> bool:
    keys = list(sticks)

    try:
        index = keys.index(date)
    except Exception as e:
        print("No such date, try again")
        print(e)
        return False

    max_price = None
    max_obv = None
    min_price = None
    min_obv = None

    for i in range((index - interval), index):  # past candles
        cd: Candlestick = sticks[keys[i]]

        if max_price is None:
            max_price = cd.end_p
        if min_price is None:
            min_price = cd.end_p
        if max_obv is None:
            max_obv = cd.obv
        if min_obv is None:
            min_obv = cd.obv

        # if cd.end_p > max_price:
        #     max_price = cd.end_p
        if cd.obv > max_obv:
            max_obv = cd.obv
            max_price = cd.end_p

        # if cd.end_p < min_price:
        #     min_price = cd.end_p
        if cd.obv < min_obv:
            min_obv = cd.obv
            min_price = cd.end_p

    cur_p = sticks[date].end_p
    cur_obv = sticks[date].obv

    if check_obv_deviate_high(max_price, max_obv, cur_p, cur_obv) or check_obv_deviate_low(min_price, min_obv, cur_p, cur_obv):
        print("Deviate")
        return True
    else:
        print("Not deviate")
        return False


def check_obv_deviate_high(com_p, com_obv, cur_p, cur_obv) -> bool:
    if com_obv > cur_obv:
        if com_p <= cur_p:
            return True

    if com_obv < cur_obv:
        if com_p >= cur_p:
            return True

    return False


def check_obv_deviate_low(com_p, com_obv, cur_p, cur_obv) -> bool:
    if com_obv > cur_obv:
        if com_p <= cur_p:
            return True

    if com_obv < cur_obv:
        if com_p >= cur_p:
            return True

    return False


def check_obv_deviate(com_p, com_obv, cur_p, cur_obv) -> bool:
    if com_obv > cur_obv:
        if com_p <= cur_p:
            return True

    if com_obv < cur_obv:
        if com_p >= cur_p:
            return True

    return False
