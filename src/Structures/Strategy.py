from typing import Dict, Any

from Structures.AssetPair import AssetPair
import Structures.Player as Player

class BuyStrategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = ""
    description : str = ""

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        pass

class SellStrategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = ""
    description : str = ""

    @staticmethod
    def strategy(player : Player.Player, ap : AssetPair)  -> float:
        pass