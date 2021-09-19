from typing import Dict

from twsecrawler import ref
from core import Candlestick


def is_rsi_deviate(sticks, interval: int, date: str) -> bool:
    keys = list(sticks)

    try:
        index = keys.index(date)
    except Exception as e:
        print("No such date, try again")
        print(e)
        return False

    max_price = None
    max_rsi = None
    min_price = None
    min_rsi = None

    for i in range((index - interval), index):  # past candles
        cd: Candlestick = sticks[keys[i]]

        if max_price is None:
            max_price = cd.end_p
        if min_price is None:
            min_price = cd.end_p
        if max_rsi is None:
            max_rsi = cd.rsi14
        if min_rsi is None:
            min_rsi = cd.rsi14

        # if cd.end_p > max_price:
        #     max_price = cd.end_p
        if cd.rsi14 > max_rsi:
            max_rsi = cd.rsi14
            max_price = cd.end_p

        # if cd.end_p < min_price:
        #     min_price = cd.end_p
        if cd.rsi14 < min_rsi:
            min_rsi = cd.rsi14
            min_price = cd.end_p

    cur_p = sticks[date].end_p
    cur_rsi = sticks[date].rsi14

    if check_obv_deviate_high(max_price, max_rsi, cur_p, cur_rsi) or check_obv_deviate_low(min_price, min_rsi, cur_p, cur_rsi):
        print("Deviate")
        return True
    else:
        print("Not deviate")
        return False


def check_obv_deviate_high(com_p, com_rsi, cur_p, cur_rsi) -> bool:
    if com_rsi > cur_rsi:
        if com_p <= cur_p:
            return True

    if com_rsi < cur_rsi:
        if com_p >= cur_p:
            return True

    return False


def check_obv_deviate_low(com_p, com_rsi, cur_p, cur_rsi) -> bool:
    if com_rsi > cur_rsi:
        if com_p <= cur_p:
            return True

    if com_rsi < cur_rsi:
        if com_p >= cur_p:
            return True

    return False


def check_obv_deviate(com_p, com_rsi, cur_p, cur_rsi) -> bool:
    if com_rsi > cur_rsi:
        if com_p <= cur_p:
            return True

    if com_rsi < cur_rsi:
        if com_p >= cur_p:
            return True

    return False
