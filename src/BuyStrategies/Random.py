import random

from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Random"
    description : str = "Random."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        return Strategy.normalize(random.random())