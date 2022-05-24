from __future__ import annotations

from Error import Error
from typing import Any, Dict, List

from KrakenAPI import KrakenAPI

###############################################################################
############################## CLASSES ########################################
###############################################################################

class Asset:

    """
    This class represents an asset.
    """

    def __init__(self : Asset) -> Asset:
        """
        Creates a new asset.
        """
        self.name : str = None
        self.altname : str = None
        self.decimals : int = None
        self.display_decimals : int = None
        self.price_to_usd : Dict[int, float] = None

    @staticmethod
    def build_asset(name : str, data : Dict[str, Any]) -> Asset:
        """
        This methods builds a new asset and returns it.

        :param name: The name of the asset being created.
        :param data: Data returned from Kraken corresponding to
        this asset.

        :returns: The constructed Asset.
        """

        # the new asset and shorter names
        asset = Asset()
        asset.name = name

        asset.altname = data["altname"]
        asset.decimals = data["decimals"]
        asset.display_decimals = data["display_decimals"]
        asset.price_to_usd = {}

        return asset

    @staticmethod
    def update_asset(asset : Asset, data : Dict[str, any]) -> Asset:
        """
        Updates an existing Asset and returns it.

        :param asset: The asset to update.
        :param data: Data returned from Kraken corresponding to
        this asset.

        :returns: The same Asset object but update.
        """
        asset.altname = data["altname"]
        asset.decimals = data["decimals"]
        asset.display_decimals = data["display_decimals"]
        return asset

    def __str__(self : Asset) -> str:
        s = f"Name = {self.name}\n"
        s += f"Altname = {self.altname}\n"
        s += f"decimals = {self.decimals}\n"
        s += f"displayed_decimals = {self.display_decimals}"
        return s

class AssetHandler:

    """
    This class is used to handle a list of assets, it keeps track of all
    the existing assets and the values associated to them.
    """

    def __init__(self : AssetHandler) -> AssetHandler:
        """
        Creates a new asset handler.
        """
        self.assets : Dict[str, Asset] = {}

    def update_assets(self : AssetHandler, kapi : KrakenAPI) -> None:
        """
        This methods updates the list of existing assets.

        :param kapi: The already initialized KrakenAPI.
        """
        result = kapi.public_kraken_request('https://api.kraken.com/0/public/Assets')

        if isinstance(result, Error):
            print("An error occurred!")
            return None

        for asset in result:
            if asset in self.assets:
                self.assets[asset] = Asset.update_asset(self.assets[asset], result[asset])
            else:
                self.assets[asset] = Asset.build_asset(asset, result[asset])


    def __str__(self : AssetHandler) -> str:
        s = ""
        for element in self.assets:
            s += str(self.assets[element]) + "\n"
            s += "-------------------------------------------------\n"
        return s.rstrip("\n")
