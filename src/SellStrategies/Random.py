import random

from Structures.AssetPair import AssetPair
from Structures.Player import Player

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Random"
    description : str = "Random."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        return random.random() >= 0.5