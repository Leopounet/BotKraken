from Structures.AssetPair import AssetPair
from Structures.Player import Player

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Five Percent"
    description : str = "Sells when the profit is 5%."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        if -(1 - ap.data.current / player.bought_asset_pair.data.current) >= 0.05:
            return True
        return False