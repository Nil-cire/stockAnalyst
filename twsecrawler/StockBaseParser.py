from core.Candlestick import Candlestick
from bs4 import BeautifulSoup as bs
from database import mongodb

class StockBaseParser:

    # @classmethod
    # def parse_to_candles(cls, raw_date: str):
    #     bs_data = bs(raw_date, "html.parser").find_all("tr")
    #     for data in bs_data:
    #         try:
    #             data.