import random

from Structures.AssetPair import AssetPair
from Structures.Player import Player
from Structures.Strategy import SellStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(SellStrategy):

    name : str = "Random"
    description : str = "Random."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        res = random.random() >= 0.5
        return Strategy.get_all(Strategy.name, player, ap, res)