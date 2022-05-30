from __future__ import annotations

from typing import Dict, Any

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

        return asset

    def copy(self : Asset) -> Asset:
        """
        Creates and returns a copy of this asset.
        """
        a = Asset()
        a.name = self.name
        a.altname = self.altname
        a.decimals = self.decimals
        a.display_decimals = self.display_decimals
        return a

    def __str__(self : Asset) -> str:
        s = f"Name = {self.name}\n"
        s += f"Altname = {self.altname}\n"
        s += f"decimals = {self.decimals}\n"
        s += f"displayed_decimals = {self.display_decimals}"
        return s