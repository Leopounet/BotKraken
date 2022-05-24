from __future__ import annotations
import time
import os
import requests
import urllib.parse
import hashlib
import hmac
import base64

from DataStructures import ErrorType, Pair, Asset, Error, Response
from typing import Any, Dict, List, Tuple

###############################################################################
############################## VARIABLES ######################################
###############################################################################

###############################################################################
############################## CLASSES ########################################
###############################################################################

class KrakenAPI:
    
    def __init__(self : KrakenAPI, api_url : str, api_key : str, api_sec : str) -> KrakenAPI:
        """
        Creates a new KrakenAPI object which will hold all of your 
        personal data and some other details. This object can be
        used to easily send requests to the Kraken API.

        :param api_url: The url of the API.
        :param api_key: The public key.
        :param sec_key: The secret key.
        """
        self.api_url : str = api_url
        self.api_key : str = api_key
        self.api_sec : str = api_sec

    def get_kraken_signature(self : KrakenAPI, uri_path : str, data : Dict[str, Any]) -> bytes:
        """
        Generates a Kraken Signature.

        :param uri_path: The URI to use for the POST request.
        :param data: A dictionary of requested parameters.

        :returns: The signature.
        """
        post_url = self.api_url + uri_path

        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = uri_path.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.api_sec), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()
        

    # Attaches auth headers and returns results of a POST request
    def private_kraken_request(self : KrakenAPI, uri_path : str, data : Dict[str, Any]) -> Any:
        """
        Sends a requests to the Kraken API and returns its result. This is the
        private version, which means that an authentification is required.

        :param uri_path: The URI to use for the POST request.
        :param data: A dictionary of requested parameters.

        :returns: Anything that the REST API returns.
        """
        headers = {}
        headers['API-Key'] = self.api_key
        headers['API-Sign'] = self.get_kraken_signature(uri_path, data)         
        req = requests.post((self.api_url + uri_path), headers=headers, data=data)
        return req

    def public_kraken_request(self : KrakenAPI, url_path : str) -> Any:
        """
        Sends a requests to the Kraken API and returns its result. This is the
        public version.

        :param post_url: The URL to use for the POST request.

        :returns: Anything that the REST API returns.
        """
        return requests.get(url_path)

    @staticmethod
    def get_nonce() -> str:
        """
        Returns a valid nonce.

        :returns: A valid nonce.
        """
        return str(int(1000 * time.time()))

    ###########################################################################
    ############################### GETTERS ###################################
    ###########################################################################

    def generic_getter(self : KrakenAPI, cached : Response, element : str, *,
                       try_altname : bool = True) -> Response:
        """
        Generic getter that works most of the time.

        :param json: The json dict to find the element in.
        :param element: The element to find.

        :return: A tuple of the key that worked and the element.
        """
        resp = Response(element)
        json = cached.result

        if cached.error is not None:
            return cached

        # check for errors
        if json["error"] != []:
            print("Some error occurred:")
            print(json["error"])
            resp.error = Error(json["error"])
            return resp

        # direct check
        if element in json["result"]:
            resp.result = json["result"][element]
            return resp

        # check altname, if requested
        if try_altname:
            result = json["result"]
            for key in result:
                if "altname" in result[key] and result[key]["altname"] == element:
                    resp.result = result[key]
                    return resp

        print("Requested element is not listed...")
        resp.error = ErrorType.UNKNOWN_ERROR
        return resp

    ###########################################################################
    ############################### BALANCE ###################################
    ###########################################################################

    def _get_balance(self : KrakenAPI) -> Response:
        """
        Returns your balance.
        """
        resp = Response("")

        json = self.private_kraken_request(
                    "/0/private/Balance", 
                    {
                        "nonce": KrakenAPI.get_nonce()
                    }
                )

        if json["error"] != []:
            resp.error = Error(json["error"])
            return resp

        resp.result = json["result"]
        return resp

    def get_balance(self : KrakenAPI, asset : Asset, balance : Response = None) -> Response:
        """
        Wrapper returning the balance of the requested currency.

        :param currency: The currency of which the balance is requested.
        :param balance: The balance to use (if not specified, a call to
        the API is made).

        :returns: The balance of the requested currency, 0 is the default case.
        """
        balance = self._get_balance() if balance is None else balance
        return self.generic_getter(balance, asset.name)

    def available_currencies_in_balance(self : KrakenAPI, balance : Response = None) -> Response:
        """
        Wrapper returning the list of currencies in the wallet.

        :param balance: The balance to use (if not specified, a call to
        the API is made).

        :returns: A list of possible currency.
        """
        resp = Response("")
        balance = self._get_balance() if balance is None else balance

        # check for errors
        if balance.error != None:
            return balance

        resp.result = list(balance.result.keys())
        return resp

    ###########################################################################
    ############################### ASSETS ####################################
    ###########################################################################

    def _get_tradable_pairs(self : KrakenAPI) -> Response:
        """
        Returns a dictionary of all tradable pairs of assets.

        :returns: A dictionary of all tradable paris of assets.
        """
        resp = Response("")
        json = requests.get('https://api.kraken.com/0/public/AssetPairs')

        # check for errors
        if json["error"] != []:
            print("Some error occurred:")
            print(json["error"])
            resp.error = Error(json["error"])
            return resp

        resp.result = json["result"]
        return resp

    def _get_assets(self: KrakenAPI) -> Response:
        """
        Returns a dictionary of all possible assets.

        :returns: A dictionary of all possible assets.
        """
        resp = Response("")
        json = requests.get('https://api.kraken.com/0/public/Assets')

        # check for errors
        if json["error"] != []:
            print("Some error occurred:")
            print(json["error"])
            resp.error = Error(json["error"])
            return resp

        resp.result = json["result"]
        return resp

    def get_all_tradable_pairs(self : KrakenAPI, pairs : Any = None) -> Response:
        """
        Returns a list of tradable pairs.

        :param pairs: Pairs to use, if not specified a call to the
        API is made.

        :returns: A list of tradable assets pairs.
        """
        resp = Response("")

        pairs = self._get_tradable_pairs().json() if pairs is None else pairs.json()

        # check for errors
        if pairs["error"] != []:
            print("Some error occurred:")
            print(pairs["error"])
            resp.error = Error(pairs["error"])
            return resp

        resp.result = list(pairs["result"].keys())
        return resp

    def get_tradable_pair(self : KrakenAPI, pair : Pair, pairs : Any = None) -> Response:
        """
        Returns info about a specific pair of tradable assets.

        :param pair: A pair of tradable assets.
        :param pairs: Pairs to use, if not specified a call to the
        API is made.

        :returns: The info about the requested tradable pair, if
        the pair does not exist, returns None.
        """
        pairs = self._get_tradable_pairs().json() if pairs is None else pairs.json()
        return self.generic_getter(pairs, pair.name)

    def get_all_assets(self : KrakenAPI, assets : Any = None) -> Response:
        """
        Returns a list of all possible assets.

        :param assets: Assets to use, if not specified a call to the
        API is made.

        :returns: A list of all possible assets.
        """
        resp = Response("")
        assets = self._get_assets().json() if assets is None else assets.json()

        # check for errors
        if assets["error"] != []:
            print("Some error occurred:")
            print(assets["error"])
            resp.error = Error(assets["error"])
            return resp

        resp.result = list(assets["result"].keys())
        return resp

    def get_asset(self : KrakenAPI, asset : Asset, assets : Any = None) -> Response:
        """
        Returns info about a specific asset.

        :param asset: An asset to get the info of.
        :param assets: Assets to use, if not specified a call to the
        API is made.

        :returns: The info about the requested asset, if
        the asset does not exist, returns None.
        """
        assets = self._get_assets().json() if assets is None else assets.json()
        return self.generic_getter(assets, asset.name)

    ###########################################################################
    ############################### INFORMATION ###############################
    ###########################################################################

    def _get_ticker(self : KrakenAPI, pair : Pair) -> Response:
        """
        Returns all the raw ticker info.

        :param pair: The pair of tradable assets to get the ticker info
        of.

        :returns: A dictionary of ticker information about the requested
        tradable pair, if it does not exist returns None.
        """
        resp = Response(pair.name)
        json = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair.name}')

        # check for errors
        if json["error"] != []:
            print("Some error occurred:")
            print(json["error"])
            resp.error = Error(json["error"])
            return resp

        resp.result = resp["result"]
        return resp

    def get_current_price(self : KrakenAPI, pair : Pair, ticker : Dict[str, Any] = None) -> Response:
        """
        Returns the current conversion rate of a given tradable pair of assets.

        :param pair: The pair to get the current price of.

        :returns: The current price of the pair.
        """
        resp = Response(pair.name)
        ticker = self._get_ticker(pair).json() if ticker is None else ticker.json()
        _, data = self.generic_getter(ticker, pair.name)
        return {"buy": float(data["c"][0]), "sell": 1 / float(data["c"][0])}

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

###############################################################################
############################## MAIN ###########################################
###############################################################################
