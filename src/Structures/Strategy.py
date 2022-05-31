from __future__ import annotations
from typing import Dict, Any, List
import math

from Structures.AssetPair import AssetPair
import Structures.Player as Player

class BuyStrategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = ""
    description : str = ""

    @staticmethod
    def normalize(x : float) -> float:
        return ((2 / math.pi) * math.atan(x) + 2) / 2

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        pass

class SellStrategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = ""
    description : str = ""
    mandatory : Dict[str, List[SellStrategy]] = {}
    optional : Dict[str, List[SellStrategy]] = {}

    @staticmethod
    def get_mandatory(s_name : str, player : Player.Player, ap : AssetPair) -> bool:
        if not s_name in SellStrategy.mandatory: return True
        mandatory = SellStrategy.mandatory[s_name]
        for f in mandatory:
            if not f.strategy(player, ap): return False
        return True

    @staticmethod
    def get_optional(s_name : str, player : Player.Player, ap : AssetPair) -> bool:
        if not s_name in SellStrategy.optional: return False
        optional = SellStrategy.optional[s_name]
        for f in optional:
            if not f.strategy(player, ap): return True
        return False

    @staticmethod
    def get_all(s_name : str, player : Player.Player, ap : AssetPair, res : bool) -> bool:
        return (SellStrategy.get_mandatory(s_name, player, ap) and 
                (SellStrategy.get_optional(s_name, player, ap) or res))

    @staticmethod
    def strategy(player : Player.Player, ap : AssetPair)  -> bool:
        pass