from __future__ import annotations
import os, glob, importlib
import time
from typing import List

from Structures.KrakenAPI import KrakenAPI
from Structures.AssetHandler import AssetHandler
from Structures.AssetPair import AssetPair
from Structures.Types import BuyStrategy
from Structures.Player import Player
from Structures.PlayerHandler import PlayerHandler

###############################################################################
############################## VARIABLES ######################################
###############################################################################

# login infos
api_url = "https://api.kraken.com"
api_key = os.environ["API_KEY_KRAKEN"]
api_sec = os.environ["API_SEC_KRAKEN"]

# strategies directory
buy_strategies_dir = "BuyStrategies"
sell_strategies_dir = "SellStrategies"

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

    ph = PlayerHandler(ah, kapi)
    ph.generate_players()

    while True:
        ph.play()
        input("")

        

