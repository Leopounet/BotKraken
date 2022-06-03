from __future__ import annotations
import os
import sys
import time
import traceback

from Structures.KrakenAPI import KrakenAPI
from Structures.AssetHandler import AssetHandler
from Structures.PlayerHandler import PlayerHandler

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

    ph = PlayerHandler(ah, kapi)
    ph.generate_players()

    while True:
        try:
            ph.play()
            for i in range(100):
                time.sleep(1)
                execute_commands()
            time.sleep(20)
        except Exception as e:
            with open("very_bad_error.txt", "a") as file:
                type, value, tr = sys.exc_info()
                file.write(str(e) + "\n")
                file.write(str(type) + "\n")
                file.write(str(value) + "\n")
                file.write(str(tr) + "\n")
                file.write(str(tr.tb_frame) + "\n")
                file.write(str(tr.tb_lasti) + "\n")
                file.write(str(tr.tb_lineno) + "\n\n")

        

