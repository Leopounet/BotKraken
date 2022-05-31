from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Five Percent"
    description : str = "Sells when the profit is 5%."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        res = False
        if -(1 - ap.data.current / player.bought_asset_pair.data.current) >= 0.05:
            res = True
        return Strategy.get_all(Strategy.name, player, ap, res)