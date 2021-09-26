from database import DbMapper
from twsecrawler import ref
from panel import Basic
from stockfilter import ObvFilter, BollingFilter, RsiFilter, CandlestickChart

listed_stocks = ref.get_listed_dict()
unlisted_stocks = ref.get_unlisted_dict()
dates_2021: list = ref.get_2021_dates()


class Analyst:
    obv_list = []
    rsi_list = []
    boll_list = []
    ma_list = []
    ma_r_list = []
    max_volume_list = []
    m_star_list = []
    e_star_list = []

    date = None

    db = None

    def __init__(self, date: str):
        self.date = date
        self.db = DbMapper.db_mapper(date)

    def prepare_lists(self, check_date: str, interval: int = 14):
        self.obv_list = filter_obv(check_date, interval)
        self.rsi_list = filter_rsi14(check_date, interval)
        self.boll_list = filter_bollinger(check_date)
        self.ma_list = filter_ma_close(check_date, 0.0025, "s")
        self.ma_r_list = filter_ma_close(check_date, 0.0025, "r")
        self.max_volume_list = filter_max_volume(check_date)
        self.m_star_list = filter_is_morning_star(check_date)
        self.e_star_list = filter_is_evening_star(check_date)

    def match_obv_rsi(self):
        match_list = []

        for stock_no in self.rsi_list:
            if stock_no in self.obv_list:
                match_list.append(stock_no)

        return match_list

    def get_deviate_set_with_volume(self) -> list:
        li = []
        tmp = []

        for stock_no in self.rsi_list:
            if stock_no in self.obv_list:
                tmp.append(stock_no)

        for stock_no in self.max_volume_list:
            if stock_no in tmp:
                li.append(stock_no)

        return li

    def match_all(self):
        match_list = []
        temp_list = []

        for stock_no in self.rsi_list:
            if stock_no in self.obv_list:
                temp_list.append(stock_no)

        for stock_no in self.boll_list:
            if stock_no in temp_list:
                match_list.append(stock_no)

        return match_list


def match_all_deviate(check_date: str, interval: int = 14):
    match_list = []

    obv_list = filter_obv(check_date, interval)
    rsi_list = filter_rsi14(check_date, interval)
    boll_list = filter_bollinger(check_date)

    temp_list = []

    for stock_no in rsi_list:
        if stock_no in obv_list:
            temp_list.append(stock_no)

    for stock_no in boll_list:
        if stock_no in temp_list:
            match_list.append(stock_no)

    return match_list


def match_rsi_obv_deviate(check_date: str, interval: int = 14):
    match_list = []

    obv_list = filter_obv(check_date, interval)
    rsi_list = filter_rsi14(check_date, interval)

    for stock_no in rsi_list:
        if stock_no in obv_list:
            match_list.append(stock_no)

    return match_list


def filter_max_volume(check_date: str, interval: int = 14):

    max_volume_list = []

    for stock_no in listed_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, check_date[0: 4] + "0101", check_date)
            index = len(cds)
            dates = list(cds)
            max_volume = 0

            for i in range((index - interval), index - 1):
                volume = cds[dates[i]].amount
                if volume > max_volume:
                    max_volume = volume

            volume_today = cds[dates[index - 1]].amount
            if volume_today > max_volume:
                max_volume_list.append(stock_no)

        except Exception as e:
            print(f'!!! Fail to get volume data for stock = {stock_no}, on date = {check_date}')
            print(e)

    for stock_no in unlisted_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, check_date[0: 4] + "0101", check_date)
            index = len(cds)
            dates = list(cds)
            max_volume = 0

            for i in range((index - interval), index - 1):
                volume = cds[dates[i]].amount
                if volume > max_volume:
                    max_volume = volume

            volume_today = cds[dates[index - 1]].amount
            if volume_today > max_volume:
                max_volume_list.append(stock_no)

        except Exception as e:
            print(f'!!! Fail to get volume data for stock = {stock_no}, on date = {check_date}')
            print(e)

    return max_volume_list


