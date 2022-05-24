from __future__ import annotations
import time
import os
import requests
import urllib.parse
import hashlib
import hmac
import base64

from typing import Any, Dict, List, Tuple

from Error import Error

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

        # login information
        self.api_url : str = api_url
        self.api_key : str = api_key
        self.api_sec : str = api_sec

    ###########################################################################
    ####################### LOGIN #############################################
    ###########################################################################

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
    def private_kraken_request(self : KrakenAPI, uri_path : str, data : Dict[str, Any]) -> Dict[str, Any] | Error:
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
        res = req.json()

        # if there was an error, only return the error
        if res["error"] != []:
            return Error(res["error"])

        return res["result"]

    def public_kraken_request(self : KrakenAPI, url_path : str) -> Dict[str, Any] | Error:
        """
        Sends a requests to the Kraken API and returns its result. This is the
        public version.

        :param post_url: The URL to use for the POST request.

        :returns: Anything that the REST API returns.
        """
        res = requests.get(url_path).json()
        
        # if there was an error, only return the error
        if res["error"] != []:
            return Error(res["error"])

        return res["result"]

    @staticmethod
    def get_nonce() -> str:
        """
        Returns a valid nonce.

        :returns: A valid nonce.
        """
        return str(int(1000 * time.time()))