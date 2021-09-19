from twsecrawler import ref
from panel import Basic
from stockfilter import ObvFilter, BollingFilter, RsiFilter

listed_stocks = ref.get_listed_dict()
unlisted_stocks = ref.get_unlisted_dict()
dates_2021: list = ref.get_2021_dates()


def match_deviate(check_date: str, interval: int = 14):
    match_list = []

    obv_list = filter_obv(check_date, interval)
    rsi_list = filter_rsi(check_date, interval)
    boll_list = filter_bollinger(check_date)

    temp_list = []

    for stock_no in rsi_list:
        if stock_no in obv_list:
            temp_list.append(stock_no)

    for stock_no in boll_list:
        if stock_no in temp_list:
            match_list.append(stock_no)

    return match_list


def filter_obv(check_date: str, interval: int = 14) -> list:

    obv_list = []

    start_date = "20210101"
    try:
        index = dates_2021.index(check_date)
        start_date = dates_2021[(index - interval)]
    except Exception as e:
        print(f'Bad request when filtering obv by date = {check_date}, interval = {interval}')
        print(e)

    for stock_no in listed_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if ObvFilter.is_obv_deviate(cds, interval, check_date):
                obv_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if ObvFilter.is_obv_deviate(cds, interval, check_date):
                obv_list.append(str(stock_no))
        except Exception as e:
            print(e)

    return obv_list


def filter_rsi(check_date: str, interval: int = 14) -> list:

    rsi_list = []

    start_date = "20210101"
    try:
        index = dates_2021.index(check_date)
        start_date = dates_2021[(index - interval)]
    except Exception as e:
        print(f'Bad request when filtering obv by date = {check_date}, interval = {interval}')
        print(e)

    for stock_no in listed_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if RsiFilter.is_rsi_deviate(cds, interval, check_date):
                rsi_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if RsiFilter.is_rsi_deviate(cds, interval, check_date):
                rsi_list.append(str(stock_no))
        except Exception as e:
            print(e)

    return rsi_list


def filter_bollinger(check_date: str) -> list:
    boll_list = []
    #
    # start_date = "20210101"
    # try:
    #     index = dates_2021.index(check_date)
    #     start_date = dates_2021[(index - interval)]
    # except Exception as e:
    #     print(f'Bad request when filtering obv by date = {check_date}, interval = {interval}')
    #     print(e)

    for stock_no in listed_stocks.keys():
        try:
            if BollingFilter.is_bollinger_deviate(check_date, str(stock_no)):
                boll_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():
        try:
            if BollingFilter.is_bollinger_deviate(check_date, str(stock_no)):
                boll_list.append(str(stock_no))
        except Exception as e:
            print(e)

    return boll_list
