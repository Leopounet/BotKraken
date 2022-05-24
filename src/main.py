from __future__ import annotations
import time
import os
import requests

from typing import Dict, Any, Tuple

from KrakenAPI import KrakenAPI

from DataStructures import Pair, Asset

###############################################################################
############################## VARIABLES ######################################
###############################################################################

# login infos
api_url = "https://api.kraken.com"
api_key = os.environ["API_KEY_KRAKEN"]
api_sec = os.environ["API_SEC_KRAKEN"]

# a line of dashes
dashed = "---------------------------------------------------------------------\
-----------"

# some assets
usd = Asset("usd")
luna = Asset("luna")

# some pairs
usd_luna = Pair(usd, luna)

###############################################################################
############################## CLASSES ########################################
###############################################################################

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

def pretty_printer(obj : Tuple[str, Dict[str, Any]], prepend : str = None, 
                                                     postpend : str = None) -> None:
    name = obj[0]
    dictionary = obj[1]

    if not prepend is None: print(prepend)

    print(name)

    for el in dictionary:
        print(el + ": " + str(dictionary[el]))

    if not postpend is None: print(postpend)

###############################################################################
############################## MAIN ###########################################
###############################################################################

if __name__ == "__main__":
    # creates a new bot
    kapi = KrakenAPI(api_url, api_key, api_sec)

    for i in range(0, 20):
        print(kapi._get_tradable_pairs().json())

    # print(kapi._get_balance().json())
    # print(kapi.get_balance("ZUSD"))
    # print(kapi.get_balance("LUNA"))
    # print(kapi.available_currency_in_balance())

    # get a lot of info
    # pairs = kapi._get_tradable_pairs()
    # assets = kapi._get_assets()
    # ticker = kapi._get_ticker("ZEURZUSD")

    # # get infos
    # pretty_printer(kapi.get_asset("ZEUR", assets), postpend=dashed)
    # pretty_printer(kapi.get_asset("ZUSD", assets), postpend=dashed)
    # pretty_printer(kapi.get_asset("USD", assets), postpend=dashed)

    # pretty_printer(kapi.get_tradable_pair("ZEURZUSD", pairs), postpend=dashed)
    # pretty_printer(kapi.get_tradable_pair("LUNAUSD", pairs), postpend=dashed)

    # print("price of EUR to USD is: " + str(kapi.get_current_price("ZEURZUSD", ticker)))


