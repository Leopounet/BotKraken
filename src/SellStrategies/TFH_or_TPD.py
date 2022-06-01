from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from SellStrategies.TwentyFourHours import Strategy as TFH
from SellStrategies.TPDescending import Strategy as TPD

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Twenty-four hours or ten percent decreasing"
    description : str = "Sells when the profit is 10% and the \
price is decreasing or it has been 24h."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        Strategy.mandatory[Strategy.name] = [TFH, TPD]
        return Strategy.get_all(Strategy.name, player, ap, True)