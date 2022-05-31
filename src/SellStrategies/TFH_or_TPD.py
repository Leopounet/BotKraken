from Structures.AssetPair import AssetPair
from Structures.Player import Player

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Twenty-four hours or ten percent decreasing."
    description : str = "Sells when the profit is 10% and the \
price is decreasing or it has been 24h."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        date_bought = max(list(player.bought_asset_pair.history.keys()))
        now = max(list(ap.history.keys()))
        if now - date_bought >= 86400:
            return True

        if -(1 - ap.data.current / player.bought_asset_pair.data.current) >= 0.10:
            if ap.data.is_falling:
                return True
        return False