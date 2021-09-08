import requests
from bs4 import BeautifulSoup as bs
import pymongo

listed_stock_number_url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
unlisted_stock_number_url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"



# b_data.find_all("td")
# b2 = b_data[1]
# b = b2.find_all("td")
# b3 = b[2: len(b)]

full_listed_list = {}
full_unlisted_list = {}

#  { "2603": [number, name, start_date, listed_state, industry], ... }


def get_listed_stocks_info() -> dict:
    res = requests.get(listed_stock_number_url)
    b_data = bs(res.text, "html.parser")
    b_data_stock = b_data.find_all("table")[1]
    b_data_stock_clean = b_data_stock.find_all("tr")
    b_final = b_data_stock_clean[2: len(b_data_stock_clean)]
    for d in b_final:
        try:
            data = d.find_all("td")
            number_list = data[0].text.split("\u3000")
            number = number_list[0]
            name = number_list[1]
            start_date = data[2].text.replace("/", "")
            listed_state = data[3].text
            industry = data[4].text

            info_list = [number, name, start_date, listed_state, industry]

            full_listed_list[number] = info_list
        except Exception as e:
            print(d)
            print(e)

    return full_listed_list


def get_unlisted_stocks_info() -> dict:
    res = requests.get(unlisted_stock_number_url)
    b_data = bs(res.text, "html.parser")
    b_data_stock = b_data.find_all("table")[1]
    b_data_stock_clean = b_data_stock.find_all("tr")
    b_final = b_data_stock_clean[2: len(b_data_stock_clean)]
    for d in b_final:
        try:
            data = d.find_all("td")
            number_list = data[0].text.split("\u3000")
            number = number_list[0]
            name = number_list[1]
            start_date = data[2].text.replace("/", "")
            listed_state = data[3].text
            industry = data[4].text

            info_list = [number, name, start_date, listed_state, industry]

            full_unlisted_list[number] = info_list
        except Exception as e:
            print(d)
            print(e)

    return full_unlisted_list


def get_listed_dict() -> dict:
    my_client1 = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db1 = my_client1["stock_twse"]
    my_col1 = my_db1["listed_stocks"]
    data = my_col1.find_one({})

    return data["stocks"]


def get_unlisted_dict() -> dict:
    my_client1 = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db1 = my_client1["stock_twse"]
    my_col1 = my_db1["unlisted_stocks"]
    data = my_col1.find_one({})
    return data["stocks"]

# get_listed_stocks_info()
# print(full_listed_list)


# <tr>
#   <td bgcolor="#FAFAD2">
#    1101　台泥
#   </td>
#   <td bgcolor="#FAFAD2">
#    TW0001101004
#   </td>
#   <td bgcolor="#FAFAD2">
#    1962/02/09
#   </td>
#   <td bgcolor="#FAFAD2">
#    上市
#   </td>
#   <td bgcolor="#FAFAD2">
#    水泥工業
#   </td>
#   <td bgcolor="#FAFAD2">
#    ESVUFR
#   </td>
#   <td bgcolor="#FAFAD2">
#   </td>
#  </tr>
#  <tr>

