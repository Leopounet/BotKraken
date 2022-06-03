import os

import Structures.AssetHandler as AH

from Structures.KrakenAPI import KrakenAPI
from Structures.Player import Player
from Structures.PlayerHandler import PlayerHandler

from BuyStrategies.Random import Strategy as Random
from SellStrategies.TFH_or_TPD import Strategy as TFHTPD

def test():
    # login infos
    api_url = "https://api.kraken.com"
    api_key = os.environ["API_KEY_KRAKEN"]
    api_sec = os.environ["API_SEC_KRAKEN"]

    kapi = KrakenAPI(api_url, api_key, api_sec)
    ah = AH.AssetHandler()
    ph = PlayerHandler(ah, kapi)

    player = Player(Random, TFHTPD)
    ph.players.append(player)

    for i in range(2):
        print(i)
        ph.ah.update_assets(ph.kapi)
        ph.ah.update_tradable_assets(ph.kapi)
        ph.ah.update_usd_tradable_prices(ph.kapi, total=2)
        for player in ph.players:
            print(player.name)
            if player.bought_asset_pair == None:
                player.buy_asset(ph.ah)
            elif player.should_sell(ph.ah):
                player.sell_asset(ph.ah)
        ph.save_best()