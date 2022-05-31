from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Never"
    description : str = "Never sells."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        return Strategy.get_all(Strategy.name, player, ap, False)