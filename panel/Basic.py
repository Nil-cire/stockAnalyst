from database.TWSEdb import TWSEdb
from core.Candlestick import Candlestick


def get_candlesticks(stock_no: str, start_day: str, end_day: str, db: TWSEdb = None):

    if db is None:
        ddb = TWSEdb("stock_twse", "basePrice")
    else:
        ddb = db

    candlesticks = {}

    c_price_data = ddb.find_single_stock(stock_no)["prices"]

    sd = int(start_day)
    ed = int(end_day)

    for date in range(int(start_day), int(end_day) + 1):

        if int(str(date)[6: 8]) > 31:
            pass
        else:
            c_info = None
            try:
                c_info = c_price_data[str(date)]
            except Exception as e:
                print(e)

            if c_info is not None:
                high_p = c_info["high_p"]
                low_p = c_info["low_p"]
                start_p = c_info["start_p"]
                end_p = c_info["end_p"]
                amount = c_info["amount"]
                trend = c_info["trend"]

                index = c_info["index"]

                ma = index["ma"]
                ma5 = ma["ma5"]
                ma10 = ma["ma10"]
                ma14 = ma["ma14"]
                ma20 = ma["ma20"]
                ma21 = ma["ma21"]
                ma60 = ma["ma60"]
                ma120 = ma["ma120"]
                ma150 = ma["ma150"]
                ma240 = ma["ma240"]

                boll = index["boll"]
                boll_high = boll["boll_high"]
                boll_mid = boll["boll_mid"]
                boll_low = boll["boll_low"]

                obv_index = index["obv"]
                obv = obv_index["obv"]

                rsi = index["rsi"]
                rsi5 = rsi["rsi5"]
                rsi10 = rsi["rsi10"]
                rsi14 = rsi["rsi14"]
                rsi20 = rsi["rsi20"]

                cd: Candlestick = Candlestick()\
                    .set_price_amount(date, high_p, low_p, start_p, end_p, amount, trend)\
                    .set_ma(ma5, ma10, ma14, ma20, ma21, ma60, ma120, ma150, ma240)\
                    .set_bollinger(boll_high, boll_mid, boll_low)\
                    .set_obv(obv)\
                    .set_rsi(rsi5, rsi10, rsi14, rsi20)

                candlesticks[str(date)] = cd

    return dict(sorted(candlesticks.items()))
