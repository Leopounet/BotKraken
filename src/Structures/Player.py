from __future__ import annotations

from typing import Type

from datetime import datetime

from Structures.AssetPair import AssetPair
import Structures.AssetHandler as AH
from Structures.Color import Color, random_color
import Structures.Strategy as Strategy

from Utils.StringManipulation import tabulate

class Player:

    """
    This class represents a Player that is able 
    to sell and buy.
    """

    result_dir = "Results/Classic/"
    detailed_result_dir = "Results/Detailed/"
    brief_result_dir = "Results/Brief/"

    def __init__(self : Player, bs : Type[Strategy.BuyStrategy], ss : Type[Strategy.SellStrategy]) -> Player:
        """
        Creates a new player.

        :param bs: The BuyStrategy to use.
        :param ss: The SellStrategy to use.
        """
        self.bs : Type[Strategy.BuyStrategy] = bs
        self.ss : Type[Strategy.SellStrategy] = ss
        self.name : str = bs.name + "---" + ss.name
        self.bought_asset_pair : AssetPair | None = None
        self.color = random_color()
        self.log_file : str = Player.result_dir + self.name + ".res"
        self.detailed_log_file : str = Player.detailed_result_dir + self.name + ".res"
        self.brief_log_file : str = Player.brief_result_dir + self.name + ".res"

        self.wins : int = 0
        self.loss : int = 0
        self.total_points : float = 0

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
            file.write(self.name + " has bought: \n")
            file.write(str(self.bought_asset_pair) + "\n\n")
            file.write("---------------------------------------------------------------------------\n")

        with open(self.brief_log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] BRIEF\n")
            file.write(self.name + f" has {self.wins} wins\n")
            file.write(self.name + f" has {self.loss} losses\n")
            file.write(self.name + f" has {self.total_points} points\n")
            file.write("---------------------------------------------------------------------------\n")

    def should_sell(self : Player, ah : AH.AssetHandler) -> None:
        """
        Check whether the currently held asset should be sold.

        :param ah: The AssetHandler to use as a reference.
        """
        return self.ss.strategy(self, ah.pairs[self.bought_asset_pair.name])

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
        profit = profit * 100

        if profit > ah.pairs[self.bought_asset_pair.name].fee:
            self.wins += 1
        else:
            self.loss += 1

        self.total_points += profit

        with open(self.log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] SOLD\n")
            file.write(self.name + " has sold " + self.bought_asset_pair.base.name)
            file.write(" for $" + str(ah.pairs[self.bought_asset_pair.name].data.current))
            file.write(". Profit was " + str(profit) + "%.\n")

        with open(self.detailed_log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] SOLD\n")
            file.write(self.name + " has sold: \n")
            file.write(str(self.bought_asset_pair) + "\n")
            file.write("Profit was " + str(profit) + "%.\n")
            file.write("---------------------------------------------------------------------------\n")

        with open(self.brief_log_file, "a") as file:
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] BRIEF\n")
            file.write(self.name + f" has {self.wins} wins\n")
            file.write(self.name + f" has {self.loss} losses\n")
            file.write(self.name + f" has {self.total_points} points\n")
            file.write("---------------------------------------------------------------------------\n")

        self.bought_asset_pair = None

    def __str__(self : Player) -> str:
        s = ""
        s += "Name: " + self.name + "\n"
        s += "BuyStrategy description: " + self.bs.description + "\n"
        s += "SellStrategy description: " + self.ss.description + "\n"

        s += "Buy strategy cached data: \n"
        s += tabulate(str(self.bs.cached_data)) + "\n"

        s += "Sell strategy cached data: \n"
        s += tabulate(str(self.ss.cached_data)) + "\n"

        s += "Bought asset pair: \n"
        s += tabulate(str(self.bought_asset_pair)) + "\n"
        s += "Wins: " + str(self.wins) + "\n"
        s += "Losses: " + str(self.loss) + "\n"
        s += "Total points: " + str(self.total_points)
        return s
        
