from __future__ import annotations
from typing import List, Set
import glob, importlib

from Structures.AssetHandler import AssetHandler
from Structures.Player import Player
from Structures.KrakenAPI import KrakenAPI
from Structures.Types import BuyStrategy, SellStrategy

class PlayerHandler:

    """
    This class is used to handle multiple players.
    """

    bsd = "BuyStrategies"
    ssd = "SellStrategies"
    ef : Set[str] = "__init__.py"

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
                bs_package_name = PlayerHandler.bsd + "."
                bs_module_name = bm.split("/")[-1].split(".")[0]
                bs : BuyStrategy = importlib.import_module(bs_package_name + bs_module_name).strategy

                ss_package_name = PlayerHandler.ssd + "."
                ss_module_name = sm.split("/")[-1].split(".")[0]
                ss : BuyStrategy = importlib.import_module(ss_package_name + ss_module_name).strategy

                self.players.append(Player(bs, ss, bs_module_name[:3] + " " + ss_module_name[:3]))

        if not was_empty:
            for bm in self.bsm:
                for sm in ssm:
                    bs_package_name = PlayerHandler.bsd + "."
                    bs_module_name = bm.split("/")[-1].split(".")[0]
                    bs : BuyStrategy = importlib.import_module(bs_package_name + bs_module_name).strategy

                    ss_package_name = PlayerHandler.ssd + "."
                    ss_module_name = sm.split("/")[-1].split(".")[0]
                    ss : BuyStrategy = importlib.import_module(ss_package_name + ss_module_name).strategy

                    self.players.append(Player(bs, ss, bs_module_name[:3] + " " + ss_module_name[:3]))
    
    def play(self : PlayerHandler) -> None:
        """
        A round of play.
        """
        self.ah.update_assets(self.kapi)
        self.ah.update_tradable_assets(self.kapi)
        self.ah.update_usd_tradable_prices(self.kapi)
        self.generate_players()
        for player in self.players:
            if player.bought_asset_pair == None:
                player.buy_asset(self.ah)
            elif player.should_sell(self.ah):
                player.sell_asset(self.ah)

