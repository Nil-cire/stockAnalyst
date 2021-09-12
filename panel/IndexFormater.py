from database.TWSEdb import TWSEdb
from database import DbMapper

# db = ""
# collection = ""


def update_ma(stock: str, date: str, country: str = "TWSE"):
    db = DbMapper.db_mapper(date, country)
    listed_dict = ref.get_listed_dict()
    unlisted_dict = ref.get_unlisted_dict()


# li
# 0831