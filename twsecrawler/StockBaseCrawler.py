import requests
import times
from bs4 import BeautifulSoup as bs


class StockBaseCrawler:

    single_stock_url_listed = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=ddd&stockNo=nnn"
    single_stock_url_unlisted = "https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_print.php?l=zh-tw&d=YYY/MM&stkno=NNNN&s=0,asc,0"

    @classmethod
    def fetch_stock_data(cls, stock_number: str, from_date: int, to_date: int = None):
        pass

    # listed_stocks
    @classmethod
    def craw_data_from_twse(cls, stock_number: str, date: str) -> str:
        url = cls.single_stock_url_listed.replace("ddd", date).replace("nnn", stock_number)
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        else:
            print("Fail to fetch price data")
            return ""

    # unlisted_stocks
    @classmethod
    def craw_data_from_tpex(cls, stock_number: str, date: str) -> str:
        year = str(int(date[0: 4]) - 1911)
        month = date[4: 6]
        url = cls.single_stock_url_unlisted.replace("YYY", year).replace("MM", month).replace("NNNN", stock_number)
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        else:
            print("Fail to fetch price data")
            return ""
