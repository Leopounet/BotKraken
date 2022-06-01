from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Twenty-four hours"
    description : str = "Sells when it has been 24h."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        res = False
        date_bought = max(list(player.bought_asset_pair.history.keys()))
        now = max(list(ap.history.keys()))
        if now - date_bought >= 86400:
            res = True
        return Strategy.get_all(Strategy.name, player, ap, res)