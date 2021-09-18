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

                cd = Candlestick().set_price_amount(date, high_p, low_p, start_p, end_p, amount, trend)

                candlesticks[str(date)] = cd

    return dict(sorted(candlesticks.items()))
