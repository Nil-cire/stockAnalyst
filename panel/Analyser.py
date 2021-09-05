from database.TWSEdb import TWSEdb
from twsecrawler import ref, StockBaseCrawler


def add_new_listed_stock_to_db():
    listed_dict = ref.get_listed_stocks_info()

    db = TWSEdb("stock_twse", 'basePrice')

    for (key, value) in listed_dict.items:
        if len(key) < 5:
            try:
                db.add_stock_info(key, value[1], "TWSE", value[3], value[4], value[2], "NTD", 2)
            except Exception as e:
                print(e)


