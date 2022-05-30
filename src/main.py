from __future__ import annotations
import os, glob, importlib
from typing import Callable

from Structures.KrakenAPI import KrakenAPI
from Structures.AssetHandler import AssetHandler
from Structures.AssetPair import AssetPair

###############################################################################
############################## VARIABLES ######################################
###############################################################################

# login infos
api_url = "https://api.kraken.com"
api_key = os.environ["API_KEY_KRAKEN"]
api_sec = os.environ["API_SEC_KRAKEN"]

# strategies directory
buy_strategies_dir = "BuyStrategies"

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
    ah.update_tradable_assets(kapi)
    ah.update_usd_tradable_prices(kapi, pair="LUNAUSD")

    buy_strategies = set(glob.glob(buy_strategies_dir + "/*.py"))
    init_files = set(glob.glob(buy_strategies_dir + "/__init__.py"))
    buy_strategies = buy_strategies.difference(init_files)

    for strategy in buy_strategies:
        package_name = buy_strategies_dir + "."
        module_name = strategy.split("/")[-1].split(".")[0]
        strategy : Callable[[AssetPair], float] = importlib.import_module(package_name + module_name).strategy

        print("Asset yielded by " + module_name + " strategy:\n")
        print(ah.get_best_usd_pair(strategy))
        print("------------------------------------------------------------------")

