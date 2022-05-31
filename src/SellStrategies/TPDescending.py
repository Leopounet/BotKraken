from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from SellStrategies.TenPercent import Strategy as TenPercent

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Ten percent decreasing."
    description : str = "Sells when the profit is 10% and the price is decreasing."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        Strategy.mandatory[Strategy.name] = [TenPercent]
        res = ap.data.is_falling
        return Strategy.get_all(Strategy.name, player, ap, res)