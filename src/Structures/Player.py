from __future__ import annotations

from datetime import datetime

import Structures.Types as Types
from Structures.AssetPair import AssetPair
import Structures.AssetHandler as AH
from Structures.Color import Color, random_color

class Player:

    """
    This class represents a Player that is able 
    to sell and buy.
    """

    result_dir = "Results/"

    def __init__(self : Player, bs : Types.BuyStrategy, ss : Types.SellStrategy, name : str) -> Player:
        """
        Creates a new player.

        :param bs: The BuyStrategy to use.
        :param ss: The SellStrategy to use.
        """
        self.bs : Types.BuyStrategy = bs
        self.ss : Types.SellStrategy = ss
        self.name : str = name
        self.bought_asset_pair : AssetPair | None = None
        self.color = random_color()
        self.log_file : str = Player.result_dir + self.name + ".res"
        self.detailed_log_file : str = Player.result_dir + self.name + "_detailed.res"

    def buy_asset(self : Player, ah : AH.AssetHandler) -> None:
        """
        Buys a new asset.

        :param ah: The AssetHandler to use as a reference.
        """
        ap = ah.get_best_usd_pair(self.bs)
        self.bought_asset_pair = ap.copy()

        # print(f"{self.color.value}Player {self.name} has bought")
        # print(self.bought_asset_pair)
        # print(f"{Color.DEFAULT.value}")

        with open(self.log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] BUY\n")
            file.write(self.name + " has bought " + self.bought_asset_pair.base.name)
            file.write(" for $" + str(self.bought_asset_pair.data.current) + "\n")

        with open(self.detailed_log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] BUY\n")
            file.write(self.name + " has bought: ")
            file.write(str(self.bought_asset_pair) + "\n\n")
            file.write("---------------------------------------------------------------------------\n")

    def should_sell(self : Player, ah : AH.AssetHandler) -> None:
        """
        Check whether the currently held asset should be sold.

        :param ah: The AssetHandler to use as a reference.
        """
        return self.ss(self, ah.pairs[self.bought_asset_pair.name])

    def sell_asset(self : Player, ah : AH.AssetHandler) -> None:
        """
        Sells the current asset.

        :param ah: The AssetHandler to use as a reference.
        """
        # print(f"{self.color.value}Player {self.name} has sold")
        # print(ah.pairs[self.bought_asset_pair.name])
        # print(f"{Color.DEFAULT.value}")

        profit = ah.pairs[self.bought_asset_pair.name].data.current / self.bought_asset_pair.data.current
        profit = - (1 - profit)

        with open(self.log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] SOLD\n")
            file.write(self.name + " has sold " + self.bought_asset_pair.base.name)
            file.write(" for $" + str(self.bought_asset_pair.data.current))
            file.write(". Profit was " + str(profit) + "%.\n")

        with open(self.detailed_log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] SOLD\n")
            file.write(self.name + " has sold: ")
            file.write(str(self.bought_asset_pair) + "\n")
            file.write("Profit was " + str(profit) + "%.\n")
            file.write("---------------------------------------------------------------------------\n")

        self.bought_asset_pair = None
        
