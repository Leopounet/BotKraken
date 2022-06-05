from __future__ import annotations
from datetime import datetime
import traceback
import time
from typing import List, Set, Tuple, Type
import glob, importlib, sys

from Structures.AssetHandler import AssetHandler
from Structures.Player import Player
from Structures.KrakenAPI import KrakenAPI
import Structures.Strategy as Strategy
from Utils.StringManipulation import tabulate

class PlayerHandler:

    """
    This class is used to handle multiple players.
    """

    bsd = "BuyStrategies"
    ssd = "SellStrategies"
    ef : Set[str] = "__init__.py"
    summary_log_file : str = "Results/summary.res"

    def __init__(self : PlayerHandler, ah : AssetHandler, kapi : KrakenAPI) -> PlayerHandler:
        """
        Creates a new PlayerHandler object.

        :param ah: The AssetHandler to use.
        :param kapi: The KrakenAPI to use.
        """
        self.ah : AssetHandler = ah
        self.kapi : KrakenAPI = kapi
        self.players : List[Player] = []

        self.bsm : Set[str] = set()
        self.ssm : Set[str] = set()

    def generate_players(self : PlayerHandler) -> None:
        """
        Generates new players if required.
        """
        buy_strategies = set(glob.glob(PlayerHandler.bsd + "/*.py"))
        bs_init_files = set(glob.glob(PlayerHandler.bsd + "/" + PlayerHandler.ef))

        sell_strategies = set(glob.glob(PlayerHandler.ssd + "/*.py"))
        ss_init_files = set(glob.glob(PlayerHandler.ssd + "/" + PlayerHandler.ef))

        bsm = buy_strategies.difference(bs_init_files).difference(self.bsm)
        ssm = sell_strategies.difference(ss_init_files).difference(self.ssm)

        was_empty = True if self.bsm == set() and self.ssm == set() else False

        self.bsm = self.bsm.union(bsm)
        self.ssm = self.ssm.union(ssm)

        for bm in bsm:
            for sm in self.ssm:
                bspn = PlayerHandler.bsd + "."
                bsmn = bm.split("/")[-1].split(".")[0]
                bs : Type[Strategy.BuyStrategy] = importlib.import_module(bspn + bsmn).Strategy

                sspn = PlayerHandler.ssd + "."
                ssmn = sm.split("/")[-1].split(".")[0]
                ss : Type[Strategy.SellStrategy] = importlib.import_module(sspn + ssmn).Strategy

                self.players.append(Player(bs, ss))

        if not was_empty:
            for bm in self.bsm:
                for sm in ssm:
                    bspn = PlayerHandler.bsd + "."
                    bsmn = bm.split("/")[-1].split(".")[0]
                    bs : Type[Strategy.BuyStrategy] = importlib.import_module(bspn + bsmn).Strategy

                    sspn = PlayerHandler.ssd + "."
                    ssmn = sm.split("/")[-1].split(".")[0]
                    ss : Type[Strategy.SellStrategy] = importlib.import_module(sspn + ssmn).Strategy

                    self.players.append(Player(bs, ss))

    def save_best(self : PlayerHandler) -> Tuple[Player, Player, Player]:
        """
        """
        with open(self.summary_log_file, "w") as file:
            most_losses = sorted(self.players, key=lambda x: x.loss)[-1]
            most_wins = sorted(self.players, key=lambda x: x.wins)[-1]
            best_score = sorted(self.players, key=lambda x: x.total_points)[-1]
            biggest_wallet = sorted(self.players, key=lambda x: x.wallet)[-1]
            file.write("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] SUMMARY\n")
            file.write("Most losses: \n")
            file.write(str(most_losses) + "\n")
            file.write("---------------------------------------------------------------------------\n")
            file.write("Most wins: \n")
            file.write(str(most_wins) + "\n")
            file.write("---------------------------------------------------------------------------\n")
            file.write("Best score: \n")
            file.write(str(best_score) + "\n")
            file.write("---------------------------------------------------------------------------\n")
            file.write("Biggest wallet: \n")
            file.write(str(biggest_wallet) + "\n")
            file.write("---------------------------------------------------------------------------\n")

    def play(self : PlayerHandler) -> None:
        """
        A round of play.
        """
        try:
            self.ah.update_assets(self.kapi)
            self.ah.update_tradable_assets(self.kapi)
            self.ah.update_usd_tradable_prices(self.kapi, total=2)
            self.generate_players()
            for player in self.players:
                if player.bought_asset_pair == None:
                    player.buy_asset(self.ah)
                elif player.should_sell(self.ah):
                    player.sell_asset(self.ah)
            self.save_best()                
        except Exception as e:
            self.handle_exception(e, sys.exc_info())

    def __str__(self : PlayerHandler) -> str:
        s = ""
        s += "Asset handler: \n"
        s += tabulate(str(self.ah)) + "\n"
        
        for player in self.players:
            s += f"Player {player.name}: \n"
            s += tabulate(str(player)) + "\n"

        s += "BuyStrategy modules: " + str(self.bsm) + "\n"
        s += "SellStrategy modules: " + str(self.ssm)
        return s

    def handle_exception(self : PlayerHandler, e : Exception, details : sys._OptExcInfo) -> None:
        """
        Handles an exception, if one happens.
        """
        with open("logs" + str(int(time.time())) + ".txt", "a") as file:
            file.write(str(e) + "\n")
            type, value, traceback = details
            file.write(str(type) + "\n")
            file.write(str(value) + "\n")
            file.write(str(traceback) + "\n")
            file.write(str(traceback.tb_frame) + "\n")
            file.write(str(traceback.tb_lasti) + "\n")
            file.write(str(traceback.tb_lineno) + "\n\n")
            print(str(traceback))

            file.write(str(self))
            file.write("\n\n\n--------------------------------------------------------------")