def filter_ma_close(check_date: str, cv_standard: float = 0.0025, model: str = "s"):

    ma_list = []

    for stock_no in listed_stocks.keys():
        try:
            date_data = Basic.get_single_day_data(stock_no, check_date)
            ma_data = date_data["index"]["ma"]
            ma5 = ma_data["ma5"]
            ma10 = ma_data["ma10"]
            ma20 = ma_data["ma20"]

            if model == "s":
                if ma5 < ma10 < ma20:

                    temp_list = [ma5, ma10, ma20]

                    cv = cal_cv(temp_list)
                    print(stock_no)
                    print(cv)

                    if cv < cv_standard:
                        ma_list.append(stock_no)

            if model == "r":
                if ma5 > ma10 > ma20:

                    temp_list = [ma5, ma10, ma20]

                    cv = cal_cv(temp_list)
                    print(stock_no)
                    print(cv)

                    if cv < cv_standard:
                        ma_list.append(stock_no)

        except Exception as e:
            print(f'!!! Fail to get ma data for stock = {stock_no}, on date = {check_date}')
            print(e)

    for stock_no in unlisted_stocks.keys():
        try:
            date_data = Basic.get_single_day_data(stock_no, check_date)
            ma_data = date_data["index"]["ma"]
            ma5 = ma_data["ma5"]
            ma10 = ma_data["ma10"]
            ma20 = ma_data["ma20"]

            if model == "s":
                if ma5 < ma10 < ma20:

                    temp_list = [ma5, ma10, ma20]

                    cv = cal_cv(temp_list)
                    print(stock_no)
                    print(cv)

                    if cv < cv_standard:
                        ma_list.append(stock_no)

            if model == "r":
                if ma5 > ma10 > ma20:

                    temp_list = [ma5, ma10, ma20]

                    cv = cal_cv(temp_list)
                    print(stock_no)
                    print(cv)

                    if cv < cv_standard:
                        ma_list.append(stock_no)
        except Exception as e:
            print(f'!!! Fail to get ma data for stock = {stock_no}, on date = {check_date}')
            print(e)

    return ma_list


def cal_stdev(data: list):
    list_sum = 0
    for i in data:
        list_sum += i

    counts = len(data)
    mean = list_sum / counts

    square_sum = 0
    for i in data:
        square_sum += ((i - mean) ** 2)

    return round((square_sum / counts) ** 0.5, 2)


def cal_cv(data: list):
    list_sum = 0
    for i in data:
        list_sum += i

    counts = len(data)
    mean = list_sum / counts

    square_sum = 0
    for i in data:
        square_sum += ((i - mean) ** 2)

    stdev = (square_sum / counts) ** 0.5

    return round((stdev / mean), 5)


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

            if ObvFilter.is_obv_deviate(cds, interval, check_date, 500, 12):
                obv_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if ObvFilter.is_obv_deviate(cds, interval, check_date, 500, 12):
                obv_list.append(str(stock_no))
        except Exception as e:
            print(e)

    return obv_list


def filter_rsi14(check_date: str, interval: int = 14) -> list:

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

            if RsiFilter.is_rsi14_deviate(cds, interval, check_date, 500, 12):
                rsi_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if RsiFilter.is_rsi14_deviate(cds, interval, check_date, 500, 12):
                rsi_list.append(str(stock_no))
        except Exception as e:
            print(e)

    return rsi_list


def filter_rsi5(check_date: str, interval: int = 14) -> list:

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

            if RsiFilter.is_rsi5_deviate(cds, interval, check_date, 500, 12):
                rsi_list.append(str(stock_no))
        except Exception as e:
            print(e)

    for stock_no in unlisted_stocks.keys():

        print(stock_no)

        try:
            cds = Basic.get_candlesticks(str(stock_no), start_date, check_date)

            if RsiFilter.is_rsi5_deviate(cds, interval, check_date, 500, 12):
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


def filter_is_morning_star(check_date: str) -> list:
    ms_list = []

    start_day = check_date[0: 4] + "0101"

    for stock_no in listed_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_morning_star(cds):
                ms_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check morning star, cause = {e}')

    for stock_no in unlisted_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            print(stock_no)
            if CandlestickChart.is_morning_star(cds):
                ms_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check morning star, cause = {e}')

    return ms_list


def filter_is_evening_star(check_date: str) -> list:
    es_list = []

    start_day = check_date[0: 4] + "0101"

    for stock_no in listed_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_evening_star(cds):
                es_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check evening star, cause = {e}')

    for stock_no in unlisted_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_evening_star(cds):
                es_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check evening star, cause = {e}')

    return es_list


def filter_is_bull_flag(check_date: str) -> list:
    bf_list = []

    start_day = check_date[0: 4] + "0101"

    for stock_no in listed_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_bull_flag(cds):
                bf_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check is_bull_flag, cause = {e}')

    for stock_no in unlisted_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_bull_flag(cds):
                bf_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check is_bull_flag, cause = {e}')

    return bf_list


def filter_is_bear_flag(check_date: str) -> list:
    bear_f_list = []

    start_day = check_date[0: 4] + "0101"

    for stock_no in listed_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_bear_flag(cds):
                bear_f_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check is_bull_flag, cause = {e}')

    for stock_no in unlisted_stocks.keys():
        try:
            cds = Basic.get_candlesticks(stock_no, start_day, check_date)
            if CandlestickChart.is_bear_flag(cds):
                bear_f_list.append(str(stock_no))
        except Exception as e:
            print(f'!!! Fail to check is_bull_flag, cause = {e}')

    return bear_f_list
