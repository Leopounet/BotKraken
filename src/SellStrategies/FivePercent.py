import random

from Structures.AssetPair import AssetPair
from Structures.Player import Player

###############################################################################
############################ STRATEGY #########################################
###############################################################################

def strategy(player : Player, ap : AssetPair) -> float:
    if -(1 - ap.data.current / player.bought_asset_pair.data.current) >= 0.05:
        return True
    return False