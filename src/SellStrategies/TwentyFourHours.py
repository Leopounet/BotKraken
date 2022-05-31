from Structures.AssetPair import AssetPair
from Structures.Player import Player

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Twenty-four hours."
    description : str = "Sells when it has been 24h."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        date_bought = max(list(player.bought_asset_pair.history.keys()))
        now = max(list(ap.history.keys()))
        if now - date_bought >= 86400:
            return True
        return False