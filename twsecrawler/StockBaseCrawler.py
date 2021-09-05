import requests
import times
from bs4 import BeautifulSoup as bs


class StockBaseCrawler:

    single_stock_url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=ddd&stockNo=nnn"

    @classmethod
    def fetch_stock_data(cls, stock_number: str, from_date: int, to_date: int = None):
        pass

    @classmethod
    def craw_data_from_twse(cls, stock_number: str, date: str) -> str:
        url = cls.single_stock_url.replace("ddd", date).replace("nnn", stock_number)
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        else:
            print("Fail to fetch price data")
            return ""
