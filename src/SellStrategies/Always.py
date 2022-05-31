from Structures.AssetPair import AssetPair
from Structures.Player import Player

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Always"
    description : str = "Always sells."

    @staticmethod
    def strategy(player : Player, ap : AssetPair) -> float:
        return True