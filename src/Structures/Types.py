from typing import Callable

from Structures.AssetPair import AssetPair
import Structures.Player as Player

BuyStrategy = Callable[[AssetPair], float]
SellStrategy = Callable[[Player.Player, AssetPair], bool]