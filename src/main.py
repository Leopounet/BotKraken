from __future__ import annotations
import time
import os
from injector import K
import requests

from KrakenAPI import KrakenAPI

###############################################################################
############################## VARIABLES ######################################
###############################################################################

# login infos
api_url = "https://api.kraken.com"
api_key = os.environ["API_KEY_KRAKEN"]
api_sec = os.environ["API_SEC_KRAKEN"]

###############################################################################
############################## CLASSES ########################################
###############################################################################

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

###############################################################################
############################## MAIN ###########################################
###############################################################################

if __name__ == "__main__":
    # creates a new bot
    kapi = KrakenAPI(api_url, api_key, api_sec)

    print(kapi._get_balance().json())
    print(kapi.get_balance("ZUSD"))
    print(kapi.get_balance("LUNA"))
    print(kapi.available_currency_in_balance())
