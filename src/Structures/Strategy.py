from __future__ import annotations
from typing import Dict, Any, List
import math

from Structures.AssetPair import AssetPair
import Structures.Player as Player

class BuyStrategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = ""
    description : str = ""
    other : Dict[str, List[BuyStrategy]] = {}

    @staticmethod
    def normalize(x : float) -> float:
        if x == None: return 0
        return ((2 / math.pi) * math.atan(x) + 2) / 2

    @staticmethod
    def get_res(s_name : str, ap : AssetPair, res : float) -> float:
        if res == None: return 0
        if not s_name in BuyStrategy.other: return res
        other = BuyStrategy.other[s_name]
        for f in other:
            res = (f.strategy(ap) + res) / 2 if res != None else f.strategy(ap)
        return res

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
        if not s_name in SellStrategy.optional: return True
        optional = SellStrategy.optional[s_name]
        for f in optional:
            if f.strategy(player, ap): return True
        return False

    @staticmethod
    def get_all(s_name : str, player : Player.Player, ap : AssetPair, res : bool) -> bool:
        return (SellStrategy.get_mandatory(s_name, player, ap) and res and 
                (SellStrategy.get_optional(s_name, player, ap)))

    @staticmethod
    def strategy(player : Player.Player, ap : AssetPair)  -> bool:
        pass