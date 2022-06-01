from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from SellStrategies.TwentyFourHours import Strategy as TFH
from SellStrategies.TenPercent import Strategy as TP

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Twenty-four hours or ten percent"
    description : str = "Sells when the profit is 10% or it has been 24h."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        Strategy.mandatory[Strategy.name] = [TFH, TP]
        return Strategy.get_all(Strategy.name, player, ap, True)