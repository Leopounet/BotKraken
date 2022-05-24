from __future__ import annotations
import os, time

from KrakenAPI import KrakenAPI

from Asset import AssetHandler
from Error import Error

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

    ah = AssetHandler()
    ah.update_assets(kapi)

    x = time.time()
    calls = 0

    for asset in ah.assets:
        print(calls)
        calls += 1
        result = kapi.public_kraken_request("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
        if isinstance(result, Error):
            print(result.error.value)
            exit(0)
        print(result)

    print(time.time() - x)
    

    # for i in range(0, 20):
    #     print(kapi._get_tradable_pairs().json())

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


