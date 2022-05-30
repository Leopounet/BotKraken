import random

from Structures.AssetPair import AssetPair
from Structures.Player import Player

###############################################################################
############################ STRATEGY #########################################
###############################################################################

def strategy(player : Player, ap : AssetPair) -> float:
    date_bought = max(list(player.bought_asset_pair.history.keys()))
    now = max(list(ap.history.keys()))
    if now - date_bought >= 86400:
        return True
    return False