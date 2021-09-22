import requests

from database.TWSEdb import TWSEdb
from twsecrawler import ref
from twsecrawler.StockBaseCrawler import StockBaseCrawler
from bs4 import BeautifulSoup as bs
import time

update_interval = 7


def add_new_listed_stock_to_db():
    listed_dict = ref.get_listed_stocks_info()

    db = TWSEdb("stock_twse", "basePrice")

    for (key, value) in listed_dict.items():
        if len(key) < 5:
            try:
                db.add_stock_info(key, value[1], "TWSE", value[3], value[2], value[4], "NTD", 2)
            except Exception as e:
                print(e)


def add_new_unlisted_stock_to_db():
    listed_dict = ref.get_unlisted_stocks_info()
    count = 0
    db = TWSEdb("stock_twse", "basePrice")

    for (key, value) in listed_dict.items():
        if len(key) < 5:
            try:
                count += 1
                db.add_stock_info(key, value[1], "TWSE", value[3], value[2], value[4], "NTD", 2)
            except Exception as e:
                print(e)

    print(f'Done add {count} stocks')


def update_single_stock_price_by_month(stock_no: str, date: str, db: TWSEdb = None, add_or_update: str = "update"):
    count = 0
    if TWSEdb is None:
        db = TWSEdb("stock_twse", "basePrice")
    res = StockBaseCrawler.craw_data_from_twse(stock_no, date)
    if res != "":
        b_data = bs(res, "html.parser")
        big_data = b_data.find_all("tbody")[0]
        data = big_data.find_all("tr")

        for d in data:
            try:
                count += 1
                detail = d.find_all("td")
                format_string = detail[0].text.replace("/", "")
                new_date = str(int(format_string[0: 3]) + 1911) + format_string[3:7]
                high_p = detail[4].text
                low_p = detail[5].text
                start_p = detail[3].text
                end_p = detail[6].text
                amount = detail[1].text.replace(",", "")

                if add_or_update == "add":
                    db.add_price_data(int(stock_no), new_date, float(high_p), float(low_p), float(start_p), float(end_p), int(amount))
                if add_or_update == "update":
                    db.update_price_data(int(stock_no), new_date, float(high_p), float(low_p), float(start_p), float(end_p), int(amount))
            except Exception as e:
                    print(e)

    print(f'Done update {count} stocks')


def update_single_unlisted_stock_price_by_month(stock_no: str, date: str, db: TWSEdb = None, add_or_update: str = "update"):
    count = 0
    if TWSEdb is None:
        db = TWSEdb("stock_twse", "basePrice")
    res = StockBaseCrawler.craw_data_from_tpex(stock_no, date)
    if res != "":
        b_data = bs(res, "html.parser")
        big_data = b_data.find_all("tbody")[0]
        data = big_data.find_all("tr")

        for d in data:
            try:
                count += 1
                detail = d.find_all("td")
                format_string = detail[0].text.replace("/", "")
                new_date = str(int(format_string[0: 3]) + 1911) + format_string[3:7]
                high_p = detail[4].text
                low_p = detail[5].text
                start_p = detail[3].text
                end_p = detail[6].text
                amount = int(detail[1].text.replace(",", "")) * 1000

                if add_or_update == "add":
                    db.add_price_data(int(stock_no), new_date, float(high_p), float(low_p), float(start_p), float(end_p), int(amount))
                if add_or_update == "update":
                    db.update_price_data(int(stock_no), new_date, float(high_p), float(low_p), float(start_p), float(end_p), int(amount))
            except Exception as e:
                print(e)

    print(f'Done update {count} stocks')


# main function
def update_all_listed_stock_price_by_month(date: str):
    listed_dict = ref.get_listed_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in listed_dict:
        if len(key) < 5:
            try:
                time.sleep(update_interval)
                update_single_stock_price_by_month(str(key), date, db, "update")
            except Exception as e:
                print(e)


# main function
def update_all_unlisted_stock_price_by_month(date: str):
    unlisted_dict = ref.get_unlisted_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in unlisted_dict:
        if len(key) < 5:
            try:
                time.sleep(update_interval)
                update_single_unlisted_stock_price_by_month(str(key), date, db, "update")
            except Exception as e:
                print(e)


# main function
def add_all_new_listed_stock_price_by_month(date: str):
    listed_dict = ref.get_listed_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in listed_dict:
        if len(key) < 5:
            try:
                time.sleep(update_interval)
                update_single_stock_price_by_month(str(key), date, db, "add")
            except Exception as e:
                print(e)


# main function
def add_all_new_unlisted_stock_price_by_month(date: str):
    unlisted_dict = ref.get_unlisted_dict()

    db = TWSEdb("stock_twse", "basePrice")

    # update_single_stock_price_by_month("2603", str(date), db)
    for key in unlisted_dict:
        if len(key) < 5:
            try:
                time.sleep(update_interval)
                update_single_stock_price_by_month(str(key), date, db, "add")
            except Exception as e:
                print(e)


daily_stock_url = "https://histock.tw/stock/rank.aspx?m=0&d=0&p=all"
# <table>
#     <tr>
#         <td>0051</td>
#         <td><a href='/stock/0051' target="_blank">元大中型100</a></td>
#         <td><span id="CPHB1_gv_lbDeal_1" class="price-up">57.1</span></td>
#         <td><span id="CPHB1_gv_lbChange_1" class="price-up">▲0.70</span></td>
#         <td><span id="CPHB1_gv_lbPercentage_1" class="price-up">+1.24%</span></td>
#         <td><span id="CPHB1_gv_lbWeekChange_1" class="price-down">-0.26%</span></td>
#         <td>0.44%</td><td>56.9</td>
#         <td><span id="CPHB1_gv_lbHigh_1">57.1</span></td>
#         <td><span id="CPHB1_gv_lbLow_1">56.85</span></td>
#         <td>56.4</td>
#         <td>21</td>
#         <td>0.012</td>
#     </tr>
# </table>
def twse_daily_price_update(date: str):
    db = TWSEdb("stock_twse", "basePrice")

    res = requests.get(daily_stock_url)
    if (res.status_code != 200):
        print(f'Fail to update twse_daily_price, status_code = {res.status_code}')
        return

    b_data = bs(res.text, "html.parser")
    b_table = b_data.find_all("table")
    b_tr = b_table[0].find_all("tr")

    count = 0
    c_total = 0

    for i in range(1, len(b_tr)):

        c_total += 1

        try:

            d = b_tr[i]
            detail = d.find_all("td")
            stock_no = detail[0].text
            high_p = detail[8].text
            low_p = detail[9].text
            start_p = detail[7].text
            end_p = detail[2].text
            amount = int(detail[11].text.replace(",", "")) * 1000

            if db.is_id_exist(stock_no):
                db.add_price_data(int(stock_no), str(date), float(high_p), float(low_p), float(start_p), float(end_p),
                                  int(amount))
                count += 1

        except Exception as e:
            print(e)

    print(f'Success update {count} items / Total {c_total}')


# listed
# 202101
# 202102
# 202103
# 202104
# 202105
# 202106
# 202107
# 202108
# 20210918

# unlisted
# 202108
# 202101
# 202102
# 202103
# 202104
# 202105
# 202105
# 202106
# 202107
# 202108
# 20210918






#5202 525