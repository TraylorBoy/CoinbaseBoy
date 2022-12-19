"""Coinbase wrapper in Python"""
import json, hmac, hashlib, time, base64, requests
from requests.auth import AuthBase
from botboy import BotBoy


class CBoyAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self._api_key = api_key
        self._secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or "")
        signature = hmac.new(
            self._secret_key.encode("utf-8"),
            message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        request.headers.update(
            {
                "CB-ACCESS-SIGN": signature,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-ACCESS-KEY": self._api_key,
            }
        )

        return request


class CBoy:
    CB_API_URL = "https://api.coinbase/v2/"
    AT_API_URL = "https://api.coinbase.com/api/v3/brokerage/"

    def __init__(self, silent=True):
        self._auth = None
        self._user = None
        self._silent = silent

    @property
    def auth(self):
        """Auth getter"""
        return self._auth

    @auth.setter
    def auth(self, connection):
        """Auth setter"""
        self._auth = connection

    @property
    def user(self):
        """User getter"""
        return self._user

    @user.setter
    def user(self, user):
        """User setter"""
        self._user = user

    @property
    def silent(self):
        """Silent getter"""
        return self._silent

    @silent.setter
    def silent(self, is_silent):
        """Silent setter"""
        self._silent = is_silent

    def connect(self, api_key, secret_key):
        """Connect to the Authenticated Coinbase Client

        api_key (String) - API Key from Coinbase Exchange
        secret_key (String) - Secret Key from Coinbase Exchange
        """
        # Create auth client
        self.log("Connecting to Coinbase...")
        self.auth = CBoyAuth(api_key, secret_key)

        # Get the user data
        self.log("Retrieving user data...")
        req = requests.get(self.CB_API_URL + "user", auth=self.auth)
        self.user = req.json()

    def tokens(self):
        """Retrieve all tokens from Coinbase"""

        def task():
            return requests.get(self.CB_API_URL + "currencies")

        bot = BotBoy("Tokens Request", task, silent=False)
        bot.execute(wait=True)
        req = bot.result
        print(req)
        return req

    def price(self, of):
        """Retrieves the price of a coin

        of (String) - Pairing to retrieve price of ex. BTC-USD
        """
        pass

    def log(self, msg):
        """Prints msg to output"""
        if not self.silent:
            print(msg)
