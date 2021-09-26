from typing import Dict
from panel import Basic
from core.Candlestick import Candlestick

large_cd_per = 0.035
mid_cd_per = 0.015
small_cd_per = 0.005


def chop_last(cds: Dict[str, Candlestick], chopped_size: int):
    keys = sorted(list(cds))
    size = len(keys)
    temp_cds = {}
    for i in range((size - chopped_size), size):
        try:
            temp_cds[keys[i]] = cds[keys[i]]
        except Exception:
            pass

    return temp_cds


def is_morning_star(cds: Dict[str, Candlestick]) -> bool:

    if len(cds) < 4:
        print("error on is_morning_star, size of cds < 3")
        return False

    if len(cds) != 4:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "DOWN":
        print("1")
        return False
    if c2.trend != "UP":
        print("2")
        return False

    # cd size
    if (c0.solid_range / c0.start_p) < large_cd_per:
        print(keys[0])
        print(c0.solid_range)
        print(c0.start_p)
        print(c0.solid_range / c0.start_p)
        print("3")
        return False
    if (c1.solid_range / c1.start_p) > mid_cd_per:
        print("4")
        return False
    if (c2.solid_range / c2.start_p) < large_cd_per:
        print("5")
        return False

    # price compare
    if c1.start_p > c0.end_p or c1.end_p > c0.end_p:
        print("6")
        return False
    if c2.start_p < c1.start_p or c2.start_p < c1.end_p:
        print("7")
        return False

    return True


def is_evening_star(cds: Dict[str, Candlestick]) -> bool:

    if len(cds) < 3:
        print("error on is_evening_star, size of cds < 3")
        return False

    if len(cds) != 3:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "UP":
        return False
    if c2.trend != "DOWN":
        return False

    # cd size
    if (c0.solid_range / c0.end_p) < large_cd_per:
        return False
    if (c1.solid_range / c1.end_p) > mid_cd_per:
        return False
    if (c2.solid_range / c2.end_p) < large_cd_per:
        return False

    # price compare
    if c1.start_p < c0.end_p or c1.end_p < c0.end_p:
        return False
    if c2.start_p > c1.start_p or c2.start_p > c1.end_p:
        return False

    return True


def is_bull_flag(cds: Dict[str, Candlestick]) -> bool:
    if len(cds) < 3:
        print("error on is_bull_flag, size of cds < 3")
        return False

    if len(cds) != 3:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "UP":
        return False
    if c1.trend != "DOWN":
        return False
    if c2.trend != "DOWN":
        return False

    # cd size
    if (c0.solid_range / c0.end_p) < large_cd_per:
        return False
    if (c1.solid_range / c1.end_p) > large_cd_per:
        return False
    if (c2.solid_range / c2.end_p) > large_cd_per:
        return False

    # price compare
    if c1.start_p > c0.end_p or c1.end_p < c0.start_p:
        return False
    if c2.start_p > c0.end_p or c2.end_p < c0.start_p:
        return False

    return True


def is_bear_flag(cds: Dict[str, Candlestick]) -> bool:
    if len(cds) < 3:
        print("error on is_bull_flag, size of cds < 3")
        return False

    if len(cds) != 3:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "DOWN":
        return False
    if c1.trend != "UP":
        return False
    if c2.trend != "UP":
        return False

    # cd size
    if (c0.solid_range / c0.end_p) < large_cd_per:
        return False
    if (c1.solid_range / c1.end_p) > large_cd_per:
        return False
    if (c2.solid_range / c2.end_p) > large_cd_per:
        return False

    # price compare
    if c1.end_p > c0.start_p or c1.start_p < c0.end_p:
        return False
    if c2.end_p > c0.start_p or c2.start_p < c0.end_p:
        return False

    return True


def is_three_star_south(cds: Dict[str, Candlestick]):
    if len(cds) < 3:
        print("error on is_three_star_south, size of cds < 3")
        return False

    if len(cds) != 3:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "DOWN":
        return False
    if c1.trend != "DOWN":
        return False
    if c2.trend != "DOWN":
        return False

    # cd size
    if c0.solid_range < c1.solid_range or c1.solid_range < c2.solid_range:
        return False

    # price compare
    if c0.end_p < c1.end_p or c1.end_p < c2.end_p:
        return False

    return True


def is_advanced_block(cds: Dict[str, Candlestick]):
    if len(cds) < 3:
        print("error on is_three_star_south, size of cds < 3")
        return False

    if len(cds) != 3:
        cd3 = chop_last(cds, 3)
        keys = list(cd3)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]
    else:
        keys = list(cds)
        c0 = cds[keys[0]]
        c1 = cds[keys[1]]
        c2 = cds[keys[2]]

    if c0.trend != "UP":
        return False
    if c1.trend != "UP":
        return False
    if c2.trend != "UP":
        return False

    # cd size
    if c0.solid_range < c1.solid_range or c1.solid_range < c2.solid_range:
        return False

    # price compare
    if c0.end_p > c1.end_p or c1.end_p > c2.end_p:
        return False

    return True
