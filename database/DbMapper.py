from .TWSEdb import TWSEdb


def db_mapper(date: str, country: str = "TWSE"):
    db_name = ""
    db_collection = ""

    if country == "TWSE":
        db_name = "stock_twse"

    if date[0: 4] == "2021":
        db_collection = "basePrice"

    if db_name is not "" and db_collection is not "":
        return TWSEdb(db_name, db_collection)
