import PriceUpdater
from database import DbMapper
from twsecrawler import ref
from panel.IndexFormater import IndexUpdater


class DailyTask:
    @staticmethod
    def update_price(date):
        PriceUpdater.twse_daily_price_update(date)

    @staticmethod
    def update_index(date: str):
        db = DbMapper.db_mapper(date)
        listed_dict = ref.get_listed_dict()0
        unlisted_dict = ref.get_unlisted_dict()

        for stock_no in listed_dict.keys():
            if stock_no == "3008" or stock_no == "5269" or stock_no == "6409" or stock_no == "6415":
                continue
            index_formatter = IndexUpdater()
            db.update_index(stock_no, date, index_formatter.get_single_stock_index_data(stock_no, date))

        for stock_no in unlisted_dict.keys():
            if stock_no == "4966" or stock_no == "5274":
                continue
            index_formatter = IndexUpdater()
            db.update_index(stock_no, date, index_formatter.get_single_stock_index_data(stock_no, date))
