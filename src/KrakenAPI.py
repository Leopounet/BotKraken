from __future__ import annotations
import time
import os
import requests
import urllib.parse
import hashlib
import hmac
import base64

from typing import Any, Dict, List

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

    def _get_balance(self : KrakenAPI) -> Any:
        """
        Returns your balance.
        """
        return self.private_kraken_request(
                    "/0/private/Balance", 
                    {
                        "nonce": KrakenAPI.get_nonce()
                    }
                )

    def get_balance(self : KrakenAPI, currency : str) -> int:
        """
        Wrapper returning the balance of the requested currency.

        :param currency: The currency of which the balance is requested.

        :returns: The balance of the requested currency, 0 is the default case.
        """
        balance = self._get_balance().json()

        # check for errors
        if balance["error"] != []:
            print("Some error occurred:")
            print(balance["error"])
            return None

        if not currency in balance["result"]:
            print("Requested currency is not listed...")
            return 0
        
        return balance["result"][currency]

    def available_currency_in_balance(self : KrakenAPI) -> List[str]:
        """
        Wrapper returning the list of currencies in the wallet.

        :returns: A list of possible currency.
        """
        balance = self._get_balance().json()

        # check for errors
        if balance["error"] != []:
            print("Some error occurred:")
            print(balance["error"])
            return None

        return list(balance["result"].keys())


###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

###############################################################################
############################## MAIN ###########################################
###############################################################################
